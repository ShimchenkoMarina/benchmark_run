#!/bin/bash
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
declare -a arr=("results" "results_NUMA" "results_features")
for i in "${arr[@]}"
do
COMMIT=$i


for dir in $(find $COMMIT/ -mindepth 2 -maxdepth 3 -type d -links 2); do
    cd ${__dir}
    sudo rm -rf ${__dir}/bug_report.txt
    input_dir=$(realpath $dir/.)
    o1=raw_dir/"${dir}"
    o2=processed_results/"${dir}"
    sudo rm -rf $o2
    sudo mkdir -p $o2

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
             sudo rm -rf ${raw_dir}/${i}.txt
        else
             python3 ${__dir}/analyze_file.py ${raw_dir} ${output_dir} ${i}.txt
	     for file in $(find ${output_dir}/ -empty); do
		echo "$file in the last stage is Empty!"
		sudo rm -rf file
		done
	fi    
    done
done
done
#python3 analyze.py
