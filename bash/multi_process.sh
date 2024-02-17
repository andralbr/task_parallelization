#!/bin/bash

numberWorkers=3

tasks=(
"task_0"
"task_1"
"task_2"
"task_3"
"task_4"    
)

serverAddresses=(
"tcp://127.0.0.1:540"
"tcp://127.0.0.1:541"
"tcp://127.0.0.1:542"    
)

# Application for running tasks
application="./demo"

# Results root directory
resultsDir="./results"

# Root directory for worker working directories
wrkRootDir="./wrk"

# -----------------------------------------------------------
# Initialize ...
scriptDir=$(pwd)

# Create worker working directories (wrk_1, wrk_2, ...)
mkdir -p $wrkRootDir
wrkRootDir=$(realpath $wrkRootDir)
cd $wrkRootDir
cc=0
while [  $cc -lt $numberWorkers ]; do
  workerDir=wrk_$cc  
  mkdir -p $workerDir
  cp ${scriptDir}/../application/build/demo $workerDir
  cc=$((cc+1))
done
cd $scriptDir

# Create results root directory
mkdir -p $resultsDir
resultsDir=$(realpath $resultsDir)

# -----------------------------------------------------------

# Process task
processTask() { # $1 = idWorker, $2 = task
  echo "Worker $1: Task '$2' start"

  # Set environment
  export SERVER_ADDRESS=${serverAddresses[$1]}
  #echo $SERVER_ADDRESS

  # Execute task
  wrkDir=wrk_$1
  logFile="log.txt"
  cd $wrkRootDir
  cd $wrkDir
  $application $2 &> $logFile
  
  # Collect results 
  cd $resultsDir
  mkdir $2
  cd $2
  taskResultDir=$(pwd)
  cd $wrkRootDir
  cd $wrkDir
  mv $logFile $taskResultDir
  mv output_file.txt $taskResultDir
  
  cd $scriptDir

  # Random sleep task
  # sleep $(( ($RANDOM % 6) + 3 ))
  echo "Worker $1: Task '$2' finished"
}


# -----------------------------------------------------------

# Worker process. Workers run in parallel
worker() { # $1 = idWorker
  echo "Worker $1 started"
  idTask=0
  for task in "${tasks[@]}"; do
    # Selects a subset of tasks for the given worker
    (( idTask % numberWorkers == $1 )) && processTask $1 "$task"
    (( idTask++ ))
  done
  echo "Worker $1 finished."
}


# -----------------------------------------------------------

for (( idWorker=0; idWorker<numberWorkers; idWorker++ )); do
  # Start workers in parallel with one process for each
  worker $idWorker &
done
wait # until all workers are done