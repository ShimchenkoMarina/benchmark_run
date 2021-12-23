#!/usr/bin/python3
import sys
import os
import re
from functools import reduce

GC_cycles_convert = {
                    "zxing": 25,
                    "tradesoap": 15,
                    "graphchi": 25,
                    "jme_def": 25,
                    "biojava": 25,
                    "h2_small": 50,
                    "h2_large": 30,
                    "h2_huge": 10,
                    "avrora": 17,
                    "fop_default": 50,
                    "juthon": 20,
                    "luindex": 30,
                    "lusearch": 20,
                    "pmd": 30,
                    "sunflow": 20,
                    "xalan": 20,
                    "hazelcast": 1,
                    "als": 30,
                    "dec-tree": 40,
                    "chi-square": 60,
                    "gauss-mix": 40,
                    "log-regression": 20,
                    "movie-lens": 20,
                    "naive-bayes": 30,
                    "page-rank": 20,
                    "akka-uct": 24,
                    "fj-kmeans": 30,
                    "reactors": 10,
                    "db-shootout": 16,
                    "neo4j-analytics": 20,
                    "future-genetic": 50,
                    "mnemonics": 16,
                    "par-mnemonics": 16,
                    "rx-scrabble": 80,
                    "scrabble": 50,
                    "dotty": 50,
                    "philosophers": 30,
                    "scala-doku": 20,
                    "scala-kmeans": 50,
                    "scala-stm-bench7": 60,
                    "finagle-chirper": 90,
                    "finagle-http": 12
}

def separate_number_chars(s):
    res = re.split('([-+]?\d+\.\d+)|([-+]?\d+)', s.strip())
    res_f = [r.strip() for r in res if r is not None and r.strip() != '']
    return res_f

def avg(l):
    return reduce(lambda a, b: a + b, l) / len(l)

