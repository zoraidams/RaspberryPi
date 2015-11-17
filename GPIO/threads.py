import threading

def worker(count):
  """funcion que realiza el trabajo en el thread"""
  print "Este es el %s trabajo que hago hoy" % count
  return

""" Lista de threads """
threads = list()

for i in range(3):
  t = threading.Thread(target=worker, args=(i,))
  threads.append(t)
  t.start()