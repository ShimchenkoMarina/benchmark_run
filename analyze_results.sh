#!/bin/bash
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMIT="results"
SOCKETS=2

for dir in $(find $COMMIT/ -mindepth 2 -maxdepth 3 -type d -links 2); do
    echo $dir
    cd ${__dir}
    input_dir=$(realpath $dir/.)
    for (( soc=0; soc<$SOCKETS; soc++ )); do
    o1=raw_dir/"${dir}_s${soc}"
    o2=processed_results/"${dir}_s${soc}"
    rm -rf $o1
    mkdir -p $o1
    rm -rf $o2
    mkdir -p $o2

    raw_dir=$(realpath $o1/.)
    output_dir=$(realpath $o2/.)

    count_files=$(expr $(ls -l $input_dir | grep -v ^l | wc -l) - 1)
    if [[ $count_files -eq 0 ]]; then # Do we even have data?
        continue
    fi
    mkdir -p ${raw_dir}/energy_dram
    mkdir -p ${raw_dir}/av_power_dram
    mkdir -p ${raw_dir}/av_power_cpu
    mkdir -p ${raw_dir}/av_power_pack
    mkdir -p ${raw_dir}/energy_cpu
    mkdir -p ${raw_dir}/energy_pack
    mkdir -p ${raw_dir}/GC_cycles
    mkdir -p ${raw_dir}/perf
    energy_dram=0
    energy_cpu=0
    energy_pack=0
    time=0
    for i in $(seq 1 $count_files); do
        python3 ${__dir}/process_file.py ${input_dir} ${raw_dir} ${i}.txt
        rm -f ${raw_dir}/energy/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Power consumption of dram s${soc}" | cut -d ' ' -f 6 >> ${raw_dir}/energy_dram/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Power consumption of dram s${soc}" | cut -d ' ' -f 6 >> ${raw_dir}/av_power_dram/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Power consumption of cpu s${soc}" | cut -d ' ' -f 6 >> ${raw_dir}/energy_cpu/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Power consumption of cpu s${soc}" | cut -d ' ' -f 6 >> ${raw_dir}/av_power_cpu/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Power consumption of package s${soc}" | cut -d ' ' -f 6 >> ${raw_dir}/energy_pack/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Power consumption of package s${soc}" | cut -d ' ' -f 6 >> ${raw_dir}/av_power_pack/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "GC(" | cut -d ' ' -f 2| cut -d '(' -f 2| cut -d ')' -f 1 >> ${raw_dir}/GC_cycles/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Execution time" | cut -d ' ' -f 3 >> ${raw_dir}/perf/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Execution time" | cut -d ' ' -f 3 >> ${raw_dir}/av_power_cpu/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Execution time" | cut -d ' ' -f 3 >> ${raw_dir}/av_power_dram/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Execution time" | cut -d ' ' -f 3 >> ${raw_dir}/av_power_pack/${i}.txt
    done
    done
done

for dir in $(find $COMMIT/ -mindepth 2 -maxdepth 3 -type d -links 2); do
    cd ${__dir}
    input_dir=$(realpath $dir/.)
    for (( soc=0; soc<$SOCKETS; soc++ )); do
    	o1=raw_dir/"${dir}_s${soc}"
   	o2=processed_results/"${dir}_s${soc}"

    	raw_dir=$(realpath $o1/.)
    	output_dir=$(realpath $o2/.)
    	count_files=$(expr $(ls -l $input_dir | grep -v ^l | wc -l) - 1)
    	if [[ $count_files -eq 0 ]]; then # Do we even have raw data?
        	continue
    	fi

    	for i in $(seq 1 $count_files); do
        	if [ ! -s ${raw_dir}/${i}.txt ]
        	then
             		echo "${raw_dir}/${i}.txt is Empty!"
             		rm -rf ${raw_dir}/${i}.txt
        	else 
             	python3 ${__dir}/analyze_file.py ${raw_dir} ${output_dir} ${i}.txt
        	fi    
        	#python3 ${__dir}/analyze_file.py ${raw_dir} ${output_dir} ${i}.txt
        	#python3 ${__dir}/analyze_file.py ${raw_dir} ${output_dir} ${i}.txt
    	done
    done
done
#python3 analyze.py
