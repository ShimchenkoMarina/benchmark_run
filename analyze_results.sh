#!/bin/bash
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
declare -a arr=("results" "results_NUMA")
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
    mkdir -p ${raw_dir}/energy_dram
    mkdir -p ${raw_dir}/energy_cpu
    mkdir -p ${raw_dir}/energy_pack
    mkdir -p ${raw_dir}/GC_cycles
    mkdir -p ${raw_dir}/perf
    mkdir -p ${raw_dir}/mean_latency
    mkdir -p ${raw_dir}/max_latency
    for i in $(seq 1 $count_files); do
        if [ ! -s ${input_dir}/${i}.txt ]
        then
            sudo rm -rf ${input_dir}/${i}.txt
            continue
        fi
        python3 ${__dir}/uncomplete.py ${input_dir} ${i}.txt
        if [ $? != 0 ];
        then
            echo "${input_dir}/${i}.txt has exception!"
            #sudo rm -rf ${input_dir}/${i}.txt Keep it for checking an exception
            continue
        fi
        python3 ${__dir}/process_file.py ${input_dir} ${raw_dir} ${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Power consumption of dram s" | cut -d ' ' -f 6 >> ${raw_dir}/energy_dram/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Power consumption of cpu s" | cut -d ' ' -f 6 >> ${raw_dir}/energy_cpu/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Power consumption of package s" | cut -d ' ' -f 6 >> ${raw_dir}/energy_pack/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "GC(" | cut -d '(' -f 2| cut -d ')' -f 1 >> ${raw_dir}/GC_cycles/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Execution time" | cut -d ' ' -f 3 >> ${raw_dir}/perf/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Duration" | cut -d ' ' -f 2 >> ${raw_dir}/perf/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "#\[Mean" | cut -d '=' -f 2 | cut -d '','' -f 1 >> ${raw_dir}/mean_latency/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "completed (" | cut -d '(' -f 3 | cut -d ')' -f 1 | cut -d ' ' -f 1 >> ${raw_dir}/perf/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "#\[Max" | cut -d '=' -f 2 | cut -d '','' -f 1 >> ${raw_dir}/max_latency/${i}.txt
        if [ ! -s ${raw_dir}/mean_latency/${i}.txt ]
        then
            cat ${raw_dir}/${i}.txt | grep "Pause" | grep "ms" >> ${raw_dir}/mean_latency/${i}.txt
            #sudo rm -rf ${raw_dir}/mean_latency/${i}.txt
        fi
        if [ ! -s ${raw_dir}/max_latency/${i}.txt ]
        then
             sudo rm -rf ${raw_dir}/max_latency/${i}.txt
	fi
    done
done
done
sudo bash analyze_results_raw_to_proccessed.sh 
sudo bash analyze_results_likwid.sh
