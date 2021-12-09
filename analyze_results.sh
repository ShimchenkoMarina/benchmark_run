#!/bin/bash
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMIT="results"
SOCKETS=1

for dir in $(find $COMMIT/ -mindepth 2 -maxdepth 3 -type d -links 2); do
    cd ${__dir}
    input_dir=$(realpath $dir/.)
    for (( soc=0; soc<$SOCKETS; soc++ )); do
    o1=raw_dir/"${dir}_s${soc}"
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
        #rm -f ${raw_dir}/energy/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Power consumption of dram s${soc}" | cut -d ' ' -f 6 >> ${raw_dir}/energy_dram/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Power consumption of cpu s${soc}" | cut -d ' ' -f 6 >> ${raw_dir}/energy_cpu/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Power consumption of package s${soc}" | cut -d ' ' -f 6 >> ${raw_dir}/energy_pack/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "GC(" | cut -d '(' -f 2| cut -d ')' -f 1 >> ${raw_dir}/GC_cycles/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Execution time" | cut -d ' ' -f 3 >> ${raw_dir}/perf/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "Duration" | cut -d ' ' -f 2 >> ${raw_dir}/perf/${i}.txt
        cat ${raw_dir}/${i}.txt | grep "#\[Mean" | cut -d '=' -f 2 | cut -d '','' -f 1 >> ${raw_dir}/mean_latency/${i}.txt
       	cat ${raw_dir}/${i}.txt | grep "completed (" | cut -d '(' -f 3 | cut -d ')' -f 1 | cut -d ' ' -f 1 >> ${raw_dir}/perf/${i}.txt
	if [ ! -s ${raw_dir}/mean_latency/${i}.txt ]
       	then
             sudo rm -rf ${raw_dir}/mean_latency/${i}.txt
	fi
        cat ${raw_dir}/${i}.txt | grep "#\[Max" | cut -d '=' -f 2 | cut -d '','' -f 1 >> ${raw_dir}/max_latency/${i}.txt
       	if [ ! -s ${raw_dir}/max_latency/${i}.txt ]
       	then
             sudo rm -rf ${raw_dir}/max_latency/${i}.txt
	fi
    done
    done
done
#sudo bash analyze_results_raw_to_proccessed.sh 
'''for dir in $(find $COMMIT/ -mindepth 2 -maxdepth 3 -type d -links 2); do
    cd ${__dir}
    sudo rm -rf ${__dir}/bug_report.txt
    input_dir=$(realpath $dir/.)
    for (( soc=0; soc<$SOCKETS; soc++ )); do
    	o1=raw_dir/"${dir}_s${soc}"
   	o2=processed_results/"${dir}_s${soc}"
	sudo rm -rf ${output_dir}
    	sudo mkdir -p ${output_dir}

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
			echo ${raw_dir} ${output_dir} ${i}.txt >> input_params_analyze_file.txt
			#for file in $(find ${output_dir}/ -empty); do
			#		echo "$file in the last stage is Empty!"
			#	sudo rm -rf file
			#done
		fi    
    	done
    done
done
cat input_params_analyze_file.txt | parallel -X -q sudo python3 ${__dir}/analyze_file.py {}'''
#python3 analyze.py
