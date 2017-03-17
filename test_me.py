#!/usr/bin/env python

# Copyright (c) 2015 Xi Wang
#
# This file is part of the UW CSE 551 lecture code.  It is freely
# distributed under the MIT License.

"""
This resembles Section 2.4 of the DART paper (PLDI'05).
"""

#from mc import *
from sched import *

def test_me(x, y):
  z = 2 * x
  if z == y:
    if y == x + 10:
      print "z==y, y==x+10"
      if x > 0:
        print "x>0"
    else:
      print "z==y, y!=x+10"
  else:
    print "z!=y"



def test_me1(x, y):
	if x > 1:
		if y > 1:
			if x + y > 10:
				print " x>1, y>1, x+y>10"
			else:
				print " x>1, y>1"
	else:
		print " x<1"







x = BitVec("x", 32)
y = BitVec("y", 32)
#test_me(x, y)
#mc_fuzz(lambda: test_me(x, y), [x, y], [0, 0])
sched(lambda: test_me(x, y))
