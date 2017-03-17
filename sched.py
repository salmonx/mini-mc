#coding:utf8
from z3 import *

class ConditionTree:

  def __init__(self, condition=None, parent=None):
    #self.traced = False
    self.parent = parent
    self.condition = condition
    self.leftchild = None
    self.rightchild = None

  def addLeftchild(self, child):
    self.leftchild  = ConditionTree(child, self)

  def addRightchild(self, child):
    self.rightchild = ConditionTree(child, self)

  def getCondtions(self):
    conditions = []
    tmp = self
    while tmp.parent:
      conditions.append(tmp.condition)
      tmp = tmp.parent
    return conditions

solver = Solver()
tree = ConditionTree()
current = tree
path = []
counter = 0

def sat_check(conditions, current_condition):
  solver.push()
  for condition in conditions:
    solver.add(condition)
  solver.add(current_condition)
  ret = solver.check()
  solver.pop()
  return ret == sat


def handle_bool(current_condition):
  # handle __bool__ when "if"
  global counter, current
  counter += 1
  if len(path) > counter:
    if str(path[counter-1]) == str(current_condition):
      return True
    else: # path[counter] == not current_condition:
      return False

  conditions = current.getCondtions()
  ret_left = sat_check(conditions, current_condition)
  if ret_left:
    current.addLeftchild(current_condition)

  neg_condition = Not(current_condition)
  ret_right = sat_check(conditions, neg_condition)
  if ret_right:
    current.addRightchild(neg_condition)

  if ret_left:
    current = current.leftchild
  elif ret_right:
    current = current.rightchild
  return ret_left

setattr(BoolRef, "__bool__", handle_bool)
setattr(BoolRef, "__nonzero__", getattr(BoolRef, "__bool__"))


def newpos():
  #when func run over, move to the other leaf node
  global current
  while current:
    if current.parent and current.parent.rightchild and \
      current.parent.rightchild != current:
      current = current.parent.rightchild
      break
    else:
      current = current.parent
      
  return current

def gen_path():
  #collect conditions from current to root to generate a path
  global path
  path = []
  tmp = current
  while tmp:
    path.append(tmp.condition)
    tmp = tmp.parent
  path = path[::-1]
  path = path[1:]

  return True

def out(firstrun, ret):

  solver.push()
  if firstrun:
    gen_path()
  print "PATH:", path
  for condition in path:
    solver.add(condition)
  
  if solver.check() == sat:
      print "INPUT:", solver.model()
  solver.pop()
  if ret:
    print "RET:", ret


def sched(func, firstrun=True):
 # run untill all branches reached
  global counter
  while True:
    counter = 0
    if not firstrun:
      if not newpos():
        return
      if not gen_path():
        return

    print "--------------------------START-------------------------------"
    try:
      ret = func()
      out(firstrun, ret)
    except:
      #pass
      typ, value, tb = sys.exc_info()
      sys.excepthook(typ, value, tb.tb_next)

    firstrun = False



def test_me(x, y):
  if x > 1:
    if y > 1:
      if x + y > 10:
        print "x>1, y>1, x+y>10"
      else:
        print "x>1, y>1, Not(x+y)>10"
    else:
      print "x>1, Not(y>1)"
  else:
    print "Not(x>1)"

x = BitVec("x", 32)
y = BitVec("y", 32)

if __name__ == '__main__':
  sched(lambda: test_me(x, y))