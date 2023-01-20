#!/bin/bash
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
declare -a arr=("test")
for i in "${arr[@]}"
do
COMMIT=$i
echo $COMMIT
for dir in $(find $COMMIT/ -mindepth 2 -maxdepth 3 -type d -links 2); do
    cd ${__dir}
    input_dir=$(realpath $dir/.)
    #o1=raw_dir/"${dir}_s${soc}"
    o1=raw_dir/"${dir}"
    rm -rf $o1
    mkdir -p $o1

    raw_dir=$(realpath $o1/.)

    count_files=$(expr $(ls -l $input_dir | grep -v ^l | wc -l) - 1)
    if [[ $count_files -eq 0 ]]; then # Do we even have data?
        continue
    fi
    mkdir -p ${raw_dir}/energy
    mkdir -p ${raw_dir}/power
    mkdir -p ${raw_dir}/GC_cycles
    mkdir -p ${raw_dir}/perf
    mkdir -p ${raw_dir}/stalls
    mkdir -p ${raw_dir}/max_pause
    mkdir -p ${raw_dir}/latency
    mkdir -p ${raw_dir}/predicted_workers
    mkdir -p ${raw_dir}/cpu_utilization
    #mkdir -p ${raw_dir}/allocation_rate
    #mkdir -p ${raw_dir}/mean_latency
    for i in $(seq 1 $count_files); do
        if [ ! -s ${input_dir}/${i}.txt ]
        then
            sudo rm -rf ${input_dir}/${i}.txt
            continue
        fi
        #python3 ${__dir}/uncomplete.py ${input_dir} ${i}.txt
        if [ $? != 0 ];
        then
            echo "${input_dir}/${i}.txt has exception!"
            #sudo rm -rf ${input_dir}/${i}.txt Keep it for checking an exception
            continue
        fi
        #python3 ${__dir}/process_file.py ${input_dir} ${raw_dir} ${i}.txt No need to cut anything off at least for spec and hazelcast
	echo $dir
        #cat ${input_dir}/${i}.txt | grep "Workers predicted:" | cut -d ':' -f 2 >> ${raw_dir}/predicted_workers/${i}.txt
        cat ${input_dir}/${i}.txt | grep "Total Energy:" | cut -d ' ' -f 2 | cut -d ":" -f 2 >> ${raw_dir}/energy/${i}.txt
        cat ${input_dir}/${i}.txt | grep "Average Power:" | cut -d ' ' -f 2 | cut -d ":" -f 2 >> ${raw_dir}/power/${i}.txt
        cat ${input_dir}/${i}.txt | grep "GC(" | cut -d '(' -f 2| cut -d ')' -f 1 >> ${raw_dir}/GC_cycles/${i}.txt
        cat ${input_dir}/${i}.txt | grep "Time:" | cut -d ' ' -f 1 | cut -d ":" -f 2 >> ${raw_dir}/perf/${i}.txt
        cat  ${input_dir}/${i}.txt | grep "Allocation Stall (" | cut -d ")" -f 2  >> ${raw_dir}/stalls/${i}.txt
        cat ${input_dir}/${i}.txt | grep "#\[Max" | cut -d '=' -f 2 | cut -d "," -f 1 >> ${raw_dir}/latency/${i}.txt
        cat ${input_dir}/${i}.txt | grep "Pause" | grep "[0-9]ms" |  cut -d ' ' -f 13 >> ${raw_dir}/max_pause/${i}.txt
        cat ${input_dir}/${i}.txt | grep "metered tail latency" | cut -d ' ' -f 16 >> ${raw_dir}/latency/${i}.txt
        cat ${input_dir}/${i}.txt | grep "CPU utilization:" | cut -d ' ' -f 3 >> ${raw_dir}/cpu_utilization/${i}.txt
        #if [[ $input_dir == *"allocation_rate"*  ]]; then
        #      python3 ${__dir}/analyze_allocation_rate.py ${input_dir} ${i} ${raw_dir}
        #fi

    done
done
done
#sudo bash analyze_results_raw_to_proccessed.sh
