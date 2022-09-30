#!/usr/bin/python3
import sys
import os
import re
from functools import reduce

BMs = ["finagle-http", "finagle-chirper", "spec", "hazelcast"]
def separate_number_chars(s):
    res = re.split('([-+]?\d+\.\d+)|([-+]?\d+)', s.strip())
    res_f = [r.strip() for r in res if r is not None and r.strip() != '']
    #print(res_f)
    return res_f

def avg(l):
    return reduce(lambda a, b: a + b, l) / len(l)

def sum(l):
    return reduce(lambda a, b: a + b, l)

def which_BM(input_dir):
    BM = input_dir.split("/")[6][:-16]
    BM_conf = input_dir.split("/")[7]
    return BM, BM_conf

def analyze_file(input_dir, file_name):
    allocation_rate_global_avg = []
    allocation_rate_global_dynamic = []
    allocation_rate_global_max = []
    #for i in range(1, int(file_num)):
    with open(os.path.join(input_dir, file_name + ".txt"), 'r') as reader:
        for line in reader.readlines():
            if "Allocation Rate" in line:
                allocation_rate_global_avg.append(separate_number_chars(line)[14])
                allocation_rate_global_dynamic.append(separate_number_chars(line)[5])
                allocation_rate_global_max.append(separate_number_chars(line)[16])

    BM, BM_conf = which_BM(input_dir)
    with open(os.path.join("./processed_results/results", BM, BM_conf, "allocation_rate_avg.txt"), "a") as writer:
        writer.write(str(allocation_rate_global_avg[-1] + '\n'))
    with open(os.path.join("./processed_results/results", BM, BM_conf, "allocation_rate_max.txt"), "a") as writer:
        writer.write(str(allocation_rate_global_max[-1] + '\n'))
    with open(os.path.join("./EnergyVsTimePlots/tables/table_allocation_rate_dynamic_" + BM + ".txt"), "a") as writer:
        writer.write(BM + "_" + BM_conf + " ")
        for el in allocation_rate_global_dynamic:
            #print(el + " ")
            writer.write(str(el) + " ")
        writer.write("\n")


def main():
    input_dir = sys.argv[1]
    file_name = sys.argv[2]
    output_dir = sys.argv[3]
    analyze_file(input_dir, file_name)
    #analyze_file()

if __name__ == "__main__":
    main()
