from functools import wraps
from multiprocessing import Lock
import os


lock = Lock()


logfile = 'log'

fp = open(logfile,'w+')

def logger(f, logfile = 'log'):
  with lock:
    @wraps(f)	
    def wrapper(*args, **kwds):
      ret = f(*args, **kwds)
      if not isinstance(ret, (int, str)):
        ret = solver.model()
      fp.write("[%s] %s\n" % (os.getpid(), ret))
    return wrapper

