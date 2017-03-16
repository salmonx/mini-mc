from mc import *

x, y = Ints('x y')
ret = []

def abs(x):
	return x if x >= 0 else -x

@logger
def abs_test(a,b):
	if (a < 0):
		if (abs(a) == b):
			return 0
		return 1
	return 2


@logger
def andor(x,y):
	if(x or y):
		return 1
	else:
		return 2

#andor(x, y)

A = [0, 1, 0, 0, 1, 0, 1]
@logger
def arrayindex2(i):
	if i in [ j for j in range(len(A)) if A[j] ]:
 		return i
	else:
		return "OTHER"

#arrayindex2(x)

#ret = arrayindex2(x)
#log(ret)
@logger
def bad_eq(i):
	if (0 == i):
		return 0
	return 1
bad_eq(x)

