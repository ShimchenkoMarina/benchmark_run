#!/usr/bin/env python
# coding: utf-8

# # Scatterplots: median time vs energy - size 1

# In[1]:

import os
from os import listdir
from os.path import isfile, join
import re

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random
import string
import csv

import PlotDendrogram
import PlotHeatMap
import PlotBars
# In[2]:
dict = {
    "specjbb15":  ["j20GZ1.0", "j20YinYanZ1.0", "j20GZ1.5", "j20YinYanZ1.5","j20GZ2.0", "j20YinYanZ2.0","j20GZ4.0","j20YinYanZ4.0"],
    "hazelcast":  ["j20GZ1.0", "j20YinYanZ1.0", "j20GZ1.2", "j20YinYanZ1.2","j20GZ1.3", "j20YinYanZ1.3","j20GZ1.5","j20YinYanZ1.5"],
    "finagle-http":  ["j20GZ1.0", "j20YinYanZ1.0", "j20GZ1.5", "j20YinYanZ1.5","j20GZ2.0", "j20YinYanZ2.0","j20GZ2.5","j20YinYanZ2.5"],
    "finagle-chirper":  ["j20GZ1.0", "j20YinYanZ1.0", "j20GZ1.5", "j20YinYanZ1.5","j20GZ2.0", "j20YinYanZ2.0","j20GZ2.5","j20YinYanZ2.5"]

}
def separate_number_chars(s):
    res = re.split(' ', s.strip())
    res_f = [r.strip() for r in res if r is not None and r.strip() != '']
    print(res_f)
    return res_f

def valid_conf(bm):
    global dict
    conf = re.split('_', bm.strip())[-1]
    BM = re.split('_', bm.strip())[0]
    for el in dict[BM]:
        if el == conf:
            return True
    return False

def sort(arrays, confs, bm):
    global dict
    lst = [[]]*len(dict[bm])
    labels = [""]*len(dict[bm])
    for jindex, j in enumerate(dict[bm]):
        for iindex, conf in enumerate(confs):
            if j in conf:
                lst[jindex] = arrays[iindex]
                labels[jindex] = conf
    return lst, labels

def create_graphs(lst, labels):
    lst, labels = sort(lst, labels, labels[0].split("_")[0])
    fig, ax = plt.subplots(int(len(labels)/2), 2,figsize= (10, len(labels)))
    k = -1
    for i in range(0, len(labels)):
        l = 0
        if i % 2 == 0:
            k = k + 1
            l = 0
        else:
            l = 1
        if lst[i]:
            res = [eval(j) for j in lst[i]]
            ax[k][l].plot(np.linspace(1, len(res), len(res)), res)
            ax[k][l].set_title(labels[i])
            start = np.min(res)
            stop = np.max(res)
            ticks = np.arange(start, stop, (stop - start) / 10)
            ax[k][l].set_yticks(ticks)
    fig.tight_layout()

    name=""
    print(labels[0])
    if labels[0].split("_")[1] != "static":
        name = labels[0].split("_")[0] + labels[0].split("_")[1]
    else:
        name = labels[0].split("_")[0]
    print(name)
    plt.savefig("./pngs/" + name + "_allocation_rate_dynamic.pdf", bbox_inches='tight',dpi=100)
    return

def read_data(file_name):
    LST = []
    BMs = []
    with open(os.path.join("./tables/", file_name), 'r') as reader:
        for line in reader.readlines():
            lst = separate_number_chars(line)
            if valid_conf(lst[0]):
                BMs.append(lst[0])
                LST.append(lst[1:])
    if LST:
        create_graphs(LST, BMs)

def process_files(files):
    #print(files)
    for f in files:
        read_data(f)

def main_bm(BM):

    allocation_rate_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith("static.txt") and f.startswith("table_allocation_rate_dynamic_" + BM))])
    print(allocation_rate_files)
    process_files(allocation_rate_files)

def main():
    for bm in ["spec"]:
        main_bm(bm)

main()
