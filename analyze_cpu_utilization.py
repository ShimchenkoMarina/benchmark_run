#!/usr/bin/python3
import sys
import os
import re
from functools import reduce

BMs = ["finagle-http", "finagle-chirper", "spec", "hazelcast"]
def separate_number_chars(s):
    res = re.split('([-+]?\d+\.\d+)|([-+]?\d+)', s.strip())
    res_f = [r.strip() for r in res if r is not None and r.strip() != '']
    return res_f

def avg(l):
    return reduce(lambda a, b: a + b, l) / len(l)

def sum(l):
    return reduce(lambda a, b: a + b, l)

def which_BM(bm, string):
    BM = ""
    BM_conf = ""
    BM = string.split(" ")[0][:-16]
    BM_conf = string.split(" ")[1][:-1]
    return BM, BM_conf

def process_line(string):
    #print(string)
    res = string.split(" ")
    res_f = [r.strip() for r in res if r is not None and r.strip() != '']
    cpu_util = 100 - float(res_f[11].replace(",", "."))
    return cpu_util

def output_cpu_util(lst, BM, BM_conf):
    #print(lst)
    #print(BM)
    #print(BM_conf)
    with open(os.path.join("./processed_results/results", BM, BM_conf, "cpu_utilization.txt"), "a+") as writer:
        writer.write(str(avg(lst)) + "\n")


def analyze_file():

    #for i in range(1, int(file_num)):
    with open(os.path.join("./output.txt"), 'r') as reader:
            BM = ""
            BM_conf = ""
            cpu_util_list = []
            for line in reader.readlines():
                if BM != "" and "777" not in line and "777\n" != line:
                    cpu_util_list.append(process_line(line))
                elif "777\n" != line and "777" not in line:
                    for bm in BMs:
                        if bm in line: #BM starts
                            BM, BM_conf = which_BM(bm, line)
                            print(BM)
                elif "777\n" == line:
                    #print("I am here")
                    output_cpu_util(cpu_util_list, BM, BM_conf)
                    BM = ""
                    BM_conf = ""
                    cpu_util_list = []


def main():
    analyze_file()

if __name__ == "__main__":
    main()
