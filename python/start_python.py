import subprocess
import os

# ---------------------------
# Parameters
# ---------------------------

# Network ports; each process is assigned one port
ports = [port_number for port_number in range(3500, 3520)]

# GPU map (Display, GPU-number)
gpu_map = [
    (":0", 1),
    (":1", 0),
    (":2", 2)
]

# Application to start (path to binary)
application = "../application/build/demo"

# Number of applications/ processes to start
number_processes = 5

# Index of the first process
process_start_index = 0

# Output directory of log files (capture stdout and stderr)
log_directory = "./log"

# Config template file and directory in which process configs are created
config_template_file = "template.toml"
config_directory = "./config"


# ------------------------------------
# Initialization
# ------------------------------------

# Check that a sufficient number of ports is available
if (process_start_index+number_processes) > len(ports):
    raise RuntimeError("Not enough ports available for the given number of processes.")

# Create directories for log and config ouput
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

if not os.path.exists(config_directory):
    os.makedirs(config_directory)

# Import configuration template
with open("config-template.toml", 'r') as f:
    template_config_file = f.read()    

# ---------------------------------
# Start application processes ...
# ---------------------------------    
for cc in range(number_processes):
    idx = cc + process_start_index 

    # Log files
    log_file = os.path.join(log_directory, "log_file" + str(idx) + ".txt")
    error_file = os.path.join(log_directory, "error_file.txt")

    # Port and GPU index
    port = str(ports[idx])
    gpu_idx = idx % len(gpu_map)
    
    # Write config file
    config_file = os.path.join(config_directory, "config_" + str(idx) + ".toml")
    with open(config_file, "w") as f:
        config_file_content = template_config_file.replace("$port", port)
        f.write(config_file_content)

    # Set environment variables
    env = {
    **os.environ,
    "DISPLAY": gpu_map[gpu_idx][0],
    "CUDA_VISIBLE_DEVICES": str(gpu_map[gpu_idx][1])
    }
    
    # Start application
    with open(log_file, "w") as l_file:
        with open(error_file, "a") as err_file:
            subprocess.Popen([application, config_file], env=env, stdout=l_file, stderr=err_file,
                              start_new_session=True)  # shell = True

print("Started " + str(number_processes) + " processes.")