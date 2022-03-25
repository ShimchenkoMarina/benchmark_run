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
import csv

import PlotDendrogram
import PlotHeatMap
# In[2]:
bench = ""
#TODO: and P_def
basic_configurations = ["j16Z1.0", "j16Ser1.0", "j16G11.0", "j16Shen1.0", "j16P1.0_n1", "j16P1.0_n2", "j16P1.0_n4", "j13Ser1.0", "j13CMS1.0", "j13P1.0_n1", "j13P1.0_n2", "j13P1.0_n4", "j16Z1.5", "j16Ser1.5", "j16G11.5", "j16Shen1.5", "j16P1.5_n1", "j16P1.5_n2", "j16P1.5_n4", "j13Ser1.5", "j13CMS1.5", "j13P1.5_n1", "j13P1.5_n2", "j13P1.5_n4", "j16Z2.0", "j16Ser2.0", "j16G12.0", "j16Shen2.0", "j16P2.0_n1", "j16P2.0_n2", "j16P2.0_n4", "j13Ser2.0", "j13CMS2.0", "j13P2.0_n1", "j13P2.0_n2", "j13P2.0_n4"]
energy_pack_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_pack"))])
energy_cpu_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_cpu"))])
energy_dram_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_dram"))])
energy_pd_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_pack_dram") and "%" not in f)])
perf_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_perf"))])
maxl_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_max_l"))])
meanl_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_mean_l"))])
wattsp_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_watts_p"))])
gc_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_GC"))])
array_of_arrays_perf = []
array_of_arrays_energy_pack = []
array_of_BMs = []
for file1, file2 in zip(energy_pd_files, perf_files):
    print(file1 + "  --> " + file2)
for energy_pack_file, perf_file, meanl_file, maxl_file, epd_file in zip(energy_pack_files, perf_files, meanl_files, maxl_files, energy_pd_files):
    array_perf = []
    array_energy_pack = []
    array_mean_latency = []
    array_max_latency = []
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
    #print(data1["BM"][0])

    #if "hazel" not in data1['BM'][0] and "avrora" not in data1['BM'][0] and "spec" not in data1['BM'][0]:
    #    continue
    original_data2 = pd.read_csv(epd_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data2 = original_data2.stack().reset_index()
    data2.columns = ['BM', 'GC', 'Energy']
    replace_data = data2["Energy"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data2["Energy"] = replace_data
    
    # Reads mean latency
    original_data3 = pd.read_csv(meanl_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data3 = original_data3.stack().reset_index()
    data3.columns = ['BM', 'GC', 'Latency']
    replace_data = data3["Latency"]
    for idx, data in enumerate(replace_data):
            if type(data) is str:
                replace_data[idx] = np.nan
    data3["Latency"] = replace_data
    time_label = "Latency"
        
        # Reads max latency
    original_data4 = pd.read_csv(maxl_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data4 = original_data4.stack().reset_index()
    data4.columns = ['BM', 'GC', 'Latency']
    replace_data = data4["Latency"]
    for idx, data in enumerate(replace_data):
            if type(data) is str:
                replace_data[idx] = np.nan
    data4["Latency"] = replace_data

    #Figure the basic configurations
    #Find default heap size
    #min_heap_size = find_heap_size(data1['BM'][0])
    for conf in basic_configurations:
            fail = True
            for index, GC in enumerate(data1["GC"]):
                if conf == GC:
                    fail = False
                    array_perf.append(data1["Time"][index])
                    break
            if fail:
                print(data1["BM"][0] + " " + conf)
            for index, GC in enumerate(data2["GC"]):
                if conf == GC:
                    array_energy_pack.append(data2["Energy"][index])
                    break
            for index, GC in enumerate(data3["GC"]):
                if conf == GC:
                    array_mean_latency.append(data3["Latency"][index])
                    break
            for index, GC in enumerate(data4["GC"]):
                if conf == GC:
                    array_max_latency.append(data4["Latency"][index])
                    break
    #print(data2)
    #print(data3)
    #print(data4)
    #print(data4["BM"][0])
    print(len(array_energy_pack))
    if len(array_energy_pack) == len(basic_configurations) and ("hazelcast_NUMA" in data1["BM"][0] or data1["BM"][0] == "hazelcast"):
        if len(array_perf) == len(basic_configurations) and "hazelcast" not in data1["BM"][0] and "spec" not in data1["BM"][0]:
            array_of_arrays_perf.append(array_perf) 
            array_of_arrays_energy_pack.append(array_energy_pack) 
            array_of_BMs.append(data1["BM"][0])
        if len(array_mean_latency) == len(basic_configurations):
            array_of_arrays_perf.append(array_mean_latency) 
            array_of_arrays_energy_pack.append(array_energy_pack) 
            array_of_BMs.append(data1["BM"][0] + "_mean_l")
        if len(array_max_latency) == len(basic_configurations):
            array_of_arrays_perf.append(array_max_latency) 
            array_of_arrays_energy_pack.append(array_energy_pack) 
            array_of_BMs.append(data1["BM"][0] + "_max_l")
    else:
            #print(array_energy_pack)
            print("Not true for " + data1["BM"][0])
#for index, bm in enumerate(array_of_BMs):
#    if "kmeans" in bm:
#        print(array_of_arrays_energy_pack[index])
'''f = open('./all_data_perf.csv', 'w')
writer = csv.writer(f)
writer.writerow(basic_configurations)
for index, bm in enumerate(array_of_BMs):
    #print(bm)
    row = array_of_arrays_perf[index]
    row.insert(0,bm)
    #print(row)
    writer.writerow(row)
f.close()
f = open('./all_data_energy.csv', 'w')
writer = csv.writer(f)
writer.writerow(basic_configurations)
for index, bm in enumerate(array_of_BMs):
    row = list(array_of_arrays_energy_pack[index])
    row.insert(0,bm)
    #print(row)
    #row.insert(0,bm)
    #print(row)
    writer.writerow(row)
f.close()
'''
#print(array_of_BMs)
#print(array_of_arrays_perf)
#print(array_of_arrays_energy_pack)
name = "Clustering_Perf"
PlotDendrogram.setup_dendrogram(array_of_arrays_perf, array_of_BMs, name)
name = "HeatMapClust_Perf"
PlotHeatMap.get_order(array_of_arrays_perf, array_of_BMs, basic_configurations, name)
name = "HeatMapClust_Energy_full_perf_order"
PlotHeatMap.get_order(array_of_arrays_energy_pack, array_of_BMs, basic_configurations, name)
name = "Clustering_energy_full"
PlotDendrogram.setup_dendrogram(array_of_arrays_energy_pack, array_of_BMs, name)
name = "HeatMapClust_Energy_full_original_order"
PlotHeatMap.get_order(array_of_arrays_energy_pack, array_of_BMs, basic_configurations, name)
