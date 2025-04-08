import time
import os
import datetime
import signal
import psutil

class Looper(object):
  def __init__(self):
    self.done = False
    return
  
  def get_cpu_limit(self):
    try:
      cpu_quota = int(open('/sys/fs/cgroup/cpu/cpu.cfs_quota_us').read())
      cpu_period = int(open('/sys/fs/cgroup/cpu/cpu.cfs_period_us').read())
      return cpu_quota / cpu_period if cpu_quota > 0 else os.cpu_count()
    except Exception:
      return os.cpu_count()

  def get_memory_limit(self):
    try:
      mem_limit = int(open('/sys/fs/cgroup/memory/memory.limit_in_bytes').read())
      return mem_limit / (1024 * 1024)
    except Exception:
      return psutil.virtual_memory().total / (1024 * 1024)  
  
  def run(self):
    hostname = os.getenv("HOSTNAME", "UNKNOWN")
    self.cnt = 0
    print(f"Starting looper on {hostname}", flush=True)
    while not self.done:
      self.cnt += 1
      mem_mb = self.get_memory_limit()
      cpus = self.get_cpu_limit()
      str_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      print(f"[{str_date}][{hostname}]: Iter #{self.cnt}, Cpus: {cpus}, Mem: {mem_mb:,.0f} MiB", flush=True)
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
  print("Done.", flush=True)
