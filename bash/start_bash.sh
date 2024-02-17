#!/bin/bash

number_processes=5

#number_gpu_elements=3
display_list=(
":0"
":1"
":2"
)

gpu_list=(
1
0
2    
)

number_gpu_elements=${#display_list[@]}

loop_counter=0
while [  $loop_counter -lt $number_processes ]; do
    echo The counter is $loop_counter

    # Set GPU properties
    idx_gpu=$(($loop_counter % $number_gpu_elements))
    display=${display_list[$idx_gpu]}
    gpu=${gpu_list[$idx_gpu]}

    echo Display $display
    echo GPU $gpu
    export DISPLAY=$display
    export CUDA_VISIBLE_DEVICES=$gpu

    # Start application
    ../application/build/demo config_${loop_counter}.toml &> log/log_${loop_counter}.txt &
    loop_counter=$((loop_counter+1))
done

# grep -oh 'config_.*.toml' *