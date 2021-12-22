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

import PlotDendrogram
import PlotHeatMap
# In[2]:
bench = ""
#TODO: and P_def
basic_configurations = ["j16Z1.0", "j16Ser1.0", "j16G11.0", "j16Shen1.0", "j16P1.0_n1", "j16P1.0_n2", "j16P1.0_n4", "j13Ser1.0", "j13CMS1.0", "j13P1.0_n1", "j13P1.0_n2", "j13P1.0_n4"]

energy_pack_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_pack"))])
energy_cpu_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_cpu"))])
energy_dram_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_dram"))])
energy_pd_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_pack_dram"))])
perf_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_perf"))])
maxl_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_max_l"))])
meanl_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_mean_l"))])
wattsp_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_watts_p"))])
gc_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_GC"))])

array_of_arrays_perf = []
array_of_arrays_energy_pack = []
array_of_BMs = []
for energy_pack_file, perf_file, meanl_file, maxl_file, epd_file in zip(energy_pack_files, perf_files, meanl_files, maxl_files, energy_pd_files):
    array_perf = []
    array_energy_pack = []
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
    original_data2 = pd.read_csv(epd_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data2 = original_data2.stack().reset_index()
    data2.columns = ['BM', 'GC', 'Energy']
    replace_data = data2["Energy"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data2["Energy"] = replace_data
    
    time_label = "Time"
    if "hazelcast" in data1['BM'][0]:
        # Reads mean latency
        original_data1 = pd.read_csv(meanl_file, sep=';', index_col="BMs")
        # Organizes it for plotting
        data1 = original_data1.stack().reset_index()
        data1.columns = ['BM', 'GC', 'Latency']
        replace_data = data1["Latency"]
        for idx, data in enumerate(replace_data):
            if type(data) is str:
                replace_data[idx] = np.nan
        data1["Latency"] = replace_data
        time_label = "Latency"
        
        # Reads max latency
        original_data3 = pd.read_csv(maxl_file, sep=';', index_col="BMs")
        # Organizes it for plotting
        data3 = original_data3.stack().reset_index()
        data3.columns = ['BM', 'GC', 'Latency']
        replace_data = data3["Latency"]
        for idx, data in enumerate(replace_data):
            if type(data) is str:
                replace_data[idx] = np.nan
        data3["Latency"] = replace_data

    #Figure the basic configurations
    #Find default heap size
    #min_heap_size = find_heap_size(data1['BM'][0])
    array_perf_temp = []
    for conf in basic_configurations:
            for index, GC in enumerate(data1["GC"]):
                if conf in GC and "P" not in GC:
                    array_perf.append(data1[time_label][index])
                    if "Latency" in time_label:
                        array_perf_temp.append(data3[time_label][index])
                    break
                if "P" in GC and conf in GC:
                    array_perf.append(data1[time_label][index])
                    if "Latency" in time_label:
                        array_perf_temp.append(data3[time_label][index])
                    break
            for index, GC in enumerate(data2["GC"]):
                if conf in GC and "P" not in GC:
                    array_energy_pack.append(data2["Energy"][index])
                    break
                if "P" in GC and conf in GC:
                    array_energy_pack.append(data2["Energy"][index])
                    break
    if len(array_perf) == len(basic_configurations) and len(array_energy_pack) == len(basic_configurations):
        array_of_arrays_perf.append(array_perf) 
        array_of_arrays_energy_pack.append(array_energy_pack) 
        array_of_BMs.append(data1["BM"][0])
    if len(array_perf_temp) == len(basic_configurations) and len(array_energy_pack) == len(basic_configurations) and "Latency" in time_label:
        array_of_arrays_perf.append(array_perf_temp) 
        array_of_arrays_energy_pack.append(array_energy_pack) 
        array_of_BMs.append(data1["BM"][0] + "_maxl")
#for index, bm in enumerate(array_of_BMs):
#    if "kmeans" in bm:
#        print(array_of_arrays_energy_pack[index])
#print(array_of_BMs)
#print(array_of_arrays_perf)
#print(array_of_arrays_energy_pack)
name = "Clustering_Perf"
PlotDendrogram.setup_dendrogram(array_of_arrays_perf, array_of_BMs, name)
name = "HeatMapClust_Perf"
PlotHeatMap.get_order(array_of_arrays_perf, array_of_BMs, basic_configurations, name)
name = "HeatMapClust_Energy_pack_perf_order"
PlotHeatMap.get_order(array_of_arrays_energy_pack, array_of_BMs, basic_configurations, name)
name = "Clustering_energy_pack"
PlotDendrogram.setup_dendrogram(array_of_arrays_energy_pack, array_of_BMs, name)
name = "HeatMapClust_Energy_pack_original_order"
PlotHeatMap.get_order(array_of_arrays_energy_pack, array_of_BMs, basic_configurations, name)

