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
  log("Docker is running.")
  gpu_check()
  res = runner()
  log("Result:", res)
  log("Done.")
  return


def cuda_checker():
  try:
    res = run_command(["nvidia-smi"])
  except Exception as e:
    log(f"Error: {e}")
    res = ""

  if res == "":
    return False
  return True

def pytorch_cuda_checker():
  import torch
  if torch.cuda.is_available():
    device = torch.device("cuda")
    # print GPU info from torch
    log("PyTorch CUDA is available.")
    log("PyTorch CUDA Device:", device)
    log("PyTorch CUDA Device Name:", torch.cuda.get_device_name(0))
    return True
  return False

def gpu_check():
  log("Checking GPU...")
  if not cuda_checker():
    log("CUDA is not available.")
    return False
  if not pytorch_cuda_checker():
    log("PyTorch CUDA is not available.")
    return False
  return True
  
if __name__ == '__main__':
  main()