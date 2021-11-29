#!/usr/bin/env python
# coding: utf-8

# # Scatterplots: median time vs energy - size 1

# In[1]:

import os
from os import listdir
from os.path import isfile, join

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random
import string
# In[2]:
benchmark_group_apache_spark = ["als", "chi-square", "dec-tree", "gauss-mix", "log-regression", "movie-lens", "naive-bayes", "page-rank"]
benchmark_group_concurrency = ["akka-uct", "fj-kmeans", "reactors"]
benchmark_group_functional = ["future-genetic", "mnemonics", "par-mnemonics", "rx-scrabble", "scrabble"]
benchmark_group_scala = ["dotty", "philosophers", "scala-doku", "scala-kmeans", "scala-stm-bench7"]
benchmark_group_web = ["finagle-chirper", "finagle-http"]
benchmark_group_latency = ["hazelcast"]
benchmark_group_dacapo = ["avora_large", "fop_default", "h2_large_t4", "h2_small_t4", "luindex_default", "lusearch_large", "pmd_large", "sunflow_large"]
benchmark_group_memory_bound = ["scrabble", "mnemonics"]
benchmark_group_compute_bound = ["als", "movie-lens"]

benchmark_groups = []
#benchmark_groups.extend(benchmark_group_apache_spark)
#benchmark_groups.extend(benchmark_group_concurrency)
#benchmark_groups.extend(benchmark_group_functional)
#benchmark_groups.extend(benchmark_group_scala)
benchmark_groups.extend(benchmark_group_web)
#benchmark_groups.extend(benchmark_group_latency)
#benchmark_groups.extend(benchmark_group_dacapo)
#benchmark_groups.extend(benchmark_group_dacapo)
#benchmark_groups.extend(benchmark_group_memory_bound)
#benchmark_groups.extend(benchmark_group_compute_bound)


main_configurations = ["Serial", "Parallel", "ZGC", "ShenGC", "G1", "CMS"]

populate = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])

count_P=0
count_Z = 0
count_Ser = 0
count_Shen = 0
count_G1 = 0
count_CMS = 0
def normilize_populate():
    global count_P
    global count_Ser
    global count_Z
    global count_Shen
    global count_G1
    global count_CMS
    count_array = []
    count_array.append(count_P)
    count_array.append(count_Ser)
    count_array.append(count_Z)
    count_array.append(count_G1)
    count_array.append(count_Shen)
    count_array.append(count_CMS)
    count_array.sort()
    norm = count_array[0]
    for i in range(len(main_configurations)):
        for j in range(len(main_configurations)):
            if i is 0 or j is 0: #Serial
                populate[i][j] = populate[i][j] / (count_Ser / norm)
            if i is 1 or j is 1: #Parallel
                populate[i][j] = populate[i][j] / (count_P / norm)
            if i is 2 or j is 2: #Z
                populate[i][j] = populate[i][j] / (count_Z / norm)
            if i is 3 or j is 3: #Shen
                populate[i][j] = populate[i][j] / (count_Shen / norm)
            if i is 4 or j is 4: #G1
                populate[i][j] = populate[i][j] / (count_G1 / norm)
            if i is 5 or j is 5: #CMS
                populate[i][j] = populate[i][j] / (count_CMS / norm)
        
def mark_x(GC, index):
    incr = 1 / value
    if "P" in GC:
        global count_P
        count_P = count_P + 1
        for i in range(6):
            populate[i][1] = populate[i][1] + incr
    if "Ser" in GC:
        global count_Ser 
        count_Ser = count_Ser + 1
        for i in range(6):
            populate[i][0] = populate[i][0] + incr
    if "Z" in GC:
        global count_Z
        count_Z = count_Z + 1
        for i in range(6):
            populate[i][2] = populate[i][2] + incr
    if "Shen" in GC:
        global count_Shen
        count_Shen = count_Shen + 1
        for i in range(6):
            populate[i][3] = populate[i][3] + incr
    if "G1" in GC:
        global count_G1
        count_G1 = count_G1 + 1
        for i in range(6):
            populate[i][4] = populate[i][4] + incr
    if "CMS" in GC:
        global count_CMS
        count_CMS = count_CMS + 1
        for i in range(6):
            populate[i][5] = populate[i][5] + incr

def mark_y(GC, value):
    increment = 1 / value
    if "P" in GC:
        for i in range(6):
            populate[1][i] = populate[1][i] + increment
    if "Ser" in GC:
        for i in range(6):
            populate[0][i] = populate[0][i] + increment
    if "Z" in GC:
        for i in range(6):
            populate[2][i] = populate[2][i] + increment
    if "Shen" in GC:
        for i in range(6):
            populate[3][i] = populate[3][i] + increment
    if "G1" in GC:
        for i in range(6):
            populate[4][i] = populate[4][i] + increment
    if "CMS" in GC:
        for i in range(6):
            populate[5][i] = populate[5][i] + increment

for bench in benchmark_groups:
    energy_pack_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_pack"))])
    energy_cpu_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_cpu"))])
    energy_dram_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_dram"))])
    perf_files = sorted(f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_perf")))
    maxl_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_max_l"))])
    meanl_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_mean_l"))])
    wattsp_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_watts_p"))])
    gc_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_GC"))])
   
    for energy_pack_file,energy_cpu_file, energy_dram_file, perf_file, maxl_file, meanl_file, wattsp_file, gc_file in zip(energy_pack_files, energy_cpu_files, energy_dram_files, perf_files, maxl_files, meanl_files, wattsp_files, gc_files):
        # Reads data from the first configuration
        original_data1 = pd.read_csv(perf_file, sep=';', index_col="BMs")
        # Organizes it for plotting
        data1 = original_data1.stack().reset_index()
        data1.columns = ['BM', 'GC', 'Time']
        replace_data = data1["Time"]
        for idx, data in enumerate(replace_data):
            if type(data) is str:
                replace_data[idx] = np.nan
        data1["Time"] = replace_data
        data1 = data1.sort_values(by = "Time")
        for index, GC in enumerate(data1['GC']):
            value = data1["Time"][index]
            mark_x(GC, value)
    

        # Reads energy for the pack
        original_data2 = pd.read_csv(energy_pack_file, sep=';', index_col="BMs")
        # Organizes it for plotting
        data2 = original_data2.stack().reset_index()
        data2.columns = ['BM', 'GC', 'Energy']
        replace_data = data2["Energy"]
        for idx, data in enumerate(replace_data):
            if type(data) is str:
                replace_data[idx] = np.nan
        data2["Energy"] = replace_data
        data2 = data2.sort_values(by = "Energy")
        for index, GC in enumerate(data2['GC']):
            value = data2["Energy"][index]
            mark_y(GC, value)

#print("count_P = ", count_P)
#print("count_Ser = ", count_Ser)
#print("count_Z = ", count_Z)
#print("count_G1 = ", count_G1)
#print("count_Shen = ", count_Shen)
#print("count_CMS = ", count_CMS)
print(populate)
normilize_populate()
print(populate)
fig, ax = plt.subplots()
im = ax.imshow(populate)
sns.heatmap(populate, annot=True,  linewidths=.5)
# We want to show all ticks...
ax.set_xticks(np.arange(len(main_configurations)))
ax.set_yticks(np.arange(len(main_configurations)))
# ... and label them with the respective list entries
ax.set_xticklabels(main_configurations)
ax.set_yticklabels(main_configurations)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
plt.setp(ax.get_yticklabels(), rotation=0, ha="right",
         rotation_mode="anchor")

ax.set_title("The best energy/perf configurations")
fig.tight_layout()
fig.savefig("NewPLot")

