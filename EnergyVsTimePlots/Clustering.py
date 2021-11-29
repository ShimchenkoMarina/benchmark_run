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
#TODO: add j13 and P_def
basic_configurations = ["j16Z", "j16Ser", "j16G1", "j16Shen", "j16P_n1", "j16P_n2", "j16P_n4", "j13Ser", "j13CMS", "j13P_n1", "j13P_n2", "j13P_n4"]

energy_pack_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_pack"))])
energy_cpu_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_cpu"))])
energy_dram_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_energy_dram"))])
perf_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_perf"))])
maxl_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_max_l"))])
meanl_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_mean_l"))])
wattsp_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_watts_p"))])
gc_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith(bench + ".csv") and f.startswith("table_GC"))])

array_of_arrays_perf = []
array_of_arrays_energy_pack = []
array_of_BMs = []
for energy_pack_file, perf_file in zip(energy_pack_files, perf_files):
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
    
    original_data2 = pd.read_csv(energy_pack_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data2 = original_data2.stack().reset_index()
    data2.columns = ['BM', 'GC', 'Energy']
    replace_data = data2["Energy"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data2["Energy"] = replace_data

    #Figure the basic configurations
    #Find default heap size
    get_number = []
    for GC in data1["GC"]:
        for conf in basic_configurations:
            if "m" in GC:
                if "P" not in conf and conf in GC:
                    get_number.append(int(GC[len(conf):].split("m")[0]))
                    break
                if "P" in conf and conf[0:3] in GC:
                    get_number.append(int(GC[4:].split("m")[0]))
                    break
            if "g" in GC:
                if "P" not in conf and conf in GC:
                    get_number.append(int(GC[len(conf):].split("g")[0]))
                    break
                if "P" in conf and conf[0:3] in GC:
                    get_number.append(int(GC[4:].split("g")[0]))
                    break
    get_number.sort()
    if len(get_number) > 0:
        min_heap_size = get_number[0]
        for conf in basic_configurations:
            for index, GC in enumerate(data1["GC"]):
                if conf + str(min_heap_size) in GC and "P" not in GC:
                    array_perf.append(data1["Time"][index])
                if "P" in GC and conf[:4] + str(min_heap_size) in GC:
                    if conf[4:] in GC:
                        array_perf.append(data1["Time"][index])
            for index, GC in enumerate(data2["GC"]):
                if conf + str(min_heap_size) in GC and "P" not in GC:
                    array_energy_pack.append(data2["Energy"][index])
                if "P" in GC and conf[:4] + str(min_heap_size) in GC:
                    if conf[4:] in GC:
                        array_energy_pack.append(data2["Energy"][index])
    if len(array_perf) == len(basic_configurations) and len(array_energy_pack) == len(basic_configurations):
        array_of_arrays_perf.append(array_perf) 
        array_of_arrays_energy_pack.append(array_energy_pack) 
        array_of_BMs.append(data1["BM"][0])
name = "Clustering_Perf"
PlotDendrogram.setup_dendrogram(array_of_arrays_perf, array_of_BMs, name)
name = "HeatMapClust_Perf"
PlotHeatMap.get_order(array_of_arrays_perf, array_of_BMs, basic_configurations, name)
name = "Clustering_energy_pack"
#print(array_of_arrays_energy_pack)
#print(array_of_BMs)
PlotDendrogram.setup_dendrogram(array_of_arrays_energy_pack, array_of_BMs, name)
name = "HeatMapClust_Energy_pack"
PlotHeatMap.get_order(array_of_arrays_energy_pack, array_of_BMs, basic_configurations, name)


