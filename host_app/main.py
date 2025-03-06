import subprocess

def log(*args):
  print(*args, flush=True)


def run_command(cmd: list) -> str:
  log("Running command:", cmd)
  try:
    res = subprocess.run(cmd, capture_output=True, text=True)
    result = res.stdout
    return_code = res.returncode
    log(f"Return: {return_code}, Errors: {res.stderr}")
  except Exception as e:
    log(f"Error: {e}")
    result = ""
  if return_code != 0:
    result = ""
  return result
  
  
def runner() -> str:
  CMD = ["docker", "run", "aidamian/test-did-external-app"]
  log("Running the child app...")
  result = run_command(CMD)
  log("Child app finished.")
  return result

def check_docker():
  result = True
  res1 = run_command(["docker", "version"])
  res2 = run_command(["docker", "ps"])
  if res1 == "" or res2 == "":
    result = False
  return result

def main():
  log("Checking Docker...")
  if not check_docker():
    log("Docker is not running.")
    return
  res = runner()
  log("Result:", res)
  log("Done.")
  return
  
if __name__ == '__main__':
  main()