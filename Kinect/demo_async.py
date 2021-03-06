import freenect
import signal
import numpy
import frame_convert
import Image

keep_running = True

def display_depth(dev, data, timestamp):
  #numpy.set_printoptions(threshold='nan')
  #  numpy.savetxt("outputnumpy.txt", data, fmt='%f', delimiter=',', newline='] ')
  #numpy.ndarray.tofile("outputnumpy.txt", sep=' ', format='%f')
  #data.numpy.tolist()
  #a=numpy.fromstring(data)
  #  M=[[int(num) for num in line.strip().split()] for line in data.split('\n')]
  array = frame_convert.pretty_depth(data)
  print array
  #im = Image.fromarray(array)
  #im.save("pic.jpg")

def display_rgb(dev, data, timestamp):
  data

def body(*args):
  if not keep_running:
    raise freenect.Kill

def handler(signum, frame):
  global keep_running
  keep_running = False

print('Press Ctrl-C in terminal to stop')
signal.signal(signal.SIGINT, handler)
freenect.runloop(depth=display_depth,
		 video=display_rgb,
		 body=body)
