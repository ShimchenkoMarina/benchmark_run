#!/usr/bin/python3
import sys
import os
import re
from functools import reduce

def avg(l):
    return reduce(lambda a, b: a + b, l) / len(l)

def analyze_file(input_dir, output_dir, file_num):
    energy_dram_list = list()
    energy_cpu_list = list()
    energy_pack_list = list()
    gc_rounds_list = list()
    exec_time_list = list()
    recorded_heap_list = list()
    max_heap_list = list()
    s = set()
    max_heap = 0

    with open(os.path.join(input_dir, "energy_cpu", file_num), 'r') as reader:
        #i=0
        for line in reader.readlines():
            if (float(line) > 0):
                energy_cpu_list.append(float(line))
        with open(os.path.join(output_dir, "energy_cpu.txt"), "a+") as writer:
           if (len(energy_cpu_list) > 0):
               writer.write(str(avg(energy_cpu_list)) + '\n')
            #        energy_cpu_list.clear()

    with open(os.path.join(input_dir, "energy_pack", file_num), 'r') as reader:
        #i=0
        for line in reader.readlines():
            if (float(line) > 0):
                energy_pack_list.append(float(line))
        with open(os.path.join(output_dir, "energy_pack.txt"), "a") as writer:
           if (len(energy_pack_list) > 0):
               writer.write(str(avg(energy_pack_list)) + '\n')
            #        energy_pack_list.clear()

    with open(os.path.join(input_dir, "energy_dram", file_num), 'r') as reader:
        #i=0
        for line in reader.readlines():
            if (float(line) > 0):
                energy_dram_list.append(float(line))
        with open(os.path.join(output_dir, "energy_dram.txt"), "a") as writer:
           if (len(energy_dram_list) > 0):
               writer.write(str(avg(energy_dram_list)) + '\n')
            #        energy_dram_list.clear()
    with open(os.path.join(input_dir, "GC_cycles", file_num), 'r') as reader:
        #i=0
        last_cycle = ''
        for line in reader.readlines():
            last_cycle = line
        with open(os.path.join(output_dir, "GC_cycles.txt"), "a") as writer:
            writer.write(last_cycle)

    with open(os.path.join(input_dir, "perf", file_num), 'r') as reader:
        #i=0
        for line in reader.readlines():
            if (float(line) > 0):
                exec_time_list.append(float(line))
        with open(os.path.join(output_dir, "perf.txt"), "a") as writer:
            if (len(exec_time_list) > 0):
                writer.write(str(avg(exec_time_list)) + '\n')

    with open(os.path.join(input_dir, "av_power_cpu", file_num), 'r') as reader:
        energy_time_cpu_list = list()
        av_power_cpu_list = list()
        number_of_runs = 0
        #first N lines represent energy
        #second N lines represent time
        #in theory the total number of lines should be evenly divisible by 2
        #we try to figure average power
        for line in reader.readlines():
            number_of_runs = number_of_runs + 1
            energy_time_cpu_list.append(float(line))
        if ((number_of_runs % 2 == 0) and (number_of_runs != 0)):
            number_of_runs = int(number_of_runs / 2)
            for x in range(number_of_runs - 1):
                if (energy_time_cpu_list[x] > 0):
                    av_power_cpu_list.append(energy_time_cpu_list[x]/energy_time_cpu_list[number_of_runs - 1 + x])
        with open(os.path.join(output_dir, "av_power_cpu.txt"), "a") as writer:
            if (len(av_power_cpu_list) > 0):
                writer.write(str(avg(av_power_cpu_list)) + '\n')
    
    with open(os.path.join(input_dir, "av_power_dram", file_num), 'r') as reader:
        energy_time_dram_list = list()
        av_power_dram_list = list()
        number_of_runs = 0
        #first N lines represent energy
        #second N lines represent time
        #in theory the total number of lines should be evenly divisible by 2
        #we try to figure average power
        for line in reader.readlines():
            number_of_runs = number_of_runs + 1
            energy_time_dram_list.append(float(line))
        if ((number_of_runs % 2 == 0) and (number_of_runs != 0)):
            number_of_runs = int(number_of_runs / 2)
            for x in range(number_of_runs - 1):
                if (energy_time_dram_list[x] > 0):
                    av_power_dram_list.append(energy_time_dram_list[x]/energy_time_dram_list[number_of_runs - 1 + x])
        with open(os.path.join(output_dir, "av_power_dram.txt"), "a") as writer:
            if (len(av_power_dram_list) > 0):
                writer.write(str(avg(av_power_dram_list)) + '\n')
    
    with open(os.path.join(input_dir, "av_power_pack", file_num), 'r') as reader:
        energy_time_pack_list = list()
        av_power_pack_list = list()
        number_of_runs = 0
        #first N lines represent energy
        #second N lines represent time
        #in theory the total number of lines should be evenly divisible by 2
        #we try to figure average power
        for line in reader.readlines():
            number_of_runs = number_of_runs + 1
            energy_time_pack_list.append(float(line))
        if ((number_of_runs % 2 == 0) and (number_of_runs != 0)):
            number_of_runs = int(number_of_runs / 2)
            for x in range(number_of_runs - 1):
                if (energy_time_pack_list[x] > 0):
                    av_power_pack_list.append(energy_time_pack_list[x]/energy_time_pack_list[number_of_runs - 1 + x])
        with open(os.path.join(output_dir, "av_power_pack.txt"), "a") as writer:
            if (len(av_power_pack_list) > 0):
                writer.write(str(avg(av_power_pack_list)) + '\n')
    
    '''with open(os.path.join(input_dir, file_num), 'r') as reader:
        for line in reader.readlines():
            if "starting" in line:
                if len(s) > 0:
                    gc_rounds_list.append(len(s))
                if max_heap > 0:
                    max_heap_list.append(max_heap)
                max_heap = 0
                s.clear()

            if "GC" in line:
                s.add(re.search(r'\((.*?)\)',line).group(1))

            if "->" in line:
                pre_heap = re.search('.* (.*)->', line).group(1)
                pre_heap = re.search('\d*', pre_heap).group(0)
                recorded_heap_list.append(int(pre_heap))
                max_heap = max(max_heap, int(pre_heap))

    if len(gc_rounds_list) > 0:
        with open(os.path.join(output_dir, "gc_rounds.txt"), "a") as writer:
            writer.write(str(avg(gc_rounds_list)) + '\n')
    else:
        with open(os.path.join(output_dir, "gc_rounds.txt"), "a") as writer:
            writer.write('')

    if len(max_heap_list) > 0:
        with open(os.path.join(output_dir, "max_heap.txt"), "a") as writer:
            writer.write(str(avg(max_heap_list)) + '\n')
    else:
        with open(os.path.join(output_dir, "max_heap.txt"), "a") as writer:
            writer.write('')

    if len(recorded_heap_list) > 0:
        with open(os.path.join(output_dir, "average_heap.txt"), "a") as writer:
            writer.write(str(avg(recorded_heap_list)) + '\n')
    else:
        with open(os.path.join(output_dir, "average_heap.txt"), "a") as writer:
            writer.write('')'''

def main():
    if len(sys.argv) != 4:
        print("Usage analyze_file.py input_dir output_dir file_num")
        exit(1)
    analyze_file(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
