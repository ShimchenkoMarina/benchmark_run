#!/usr/bin/env python
# coding: utf-8

# # Scatterplots: median time vs energy - size 1

# In[1]:

import os
from os import listdir
from os.path import isfile, join
from collections import namedtuple, OrderedDict
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
# In[2]:
bench = ""
N = 3
#TODO: and P_def
basic_configurations1 = ["j16Z1.0", "j16Ser1.0", "j16G11.0", "j16Shen1.0", "j16P1.0_n1", "j16P1.0_n2", "j16P1.0_n4", "j13Ser1.0", "j13CMS1.0", "j13P1.0_n1", "j13P1.0_n2", "j13P1.0_n4"]
basic_configurations2 = ["j16Z1.5", "j16Ser1.5", "j16G11.5", "j16Shen1.5", "j16P1.5_n1", "j16P1.5_n2", "j16P1.5_n4", "j13Ser1.5", "j13CMS1.5", "j13P1.5_n1", "j13P1.5_n2", "j13P1.5_n4"]
basic_configurations3 = ["j16Z2.0", "j16Ser2.0", "j16G12.0", "j16Shen2.0", "j16P2.0_n1", "j16P2.0_n2", "j16P2.0_n4", "j13Ser2.0", "j13CMS2.0", "j13P2.0_n1", "j13P2.0_n2", "j13P2.0_n4"]
energy_pack_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_pack") and "dram" not in f)])
energy_cpu_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_cpu"))])
energy_dram_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_dram"))])
energy_pd_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_pack_dram") and "%" not in f)])
energy_pd_percentale_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_pack_dram%"))])
perf_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_perf"))])
maxl_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_max_l"))])
meanl_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_mean_l"))])
wattsp_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_watts_p"))])
gc_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_GC_cycles"))])
energy_pack = []
fig, ax = plt.subplots(3,3, figsize=(20,10), dpi = 300)
count = 0
pos_x = 0
pos_y = 0
handles = []
labels = []
basic_configuration = []
#for f1, f2 in zip(energy_pack_files, energy_pd_files):
#    print(f1 +  "   " + f2)
for conf in basic_configurations1:
    basic_configuration.append(conf.replace("1.0", ""))
print(basic_configuration)
f = open('/home/marina/workspace/2021NewProject/OpenJDK/benchmark_run/EnergyVsTimePlots/all_heap_sizes_experiments.csv', 'w')
writer = csv.writer(f)
all_conf = []
all_conf.append("BMs/GCs")
for conf in basic_configurations1:
    all_conf.append(conf)
for conf in basic_configurations2:
    all_conf.append(conf)
for conf in basic_configurations3:
    all_conf.append(conf)
