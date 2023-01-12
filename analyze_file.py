#!/usr/bin/python3
import sys
import os
import re
from functools import reduce
def do_nothing():
    return

def avg(l):
    return reduce(lambda a, b: a + b, l) / len(l)

def sum(l):
    return reduce(lambda a, b: a + b, l)

def analyze_file(input_dir, output_dir, file_num):
    energy_list = list()
    power_list = []
    gc_rounds_list = list()
    perf_list = list()
    stalls_time_list = list()
    pause_time_list = list()

    #for i in range(1, int(file_num)):
    with open(os.path.join(input_dir, "total_energy", str(file_num) + ".txt"), 'r') as reader:
            for line in reader.readlines():
                line =line.replace(",", ".").strip()
                try:
                    float(line)
                    energy_list.append(float(line))
                except:
                    with open(os.path.join("bug_report.txt"), "a") as writer:
                        writer.write("Check numbers in (did not convert) : " +  input_dir + file_num + '\n')
    with open(os.path.join(output_dir, "total_energy.txt"), "a+") as writer:
        if (len(energy_list) > 0):
            writer.write(str(avg(energy_list)) + '\n')

    #for i in range(1, int(file_num)):
    with open(os.path.join(input_dir, "average_power", str(file_num) + ".txt"), 'r') as reader:
            for line in reader.readlines():
                line =line.replace(",", ".").strip()
                try:
                    float(line)
                    power_list.append(float(line))
                except:
                    with open(os.path.join("bug_report.txt"), "a") as writer:
                        writer.write("Check numbers in (did not convert) : " +  input_dir + file_num + '\n')
    with open(os.path.join(output_dir, "average_power.txt"), "a+") as writer:
        if (len(power_list) > 0):
            writer.write(str(avg(power_list)) + '\n')

    #for i in range(1, int(file_num)):
    with open(os.path.join(input_dir, "perf", str(file_num) + ".txt"), 'r') as reader:
            for line in reader.readlines():
                line =line.replace(",", ".").strip()
                try:
                    float(line)
                    perf_list.append(float(line))
                except:
                    with open(os.path.join("bug_report.txt"), "a") as writer:
                        writer.write("Check numbers in (did not convert) : " +  input_dir + file_num + '\n')
    with open(os.path.join(output_dir, "perf.txt"), "a+") as writer:
        if (len(perf_list) > 0):
            writer.write(str(avg(perf_list)) + '\n')

    last_cycle = ''
    run = 1
    memory_list = []
    with open(os.path.join(input_dir, "memory", file_num + ".txt"), 'r') as reader:
        for line in reader.readlines():
            last_cycle = line
            last_cycle =last_cycle.replace(",", ".")
            try:
                float(last_cycle)
                memory_list.append(float(line))
            except:
                do_nothing()
    with open(os.path.join(output_dir, "memory.txt"), "a+") as writer:
        if (len(memory_list) > 0):
            writer.write(str(avg(memory_list)) + '\n')


    '''with open(os.path.join(input_dir, "stalls", file_num + ".txt"), 'r') as reader:
        for line in reader.readlines():
            line =line.replace(",", ".")
            if line.strip() and line  not in ['\n', '\r\n']:
                line_array = separate_number_chars(line)
                for subline in line_array:
                    try:
                        float(subline)
                        if float(subline) > 0:
                            stalls_time_list.append(float(subline))
                    except:
                        with open(os.path.join("bug_report.txt"), "a") as writer:
                            writer.write("Check numbers in (did not convert) : " +  input_dir +" " + file_num + " --> " + subline + '\n')


    with open(os.path.join(output_dir, "stalls.txt"), "a") as writer:
        if (len(stalls_time_list) > 0):
            writer.write(str(sum(stalls_time_list)) + '\n')
        else:
            writer.write("0" + '\n')
    '''
    with open(os.path.join(input_dir, "max_latency", file_num + ".txt"), 'r') as reader:
        for line in reader.readlines():
            if "ms" not in line:
                continue
            line =line.replace(",", ".")
            if line.strip() and line  not in ['\n', '\r\n']:
                line_array = separate_number_chars(line)
                for subline in line_array:
                    try:
                        float(subline)
                        if float(subline) > 0:
                            pause_time_list.append(float(subline))
                    except:
                        pass


    with open(os.path.join(output_dir, "max_latency.txt"), "a") as writer:
        if (len(pause_time_list) > 0):
            writer.write(str(max(pause_time_list)) + '\n')

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
