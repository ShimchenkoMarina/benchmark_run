#!/bin/bash
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
declare -a arr=("results_likwid" "results_likwid_NUMA")
for i in "${arr[@]}"
do 
COMMIT=$i
rm -rf $COMMIT/../raw_dir/results_likwid/
for dir in $(find $COMMIT/ -mindepth 2 -maxdepth 3 -type d -links 2); do
    cd ${__dir}
    input_dir=$(realpath $dir/.)
    o1=raw_dir/"${dir}"/../features
    #rm -rf $o1
    mkdir -p $o1

    raw_dir=$(realpath $o1/.)

    count_files=$(expr $(ls -l $input_dir | grep -v ^l | wc -l) - 1)
    if [[ $count_files -eq 0 ]]; then # Do we even have data?
        continue
    fi
    for i in $(seq 1 $count_files); do
        if [ ! -s ${input_dir}/${i}.txt ]
        then
            sudo rm -rf ${input_dir}/${i}.txt
            continue
        fi
        cat ${dir}/${i}.txt | grep '''Branch rate STAT''' | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep '''Branch misprediction rate STAT''' | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Branch misprediction ratio STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Instructions per branch STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Instructions per branch STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Total execution stalls PMC3" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Stalls caused by L1D misses" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Stalls caused by L2 misses" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Execution stall rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Stalls caused by L1D misses rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Stalls caused by L2 misses rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Load to store ratio" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Energy PP0" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Power PP0" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Energy DRAM" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Power DRAM" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Energy [J]" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Power [W]" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I request rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I miss rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I miss ratio" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I stalls" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I stall rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I queue full stalls" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I queue full stall rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L2 request rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L2 miss rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L2 miss ratio" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L3 request rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L3 miss rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L3 miss ratio" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Memory read bandwidth" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Memory read data volume" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Memory write bandwidth" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Memory write data volume" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Memory bandwidth" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Memory data volume" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "CPI" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "MFLOP/s" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "AVX" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Packed" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Scalar" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Operational intensity" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 DTLB load misses" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 DTLB load miss rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 DTLB load miss duration" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 DTLB store misses" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 DTLB store miss rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 DTLB store miss duration" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 ITLB misses" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 ITLB miss rate" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 ITLB miss duration" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        python3 ${__dir}/clean_file_likwid.py ${raw_dir} ${i}.txt
    done
done
done
