import freenect
import signal
import numpy
import frame_convert
import Image

keep_running = True

def get_depth():
  return frame_convert.pretty_depth(freenect.sync_get_depth()[0])

def get_video():
  return freenect.sync_get_video()[0]

def handler(signum, frame):
  """ Sets up the kill handler, catches SIGINT """
  global keep_running
  keep_running = False

#print('Press Ctrl-C in terminal to stop')
#while keep_running:
  #numpy.savetxt("outputnumpy.txt", a[0], fmt='%d', delimiter=',', newline='\nNew slice\n')
#  depth = get_depth()
#  video = get_video()
#  depim = Image.fromarray(depth)
#  vidim = Image.fromarray(video)
#  depim.save("picdepth.jpg")
#  vidim.save("picvid.jpg")

depth = get_depth()
video = get_video()
depim = Image.fromarray(depth)
vidim = Image.fromarray(video)
depim.save("picdepth.jpg")
vidim.save("picvid.jpg")
