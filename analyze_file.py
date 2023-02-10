#!/usr/bin/python3
import sys
import os
import re
from functools import reduce
import numpy as np
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

def sum(l):
    return reduce(lambda a, b: a + b, l)

def reject_outliers(data, m = 2.):
        d = np.abs(data - np.median(data))
        mdev = np.median(d)
        s = d/mdev if mdev else 0.
        return data[s<m]

def analyze_file(input_dir, output_dir, file_num):
    energy_list = list()
    power_list = []
    gc_rounds_list = list()
    perf_list = list()
    stalls_time_list = list()
    pause_time_list = list()

    #for i in range(1, int(file_num)):
    with open(os.path.join(input_dir, "energy", str(file_num) + ".txt"), 'r') as reader:
            for line in reader.readlines():
                line =line.replace(",", ".").strip()
                try:
                    float(line)
                    energy_list.append(float(line))
                except:
                    with open(os.path.join("bug_report.txt"), "a") as writer:
                        writer.write("Check numbers in (did not convert) : " +  input_dir + file_num + '\n')
    with open(os.path.join(output_dir, "energy.txt"), "a+") as writer:
        if (len(energy_list) > 0):
            writer.write(str(avg(energy_list)) + '\n')

    #for i in range(1, int(file_num)):
    '''with open(os.path.join(input_dir, "power", str(file_num) + ".txt"), 'r') as reader:
            for line in reader.readlines():
                line =line.replace(",", ".").strip()
                try:
                    float(line)
                    power_list.append(float(line))
                except:
                    with open(os.path.join("bug_report.txt"), "a") as writer:
                        writer.write("Check numbers in (did not convert) : " +  input_dir + file_num + '\n')
    with open(os.path.join(output_dir, "power.txt"), "a+") as writer:
        if (len(power_list) > 0):
            writer.write(str(avg(power_list)) + '\n')
    '''
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
        if (len(perf_list) == 1):
            writer.write(str(avg(perf_list)) + '\n')
        elif (len(perf_list) > 1):
            writer.write(str(avg(reject_outliers(np.array(perf_list)))) + '\n')

    last_cycle = ''
    run = 1
    with open(os.path.join(input_dir, "GC_cycles", file_num + ".txt"), 'r') as reader:
        for line in reader.readlines():
            last_cycle = line
    last_cycle =last_cycle.replace(",", ".")
    #for (bm, runs) in GC_cycles_convert.items():
    #    if (bm in input_dir):
    #        run = runs
    #        break
    #last_cycle = last_cycle.replace(",", ".")
    try:
        float(last_cycle)
        with open(os.path.join(output_dir, "GC_cycles.txt"), "a") as writer:
            writer.write(str(float(last_cycle)) + '\n')
    except:
        if last_cycle == "":
            with open(os.path.join(output_dir, "GC_cycles.txt"), "a") as writer:
                writer.write("0" + '\n')
        else:
            with open(os.path.join("bug_report.txt"), "a") as writer:
                writer.write("Check numbers in (did not convert) : " +  input_dir +" " + file_num + " --> " + last_cycle + '\n')

    with open(os.path.join(input_dir, "cpu_utilization", file_num + ".txt"), 'r') as reader:
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


    with open(os.path.join(output_dir, "cpu_utilization.txt"), "a") as writer:
        if (len(stalls_time_list) > 0):
            writer.write(str(avg(stalls_time_list)) + '\n')
        #else:
        #    writer.write("0" + '\n')

    with open(os.path.join(input_dir, "latency", file_num + ".txt"), 'r') as reader:
        for line in reader.readlines():
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

    #print(pause_time_list)
    #print(np.std(pause_time_list))
    #print(np.std(pause_time_list/np.mean(pause_time_list)))
    #print(reject_outliers(np.array(pause_time_list)))
    #print(np.std(reject_outliers(np.array(pause_time_list))))
    #print(np.std(reject_outliers(np.array(pause_time_list)))/np.mean(reject_outliers(np.array(pause_time_list))))
    with open(os.path.join(output_dir, "latency.txt"), "a") as writer:
        if (len(pause_time_list) > 1):
            if np.std(reject_outliers(np.array(pause_time_list)))/np.mean(reject_outliers(np.array(pause_time_list))) < 0.2:
                writer.write(str(avg(reject_outliers(np.array(pause_time_list)))) + '\n')
        if (len(pause_time_list) == 1):
            writer.write(str(avg(np.array(pause_time_list))) + "\n")

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
