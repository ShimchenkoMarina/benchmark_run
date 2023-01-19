#!/bin/bash
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
declare -a arr=("results")
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
    mkdir -p ${raw_dir}/total_energy
    mkdir -p ${raw_dir}/energy_dram
    mkdir -p ${raw_dir}/energy_package
    mkdir -p ${raw_dir}/energy_cpu
    mkdir -p ${raw_dir}/average_power
    mkdir -p ${raw_dir}/memory
    mkdir -p ${raw_dir}/soft_max_capacity
    mkdir -p ${raw_dir}/memory_with_timestamps
    mkdir -p ${raw_dir}/perf
    mkdir -p ${raw_dir}/max_latency
    mkdir -p ${raw_dir}/gc
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
        cat ${input_dir}/${i}.txt | grep "Total Energy:" | cut -d ' ' -f 2 | cut -d ":" -f 2 >> ${raw_dir}/total_energy/${i}.txt
        cat ${input_dir}/${i}.txt | grep "Average Power:" | cut -d ' ' -f 2 | cut -d ":" -f 2 >> ${raw_dir}/average_power/${i}.txt
        cat ${input_dir}/${i}.txt | grep "GC(" | grep -v "System" | cut -d ' ' -f 2,8 | cut -d '(' -f 1 | cut -d ']' -f 1,4 | cut -d '[' -f 2 >> ${raw_dir}/memory_with_timestamps/${i}.txt
	cat ${input_dir}/${i}.txt | grep "GC(" |grep -v "System" | grep -v "Soft Max"| cut -d '-' -f 1| rev | cut -d ")" -f 2| cut -d "M" -f 2 | rev>> ${raw_dir}/memory/${i}.txt
	cat ${input_dir}/${i}.txt | grep "GC(" | cut -d '(' -f 2 | cut -d ')' -f 1 >> ${raw_dir}/gc/${i}.txt
        cat ${input_dir}/${i}.txt | grep "Time:" | cut -d ' ' -f 1 | cut -d ":" -f 2 >> ${raw_dir}/perf/${i}.txt
        cat ${input_dir}/${i}.txt | grep "#\[Max" | cut -d '=' -f 2 | cut -d '','' -f 1 >> ${raw_dir}/max_latency/${i}.txt
        cat ${input_dir}/${i}.txt | grep "metered tail latency" | cut -d " " -f 10  >> ${raw_dir}/max_latency/${i}.txt
        cat ${input_dir}/${i}.txt | grep "Soft Max Capacity" | cut -d ":" -f 2  >> ${raw_dir}/soft_max_capacity/${i}.txt
    done
done
done
sudo bash analyze_results_raw_to_proccessed.sh
