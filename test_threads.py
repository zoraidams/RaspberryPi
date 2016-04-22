#!/usr/bin/python
import threading

def worker(count):
  """ Function that makes the work in the thread """
  print "This is the work %s that I do today" % count
  return

""" List of threads """
threads = list()

for i in range(3):
  t = threading.Thread(target=worker, args=(i,))
  threads.append(t)
  t.start()
