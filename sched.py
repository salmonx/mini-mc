# -*- coding: utf-8 -*-

# Copyright (c) 2015 Xi Wang
#
# This file is part of the UW CSE 551 lecture code.  It is freely
# distributed under the MIT License.

# ---------------------------------------------------------------
# symbolic
# ---------------------------------------------------------------

from mc_util import *

class CondtionsTree:

  def __init__(self, condtion, parent=None):
    #self.traced = False
    self.parent = parent
    self.condtion = condtion
    self.leftchild = None
    self.rigntchild = None

  def addLeftchild(self, child):
    self.leftchild  = child

  def addRightchild(self, child):
    self.rigntchild = child

  def getCondtions(self):
    condtions = []
    while self.parent:
      tmp = self.parent
      condtions.append(tmp.condtion)

    return condtions



def sat_check(condtions, current_condtion):
  
  solver.push()
  for condtion in condtions:
    solver.add(condtion)
  solver.add(current_condtion)
  ret = solver.check()
  solver.pop()
  return ret == sat



tree = CondtionsTree()
current = tree


# handle __bool__ when "if"
def handle_bool(current_condtion):

  condtions = current.getCondtions()

  ret_left = sat_check(condtions, current_condtion)
  if ret_left:
    current.addLeftchild(current_condtion)

  neg_condtion = not current_condtion
  ret_right = sat_check(condtions, neg_condtion):
  if ret_right:
    current.addRightchild(neg_condtion)

  if ret_left:
    current = current.leftchild
  elif ret_right:
    current = current.rigntchild
  return ret_left



#dfs search the tree
def sched():
  
  













setattr(BoolRef, "__bool__", handle_bool)
setattr(BoolRef, "__nonzero__", getattr(BoolRef, "__bool__"))



def mc_fuzz(f, cnt = 0):

  trace = []
  setattr(BoolRef, "__bool__", lambda self: sched_dfs(self, trace))
  setattr(BoolRef, "__nonzero__", getattr(BoolRef, "__bool__"))

  try:
    f()
  except:
    typ, value, tb = sys.exc_info()
    sys.excepthook(typ, value, tb.tb_next)

  delattr(BoolRef, "__bool__")
  delattr(BoolRef, "__nonzero__")

  # this path done
  if trace:
    solver.add(Not(And(*trace)))

  # choose a new path
  while trace:
    solver.push()
    solver.add(Not(trace[-1]))
    trace = trace[:-1]
    solver.add(*trace)
    r = solver.check()
    solver.pop()
    if r == sat:
      m = solver.model()
      print m
      cnt = mc_fuzz(f, cnt + 1)

  return cnt

