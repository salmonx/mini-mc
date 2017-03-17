# -*- coding: utf-8 -*-

# Copyright (c) 2015 Xi Wang
#
# This file is part of the UW CSE 551 lecture code.  It is freely
# distributed under the MIT License.

# ---------------------------------------------------------------
# symbolic
# ---------------------------------------------------------------

from mc_util import *

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


def sat_check(conditions, current_condition):
  
  solver.push()
  for condition in conditions:
    solver.add(condition)
  solver.add(current_condition)
  ret = solver.check()
  solver.pop()
  return ret == sat


tree = ConditionTree()
current = tree
path = []

# handle __bool__ when "if"
def handle_bool(current_condition):
  
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
  
  


def newpos():
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
  global path
  path = []
  tmp = current

  if tmp.condition is None:
    print "reach root"
    return False

  while tmp:
    path.append(tmp.condition)
    tmp = tmp.parent

  path = path[::-1]
  

  path = path[1:]
  print "path:", path
  return True

counter = 0
#dfs search the tree
def sched(func, init=True):
  global counter
  counter = 0
  print "-----------------------START-------------------------------"
  
  if not init:
    if not newpos():
      return

    if not gen_path():
      return 
  
  try:
    func()
  except:
    print "err"
    pass
    #typ, value, tb = sys.exc_info()
    #sys.excepthook(typ, value, tb.tb_next)
  sched(func, False)

 
setattr(BoolRef, "__bool__", handle_bool)
setattr(BoolRef, "__nonzero__", getattr(BoolRef, "__bool__"))
