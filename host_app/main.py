import subprocess
import multiprocessing
import threading
import time
import signal
import sys
import json

# List of containers to run
containers = []
CONFIG_FILE = "config.json"

container_processes = []

# Load container config from JSON file
def load_container_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# Dictionary to store container IDs and statuses
container_procs = {}

# Function to build docker run command
def build_docker_command(container):
    cmd = ["docker", "run", "--rm"]

    # Port mappings
    for port in container.get("ports", []):
        cmd += ["-p", port]

    # Volume mounts
    for volume in container.get("volumes", []):
        cmd += ["-v", volume]

    # Environment variables
    for env in container.get("env", []):
        cmd += ["-e", env]

    # Image name
    cmd.append(container["image"])

    return cmd


# Function to log in (if needed) and start a container
def run_container(container):
    image = container["image"]
    registry = container["registry"]
    username = container["username"]
    password = container["password"]

    try:
        # Log in to the registry
        if registry and username and password:
            login_cmd = f'echo "{password}" | docker login {registry} -u "{username}" --password-stdin'
            subprocess.run(login_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Logged into {registry}")

        # Run the container in foreground (blocking)
        run_cmd = build_docker_command(container)

        log (f"Starting container {image}...")

        process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        container_procs[image] = process
        log(f"Started container {image}...")

        # Start a thread to monitor logs
        log_thread = threading.Thread(target=monitor_clogs, args=(process, image), daemon=True)
        log_thread.start()

        process.wait()  # Wait for the container to finish
        print(f" Container {image} stopped.")

    except subprocess.CalledProcessError as e:
        log(f"Error starting {image}: {e.stderr.decode().strip()}")

# Function to monitor container logs in real-time
def monitor_clogs(process, image):
    try:
        log(f"Monitoring logs for {image} ...")
        
        # Read logs line by line
        for line in process.stdout:
            log(f"[{image}] {line.strip()}")

    except Exception as e:
        log(f"Error monitoring logs for {image}: {str(e)}")

def monitor_containers():
    while True:
        running_containers = [proc.poll() is None for proc in container_procs.values()]
        if not any(running_containers):  # If all containers have stopped
            print("All containers have stopped. Exiting.")
            break
        time.sleep(2)


def log(*args):
  print(*args, flush=True)

# Graceful shutdown handler
def shutdown_handler(signum, frame):
    print("\n Stopping all containers...")
    
    for image, process in container_procs.items():
        process.terminate()
        print(f" Stopped {image}")

    sys.exit(0)

# Attach signal handlers to handle CTRL+C and termination signals
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

def main():
  log("Checking Docker...")
  if not check_docker():
    log("Docker is not running.")
    return
  log("Docker is running.")
  gpu_check()

  containers = load_container_config()

  log("Starting containers....")
  with multiprocessing.Pool(len(containers)) as pool:
        pool.map(run_container, containers)
  # Start monitoring if at least one container is running
  monitor_containers()

  return


def run_command(cmd: list) -> str:
  log("Running command:", cmd)
  try:
    res = subprocess.run(cmd, text=True)
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