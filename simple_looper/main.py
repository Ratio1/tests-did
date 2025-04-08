import time
import os
import datetime
import signal

class Looper(object):
  def __init__(self):
    self.done = False
    return

  def run(self):
    hostname = os.getenv("HOSTNAME", "UNKNOWN")
    self.cnt = 0
    print(f"Starting looper on {hostname}", flush=True)
    while not self.done:
      self.cnt += 1
      str_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      print(f"[{str_date}][{hostname}]: Iter #{self.cnt}", flush=True)
      time.sleep(5)
    return

if __name__ == "__main__":
  eng = Looper()

  # capture SIGINT
  def signal_handler(sig, frame):
    print("\nExiting...", flush=True)
    eng.done = True
    return  
  
  signal.signal(signal.SIGINT, signal_handler)

  eng.run()
