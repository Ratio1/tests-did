import subprocess

def log(*args):
  print(*args, flush=True)
  
  
def runner() -> str:
  CMD = ["docker", "run", "aidamian/test-did-external-app"]
  log("Running the child app...")
  try:
    res = subprocess.run(CMD, capture_output=True, text=True)
  except Exception as e:
    log(f"Error: {e}")
    return ""
  log("Child app finished.")
  return res.stdout

def main():
  res = runner()
  log("Result:", res)
  log("Done.")
  return
  
if __name__ == '__main__':
  main()