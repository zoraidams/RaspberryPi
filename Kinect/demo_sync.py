import freenect
import signal
import numpy

keep_running = True

def get_depth():
  return freenect.sync_get_depth()

def get_video():
  return freenect.sync_get_video()

def handler(signum, frame):
  """ Sets up the kill handler, catches SIGINT """
  global keep_running
  keep_running = False

while keep_running:
  a = get_depth()
  numpy.savetxt("outputnumpy.txt", a[0], fmt='%d', delimiter=',', newline='\nNew slice\n')
