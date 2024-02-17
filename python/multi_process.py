import os
from multiprocessing import current_process, Pool
import time
import subprocess
import shutil

# Number pool workers
number_workers = 3

# Server addresses; each worker is assigned one server
server_addresses = ["tcp://127.0.0.1:"+str(port_number) for port_number in range(3500, 3520)]

# Application to start (path to binary)
application = "./demo"

# Tasks / List of tasks to be performed
tasks = ["task_" + str(idx) for idx in range(5,15)]

# Results directory
results_directory = "./results"

# Create and initialize working directories for the pool workers
wrk_root_dir = "./wrk"
wrk_dirs = []

for cc in range(number_workers):
    worker_dir = os.path.join(wrk_root_dir, "wrk_"+str(cc))
    wrk_dirs.append(worker_dir)
    if not os.path.exists(worker_dir):
        os.makedirs(worker_dir)
    shutil.copy2("../application/build/demo", worker_dir) 

# ------------------------------------------------------------

# Utility function to move data
def move_if_exists(src, dest):
    if os.path.exists(src):
        shutil.move(src, dest)

# ------------------------------------------------------------

# Process a task
def process_task(task):
    p = current_process()

    # Assign working directory and server to worker
    worker_idx = int(p._identity[0])-1
    worker_dir = wrk_dirs[worker_idx]
    server_address = server_addresses[worker_idx]

    # Set environment variables
    env = {
    **os.environ,
    "SERVER_ADDRESS": server_address
    }

    # Log file for program output
    log_file = os.path.join(worker_dir, "log.txt")

    # Start task
    print("Starting task: ", task, ", server address = ", server_address, ", worker_id = ", p._identity[0])
    with open(log_file, "w") as l_file:
        s_proc = subprocess.run([application, task], env=env, cwd=worker_dir, stdout=l_file, stderr=l_file)
        if s_proc.returncode != 0:
            print("Task \'" +str(task)+ "\' may have failed: Exit code = " + str(s_proc.returncode))

    # Copy results to output directory
    # List of output files relative to executable working directory    
    output_files = [
        "output_file.txt"
    ]    
    res_dir = os.path.join(results_directory, task)    
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)
    move_if_exists(log_file, res_dir)
    for output_file in output_files:
        move_if_exists(os.path.join(worker_dir, output_file), res_dir)
           
    # Just some time to relax ...
    time.sleep(5)

# ------------------------------------------------------------

if __name__ == '__main__':
    with Pool(number_workers) as p:
        r = p.map(process_task, tasks)
    p.join()  