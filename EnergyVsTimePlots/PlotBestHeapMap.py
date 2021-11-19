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

'''    # Reads max latency
    original_data3 = pd.read_csv(maxl_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data3 = original_data3.stack().reset_index()
    data3.columns = ['BM', 'GC', 'MaxL']
    replace_data = data3["MaxL"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data3["MaxL"] = replace_data
    
    # Reads mean latency
    original_data4 = pd.read_csv(meanl_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data4 = original_data4.stack().reset_index()
    data4.columns = ['BM', 'GC', 'MeanL']
    replace_data = data4["MeanL"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data4["MeanL"] = replace_data
    
    # Reads power
    original_data5 = pd.read_csv(wattsp_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data5 = original_data5.stack().reset_index()
    data5.columns = ['BM', 'GC', 'WattsP']
    replace_data = data5["WattsP"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data5["WattsP"] = replace_data

    # Reads energy for the pack
    original_data6 = pd.read_csv(energy_cpu_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data6 = original_data6.stack().reset_index()
    data6.columns = ['BM', 'GC', 'EnergyC']
    replace_data = data6["EnergyC"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data6["EnergyC"] = replace_data


    # Reads energy for the pack
    original_data7 = pd.read_csv(energy_dram_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data7 = original_data7.stack().reset_index()
    data7.columns = ['BM', 'GC', 'EnergyD']
    replace_data = data7["EnergyD"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data7["EnergyD"] = replace_data
    
    # Reads energy for the pack
    original_data8 = pd.read_csv(gc_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data8 = original_data8.stack().reset_index()
    data8.columns = ['BM', 'GC', 'GC_cycles']
    replace_data = data8["GC_cycles"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data8["GC_cycles"] = replace_data
    print(data8)

    # Organizes information related to the regions and configurations used
    #configurations = original_data1.columns
    bms1 = original_data1.index
    print(bms1)
    bms2 = original_data2.index
    print(bms2)
    bm = [value for value in bms1 if value in bms2]
    print(bm)
    if "hazelcast" in bm:
        regions = [["EnerFPerf", "PowerFPerf"], ["EnerCPerf", "EnerDPerf"], ["EnerFMaxL", "EnerFMeanL"], ["PowerFMaxL", "PowerFMeanL"]]
    else:
        regions = [["EnerFPerf", "PowerFPerf"], ["EnerCPerf", "EnerDPerf"]]
        
    # In[3]:
    
    print(best_perf)    
    # Generate scatterplots
    if "hazelcast" in bm:
        fig,ax = plt.subplots(5,2, figsize=(15, 5*15), gridspec_kw={'width_ratios': [1, 1], 'height_ratios': [1, 1, 1, 1, 1]})
    else: 
        fig,ax = plt.subplots(3,2, figsize=(15, 5*15), gridspec_kw={'width_ratios': [1, 1], 'height_ratios': [1, 1, 1]})
    column_y = ""
    column_x = ""
    for index_x, tuple_region in enumerate(regions):
        for index_y, region in enumerate(tuple_region):
            if "Perf" in region:
                right = data1
                column_x = "Time"
            elif "MaxL" in region:
                right = data3
                column_x = "MaxL"
                ax[index_x][index_y].set(xscale="log")
            elif "MeanL" in region:
                right = data4
                column_x = "MeanL"
                ax[index_x][index_y].set(xscale="log")
            if "EnerF" in region:
                left = data2
                column_y = "Energy"
            elif "PowerF" in region:
                left = data5
                column_y = "WattsP"
            elif "EnerC" in region:
                left = data6
                column_y = "EnergyC"
            elif "EnerD" in region:
                left = data7
                column_y = "EnergyD"
            plot_data = pd.merge(left, right, on='GC')
            print(plot_data)
            #print(plot_data.sort_values("GC"))
            #indexes = []
            #for index in plot_data.index:
            #    if "5g" not in plot_data["GC"][index]:
            #        indexes.append(index)
            #print(indexes)
            #plot_data.drop(index=indexes, axis=0, inplace=True)
            #print(plot_data)
            ax[index_x][index_y].set(title=(f"{column_y} and {column_x}"))
            plt.sca(ax[index_x][index_y])
            #sns.scatterplot(data=plot_data, s=300, x=column_x, y=column_y, hue=plot_data['GC'], palette = sns.color_palette('gnuplot', n_colors=len(plot_data['GC']))).get_figure().savefig(str(bm[0]) + ".png")
            sns.scatterplot(data=plot_data, s=300, x=column_x, y=column_y, hue=plot_data['GC'], style=plot_data["GC"]).get_figure().savefig(str(bm[0]) + ".png")
            #splot.set(xscale="log")
    if "hazelcast" in bm:
        ax[4][0].set(title=(f"GC_cycles per version"))
        plt.sca(ax[4][0])
    else: 
        ax[2][0].set(title=(f"GC_cycles per version"))
        plt.sca(ax[2][0])
    sns.scatterplot(data=data8, s=300, x="GC",y="GC_cycles", hue=data8['GC'], style=data8["GC"]).get_figure().savefig(str(bm[0]) + ".png")'''