def analyze_file(input_dir, output_dir, file_num):
    OVERFLOW_CONST = 65536
    energy_dram_list = list()
    energy_cpu_list = list()
    energy_pack_list = list()
    gc_rounds_list = list()
    exec_time_list = list()
    recorded_heap_list = list()
    max_heap_list = list()
    mean_latency_list = list()
    max_latency_list = list()
    s = set()
    max_heap = 0
    
    #We need this if since we collect latency only for some bms    
    if os.path.exists(os.path.join(input_dir, "mean_latency", file_num)):
        with open(os.path.join(input_dir, "mean_latency", file_num), 'r') as reader:
            for line in reader.readlines():
                line = line.replace(",", ".")
                try:
                    float(line)
                    if (float(line) > 0):
                        mean_latency_list.append(float(line))
                    elif float(line) <= 0:
                        mean_latency_list.append(float(line) + OVERFLOW_CONST)
                except:
                    with open(os.path.join("bug_report.txt"), "a") as writer:
                        writer.write("Check numbers in (did not convert) : " +  input_dir + file_num + '\n')
        with open(os.path.join(output_dir, "mean_latency.txt"), "a+") as writer:
            if (len(mean_latency_list) > 0):
                writer.write(str(avg(mean_latency_list)) + '\n')
            else:
                with open(os.path.join("list_of_empty_files.txt"), "a") as writer:
                    writer.write(output_dir + file_num + '\n')
    
    #We need this if since we collect latency only for some bms    
    if os.path.exists(os.path.join(input_dir, "max_latency", file_num)):
        with open(os.path.join(input_dir, "max_latency", file_num), 'r') as reader:
            for line in reader.readlines():
                line = line.replace(",", ".")
                try:
                    float(line)
                    if (float(line) > 0):
                        max_latency_list.append(float(line))
                    elif float(line) <= 0:
                        max_latency_list.append(float(line) + OVERFLOW_CONST)
                except:
                    with open(os.path.join("bug_report.txt"), "a") as writer:
                        writer.write("Check numbers in (did not convert) : " +  input_dir + file_num + '\n')

        with open(os.path.join(output_dir, "max_latency.txt"), "a+") as writer:
           if (len(max_latency_list) > 0):
               writer.write(str(avg(max_latency_list)) + '\n')

    with open(os.path.join(input_dir, "energy_cpu", file_num), 'r') as reader:
        for line in reader.readlines():
            line =line.replace(",", ".")
            try:
                float(line)
                if (float(line) > 0):
                    energy_cpu_list.append(float(line))
                elif float(line) <= 0:
                    energy_cpu_list.append(float(line) + OVERFLOW_CONST)
            except:
                with open(os.path.join("bug_report.txt"), "a") as writer:
                    writer.write("Check numbers in (did not convert) : " +  input_dir + file_num + '\n')
    with open(os.path.join(output_dir, "energy_cpu.txt"), "a+") as writer:
        if (len(energy_cpu_list) > 0):
            writer.write(str(avg(energy_cpu_list)) + '\n')

    with open(os.path.join(input_dir, "energy_pack", file_num), 'r') as reader:
        for line in reader.readlines():
            line =line.replace(",", ".")
            try:
                float(line)
                if (float(line) > 0):
                    energy_pack_list.append(float(line))
                elif float(line) <= 0:
                    energy_pack_list.append(float(line) + OVERFLOW_CONST)
            except:
                with open(os.path.join("bug_report.txt"), "a") as writer:
                    writer.write("Check numbers in (did not convert) : " +  input_dir + file_num + " --> " + line + '\n')
    with open(os.path.join(output_dir, "energy_pack.txt"), "a") as writer:
        if (len(energy_pack_list) > 0):
            writer.write(str(avg(energy_pack_list)) + '\n')

    with open(os.path.join(input_dir, "energy_dram", file_num), 'r') as reader:
        for line in reader.readlines():
            line =line.replace(",", ".")
            try:
                float(line)
                if float(line) > 0:
                    energy_dram_list.append(float(line))
                elif float(line) <= 0:
                    energy_dram_list.append(float(line) + OVERFLOW_CONST)
            except:
                with open(os.path.join("bug_report.txt"), "a") as writer:
                    writer.write("Check numbers in (did not convert to float) : " +  input_dir + file_num + " --> " + line + '\n')
        with open(os.path.join(output_dir, "energy_dram.txt"), "a") as writer:
           if (len(energy_dram_list) > 0):
               writer.write(str(avg(energy_dram_list)) + '\n')

    with open(os.path.join(output_dir, "energy_pack_dram.txt"), "a") as writer:
        if (len(energy_dram_list) > 0) and len(energy_pack_list) > 0:
            writer.write(str(avg(energy_dram_list) + avg(energy_pack_list)) + '\n')
    
    last_cycle = ''
    run = 1
    with open(os.path.join(input_dir, "GC_cycles", file_num), 'r') as reader:
        for line in reader.readlines():
            last_cycle = line
    last_cycle =last_cycle.replace(",", ".")
    for (bm, runs) in GC_cycles_convert.items():
        if (bm in input_dir):
            run = runs
            break
    last_cycle = last_cycle.replace(",", ".")
    try:
        if float(last_cycle)/run < 2:
            with open(os.path.join("bug_report.txt"), "a") as writer:
                writer.write("Report: needs a smaller heap size: " +  input_dir + '\n')
        with open(os.path.join(output_dir, "GC_cycles.txt"), "a") as writer:
            writer.write(str(float(last_cycle)/run) + '\n')
    except:
        with open(os.path.join("bug_report.txt"), "a") as writer:
            writer.write("Check numbers in (did not convert) : " +  input_dir +" " + file_num + " --> " + last_cycle + '\n')

    with open(os.path.join(input_dir, "perf", file_num), 'r') as reader:
        #i=0
        for line in reader.readlines():
            line =line.replace(",", ".")
            if line.strip() and line  not in ['\n', '\r\n']:
                line_array = separate_number_chars(line)
                for subline in line_array:
                    try:
                        float(subline)
                        if float(subline) > 0:
                            exec_time_list.append(float(subline))
                    except:
                        with open(os.path.join("bug_report.txt"), "a") as writer:
                            writer.write("Check numbers in (did not convert) : " +  input_dir +" " + file_num + " --> " + subline + '\n')
                        

    with open(os.path.join(output_dir, "perf.txt"), "a") as writer:
        if (len(exec_time_list) > 0):
            writer.write(str(avg(exec_time_list)) + '\n')
        else:
            with open(os.path.join("bug_report.txt"), "a") as writer:
                writer.write("No time reported in " +  input_dir + file_num + '\n')
            

    av_power_cpu_list = list()
    av_power_dram_list = list()
    av_power_pack_list = list()
    if len(exec_time_list) == len(energy_cpu_list):
        for x in range(len(exec_time_list)):
            if (energy_cpu_list[x] > 0):
                av_power_cpu_list.append(energy_cpu_list[x]/exec_time_list[x] * 1000)
            else:
                av_power_cpu_list.append((energy_cpu_list[x] + OVERFLOW_CONST)/exec_time_list[x] * 1000)
        with open(os.path.join(output_dir, "watts_cpu.txt"), "a") as writer:
            if (len(av_power_cpu_list) > 0):
                writer.write(str(avg(av_power_cpu_list)) + '\n')
    else:
        with open(os.path.join("bug_report.txt"), "a") as writer:
            writer.write("Watts_cpu can not be calculated, length of arrays is not the same : " +  input_dir +"/" + file_num +'\n')
    
    if len(exec_time_list) == len(energy_dram_list):
        for x in range(len(exec_time_list)):
            if (energy_dram_list[x] > 0):
                av_power_dram_list.append(energy_dram_list[x]/exec_time_list[x] * 1000)
            else:
                av_power_dram_list.append((energy_dram_list[x] + OVERFLOW_CONST)/exec_time_list[x] * 1000)
        with open(os.path.join(output_dir, "watts_dram.txt"), "a") as writer:
            if (len(av_power_dram_list) > 0):
                writer.write(str(avg(av_power_dram_list)) + '\n')
    else:
        with open(os.path.join("bug_report.txt"), "a") as writer:
            writer.write("Watts_dram can not be calculated, length of arrays is not the same : " +  input_dir +"/" + file_num +'\n')
    
    if len(exec_time_list) == len(energy_pack_list):
        for x in range(len(exec_time_list)):
            if (energy_pack_list[x] > 0):
                av_power_pack_list.append(energy_pack_list[x]/exec_time_list[x] * 1000)
            else:
                av_power_pack_list.append((energy_pack_list[x] + OVERFLOW_CONST)/exec_time_list[x] * 1000)
        with open(os.path.join(output_dir, "watts_pack.txt"), "a") as writer:
            if (len(av_power_pack_list) > 0):
                writer.write(str(avg(av_power_pack_list)) + '\n')
    else:
        with open(os.path.join("bug_report.txt"), "a") as writer:
            writer.write("Watts_pack can not be calculated, length of arrays is not the same : " +  input_dir +"/" + file_num +'\n')

def main():
    if len(sys.argv) == 4:
        analyze_file(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 2:#for parallel
        input_dir = sys.argv[1].split(" ")[0] 
        output_dir = sys.argv[1].split(" ")[1]
        file_name = sys.argv[1].split(" ")[2]
        analyze_file(input_dir, output_dir, file_name)
    else:
        for args in sys.argv[1:]:
            input_dir = args.split(" ")[0] 
            output_dir = args.split(" ")[1]
            file_name = args.split(" ")[2]
            analyze_file(input_dir, output_dir, file_name)
            

if __name__ == "__main__":
    main()