writer.writerow(all_conf)
for gc_file, epd_file, e_dram_of_pack_file, dram_file, cpu_file in zip(gc_files, energy_pd_files, energy_pd_percentale_files, energy_dram_files, energy_pack_files):
    # Reads data from the first configuration
    original_data1 = pd.read_csv(epd_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data1 = original_data1.stack().reset_index()
    data1.columns = ['BM', 'GC', 'Energy']
    replace_data = data1["Energy"]
    #for idx, data in enumerate(replace_data):
    #    if type(data) is str:
    #        replace_data[idx] = np.nan
    #data1["Energy"] = replace_data
    bm = data1["BM"][0]
    #print(bm)
    
    # Reads data from the first configuration
    original_data2 = pd.read_csv(gc_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data2 = original_data2.stack().reset_index()
    data2.columns = ['BM', 'GC', 'GC_count']
    
    original_data3 = pd.read_csv(dram_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data3 = original_data3.stack().reset_index()
    data3.columns = ['BM', 'GC', 'Energy']
    
    original_data4 = pd.read_csv(cpu_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data4 = original_data4.stack().reset_index()
    data4.columns = ['BM', 'GC', 'Energy']
    
    original_data5 = pd.read_csv(e_dram_of_pack_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data5 = original_data5.stack().reset_index()
    data5.columns = ['BM', 'GC', 'Percent']
    #print(data5)
    #print(data1)
    
    row = []
    row_gc_count = []
    row_dram = []
    row_cpu = []
    #print(bm) 
    if "hazelcast" in bm:
        continue
    for i in range(0, N):
        row.append([None] * len(basic_configurations1))
        row_dram.append([None] * len(basic_configurations1))
        row_cpu.append([None] * len(basic_configurations1))
        row_gc_count.append([None] * len(basic_configurations1))
    sum = 0
    #if data1["BM"][0] != data4["BM"][0]:
    #    print(data1["BM"][0])
    #    print(data4["BM"][0])
    #    continue
    for index, gc in enumerate(data1["GC"]):
        for x, basic_gc1 in enumerate(basic_configurations1):
             if gc == basic_gc1:
                row[0][x] = data1["Energy"][index]
                row_dram[0][x] = data1["Energy"][index]
                row_cpu[0][x] = data4["Energy"][index]
                row_gc_count[0][x] = data2["GC_count"][index]
                print("1.0 " + gc + " "  +str(row_gc_count[0][x]))
                sum = sum + 1
        for x, basic_gc2 in enumerate(basic_configurations2):
             if gc == basic_gc2:
                row[1][x] = data1["Energy"][index]
                row_dram[1][x] = data3["Energy"][index]
                row_cpu[1][x] = data4["Energy"][index]
                row_gc_count[1][x] = data2["GC_count"][index]
                print("1.5 " + gc + " " +str(row_gc_count[1][x]))
                sum = sum + 1
        for x, basic_gc3 in enumerate(basic_configurations3):
             if gc == basic_gc3:
                row[2][x] = data1["Energy"][index]
                row_dram[2][x] = data3["Energy"][index]
                row_cpu[2][x] = data4["Energy"][index]
                row_gc_count[2][x] = data2["GC_count"][index]
                print("2 " + gc + " " +str(row_gc_count[2][x]))
                sum = sum + 1
    if sum is len(basic_configurations1)*3:
        print(bm) 
        print(row_gc_count[0][2])
        print(row_gc_count[1][2])
        print(row_gc_count[2][2])
        '''global_row = []
        global_row.append(bm)
        for el in row[0]:
            global_row.append(el)
        for el in row[1]:
            global_row.append(el)
        for el in row[2]:
            global_row.append(el)
        writer.writerow(global_row)'''
        for x, val in enumerate(row[0]):
            gc1 = basic_configurations1[x]
            gc2 = basic_configurations2[x]
            gc3 = basic_configurations3[x]
            '''for y, gc_indata5 in enumerate(data5["GC"]):
                    if gc_indata5 == gc2:
                        row[1][x] = row[1][x]/val - (row[1][x]/val)*data5["Percent"][y]
                        row_dram[1][x] = row[1][x]/val*data5["Percent"][y]
                        row_cpu[1][x] = row_cpu[1][x]/row_cpu[0][x]
            for y, gc_indata5 in enumerate(data5["GC"]):
                    if gc_indata5 == gc3:
                        row[2][x] = row[2][x]/val - (row[1][x]/val)*data5["Percent"][y]
                        row_dram[2][x] = (row[1][x]/val)*data5["Percent"][y]
                        row_cpu[2][x] = row_cpu[2][x]/row_cpu[0][x]
            for y, gc_indata5 in enumerate(data5["GC"]):
                    if gc_indata5 == gc1:
                        row[0][x] = 1 - 1*data5["Percent"][y]
                        row_dram[0][x] = 1*data5["Percent"][y]
                        row_cpu[0][x] = 1'''
            row[1][x] = row[1][x]/val
            row[2][x] = row[2][x]/val
            row[0][x] = 1
        for inx in range(0, len(basic_configurations1)):
            print(basic_configurations2[inx] + " " + str(row_gc_count[1][inx]))
            row_gc_count[1][inx] = row_gc_count[1][inx]/row_gc_count[0][inx]
            print(row_gc_count[1][inx])
            row_gc_count[2][inx] = row_gc_count[2][inx]/row_gc_count[0][inx]
            row_gc_count[0][inx] = 1
        #print(row_gc_count)
        ind = np.arange(len(basic_configurations1)) 
        width = 0.2
        ax[pos_x][pos_y].bar(ind, row[0], width, label='1.0 Jouls Pack', color = 'orangered')
        #ax[pos_x][pos_y].bar(ind, row_dram[0], width, label='1.0 Jouls DRAM', color = 'b')
        ax[pos_x][pos_y].bar(ind, row_gc_count[0], width, label='1.0 GC', color = 'silver',  alpha=0.5, hatch='///')
        ax[pos_x][pos_y].bar(ind + width, row[1], width,label='1.5 Jouls', color = 'r')
        ax[pos_x][pos_y].bar(ind + width, row_gc_count[1], width, label='1.5 GC', color = 'silver',  alpha=0.5, hatch='--')
        #ax[pos_x][pos_y].bar(ind + width, row_dram[1], width, label='1.5 Jouls DRAM', color = 'gold')
        ax[pos_x][pos_y].bar(ind + 2*width, row[2], width,label='2.0 Jouls', color = 'salmon')
        ax[pos_x][pos_y].bar(ind + 2*width, row_gc_count[2], width, label='2.0 GC', color = 'silver',  alpha=0.5, hatch='////')
        #ax[pos_x][pos_y].bar(ind + 2*width, row_dram[2], width, label='2.0 Jouls DRAM', color = 'olive')
        #ax[count].bar(ind + 5*width, row_dram[2], width, label='2.0', color = 'khaki')
        #ax[count].bar(ind + 3*width, row_dram[0], width, label='1.0', color = 'gold')
        #ax[count].bar(ind + 4*width, row_dram[1], width, label='1.5', color = 'goldenrod')
        #ax[count].bar(ind + 8*width, row_dram[2], width, label='2.0', color = 'cadetblue')
        #ax[count].bar(ind + 6*width, row_dram[0], width, label='1.0', color = 'darkslategray')
        #ax[count].bar(ind + 7*width, row_dram[1], width, label='1.5', color = 'teal')
        plt.sca(ax[pos_x][pos_y])
        plt.xticks((ind + 2 * width), basic_configuration, fontsize=8, rotation = 45)
        ax[pos_x][pos_y].set(title=bm)
        handles, labels = ax[pos_x][pos_y].get_legend_handles_labels()
        count = count + 1
        pos_y = pos_y + 1
        if pos_y == 3:
            pos_x = pos_x + 1
            pos_y = 0 
plt.tight_layout()
lgd = fig.legend(handles, labels, ncol=9, handletextpad=2, bbox_to_anchor=(0.7, -0.02))
plt.savefig("HS", bbox_inches="tight")
f.close()
