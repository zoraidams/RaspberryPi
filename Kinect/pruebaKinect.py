# Need to import the required modules
import freenect
import time
import random
import signal

# Some global variables
keep_running = True
last_time = 0

# This is the function that will be
# run as the body of a run loop in freenect
# This example will randomly change the
# LED and the tilt angle of the kinect
def body(dev, ctx):
  global last_time
  if not keep_running:
    raise freenect.Kill
  if time.time() - last_time < 3:
    return
  last_time = time.time()
  led = random.randint(0, 6)
  tilt = random.randint(0, 30)
  freenect.set_led(dev, led)
  freenect.set_tilt_degs(dev, tilt)

# We will need a signal handler to let
# the user interrupt the run loop
def handler(signum, frame):
  """Sets up the kill handler, catches SIGINT"""
  global keep_running
  keep_running = False

# Now we set the signal handler and start the
# run loop - it will stop when you press CTRL-C
signal.signal(signal.SIGINT, handler)
freenect.runloop(body=body)

# If we want to get video data and display
# it, we need to import matplotlib
import matplotlib.pyplot as mp
keep_running = True

# Need to set up matplotlib
mp.ion()
mp.gray()

# Get an initial frame and set up the signal handler
image_rgb = mp.imshow(freenect.sync_get_video()[0], interpolation='nearest',
animated=True)
signal.signal(signal.SIGINT, handler)

# And now we loop
while keep_running:
  image_rgb.set_data(freenect.sync_get_video()[0])
  mp.draw()
  mp.waitforbuttonpress(0.01)
