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
        cat ${dir}/${i}.txt | grep "Total execution stalls PMC3" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Stalls caused by L1D misses" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Stalls caused by L2 misses" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Execution stall rate" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Stalls caused by L1D misses rate" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Stalls caused by L2 misses rate" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Load to store ratio" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Energy PP0 [J] STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Power PP0 [W] STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Energy DRAM [J] STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Power DRAM [W] STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Energy [J] STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Power [W] STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I request rate" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I miss rate" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I miss ratio" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I stalls" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I stall rate" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I queue full stalls" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1I queue full stall rate" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L2 request rate STAT" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L2 miss rate STAT" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L2 miss ratio STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L3 request rate STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L3 miss rate STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L3 miss ratio STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Memory read bandwidth [MBytes/s] STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Memory read data volume" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Memory write bandwidth" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Memory write data volume" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Memory bandwidth" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Memory data volume" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "CPI" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "MFLOP/s" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "AVX" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Packed" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Scalar" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "Operational intensity" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 DTLB load misses" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 DTLB load miss rate" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 DTLB load miss duration" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 DTLB store misses" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 DTLB store miss rate" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 DTLB store miss duration" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 ITLB misses" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 ITLB miss rate" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        cat ${dir}/${i}.txt | grep "L1 ITLB miss duration" | grep "STAT" | cut -d '|' -f 2,3 >> ${raw_dir}/${i}.txt
        python3 ${__dir}/clean_file_likwid.py ${raw_dir} ${i}.txt
    done
done
done
