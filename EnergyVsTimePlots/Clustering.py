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
import PlotGC
# In[2]:
bench = ""
#TODO: and P_def
basic_configurations = ["j20GZ1.0", "j20GZ1.5", "j20GZ2.0", "j20GZ4.0",
                        "j20YinYanZ1.0", "j20YinYanZ1.5","j20YinYanZ2.0","j20YinYanZ4.0"]
                        #"j20Z1.0", "j20Z1.5", "j20Z2.0", "j20Z4.0"]

energy_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_energy_"))])
power_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_power"))])
perf_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_perf"))])
gc_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_GC"))])
stalls_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_stalls"))])
array_of_arrays_perf = []
array_of_arrays_energy = []
array_of_arrays_power = []
array_of_arrays_gc = []
array_of_arrays_stalls = []
array_of_BMs = []
for file1, file2 in zip(energy_files, perf_files):
    print(file1 + "  --> " + file2)
for energy_file, perf_file, power_file , gc_file, stalls_file in zip(energy_files, perf_files, power_files, gc_files, stalls_files):
    #print(energy_file)
    #print(perf_file)
    #print(power_file)
    #print(gc_file)
    #print(stalls_file)
    array_perf = []
    array_energy = []
    array_power = []
    array_gc = []
    array_stalls = []
    # Reads data from the first configuration
    original_data1 = pd.read_csv("./tables/" + perf_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data1 = original_data1.stack().reset_index()
    data1.columns = ['BM', 'GC', 'Time']
    replace_data = data1["Time"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data1["Time"] = replace_data
    print(data1["BM"][0])

    #if "hazel" not in data1['BM'][0] and "avrora" not in data1['BM'][0] and "spec" not in data1['BM'][0]:
    #    continue
    original_data2 = pd.read_csv("./tables/" + energy_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data2 = original_data2.stack().reset_index()
    data2.columns = ['BM', 'GC', 'Energy']
    replace_data = data2["Energy"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data2["Energy"] = replace_data
    # Reads power
    original_data3 = pd.read_csv("tables/" + power_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data3 = original_data3.stack().reset_index()
    data3.columns = ['BM', 'GC', 'Power']
    replace_data = data3["Power"]
    for idx, data in enumerate(replace_data):
            if type(data) is str:
                replace_data[idx] = np.nan
    data3["Power"] = replace_data

    # Reads gc
    original_data4 = pd.read_csv("tables/" + gc_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data4 = original_data4.stack().reset_index()
    data4.columns = ['BM', 'GC', 'Cycles']
    replace_data = data4["Cycles"]
    for idx, data in enumerate(replace_data):
            if type(data) is str:
                replace_data[idx] = np.nan
    data3["Cycles"] = replace_data

    # Reads stalls
    original_data5 = pd.read_csv("tables/" + stalls_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data5 = original_data5.stack().reset_index()
    data5.columns = ['BM', 'GC', 'Stalls']
    replace_data = data5["Stalls"]
    for idx, data in enumerate(replace_data):
            if type(data) is str:
                replace_data[idx] = np.nan
    data5["Stalls"] = replace_data

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
                    array_energy.append(data2["Energy"][index])
                    break
            for index, GC in enumerate(data3["GC"]):
                if conf == GC:
                    array_power.append(data3["Power"][index])
                    break
            for index, GC in enumerate(data4["GC"]):
                if conf == GC:
                    array_gc.append(data4["Cycles"][index])
                    break
            for index, GC in enumerate(data5["GC"]):
                if conf == GC:
                    array_stalls.append(data5["Stalls"][index])
                    break
    #print(data2)
    #print(data3)
    #print(data4)
    #print(data4["BM"][0])
    #print(len(array_energy))
    if len(array_energy) == len(basic_configurations):
            array_of_arrays_energy.append(array_energy)
            array_of_BMs.append(data1["BM"][0])
    if len(array_power) == len(basic_configurations):
            array_of_arrays_power.append(array_power)
    if len(array_perf) == len(basic_configurations):
            array_of_arrays_perf.append(array_perf)
    if len(array_gc) == len(basic_configurations):
            array_of_arrays_gc.append(array_gc)
    if len(array_stalls) == len(basic_configurations):
            array_of_arrays_stalls.append(array_stalls)
    else:
            #print(array_energy_pack)
            print("Not true for " + data1["BM"][0])
for index, bm in enumerate(array_of_BMs):
    #if "kmeans" in bm:
        print(array_of_arrays_energy[index])

'''f = open('./all_data/all_data_perf.csv', 'w')
writer = csv.writer(f)
writer.writerow(basic_configurations)
for index, bm in enumerate(array_of_BMs):
    #print(bm)
    row = array_of_arrays_perf[index]
    row.insert(0,bm)
    #print(row)
    writer.writerow(row)
f.close()

f = open('./all_data/all_data_energy.csv', 'w')
writer = csv.writer(f)
writer.writerow(basic_configurations)
for index, bm in enumerate(array_of_BMs):
    row = list(array_of_arrays_energy[index])
    row.insert(0,bm)
    #print(row)
    #row.insert(0,bm)
    #print(row)
    writer.writerow(row)
f.close()

f = open('./all_data/all_data_power.csv', 'w')
writer = csv.writer(f)
writer.writerow(basic_configurations)
for index, bm in enumerate(array_of_BMs):
    row = list(array_of_arrays_power[index])
    row.insert(0,bm)
    #print(row)
    #row.insert(0,bm)
    #print(row)
    writer.writerow(row)
f.close()
'''
#print(array_of_BMs)
#print(array_of_arrays_perf)
#print(array_of_arrays_energy)
#print("stalls ",array_of_arrays_stalls)
#print("gc ", array_of_arrays_gc)
PlotGC.plot(array_of_BMs, array_of_arrays_gc, array_of_arrays_stalls, basic_configurations)
name = "Clustering_Perf"
PlotDendrogram.setup_dendrogram(array_of_arrays_perf, array_of_BMs, name)
name = "HeatMapClust_Perf"
PlotHeatMap.get_order(array_of_arrays_perf, array_of_BMs, basic_configurations, name)
#name = "HeatMapClust_Energy_full_perf_order"
#PlotHeatMap.get_order(array_of_arrays_energy_pack, array_of_BMs, basic_configurations, name)

name = "Clustering_Energy"
PlotDendrogram.setup_dendrogram(array_of_arrays_energy, array_of_BMs, name)
name = "HeatMapClust_Energy"
PlotHeatMap.get_order(array_of_arrays_energy, array_of_BMs, basic_configurations, name)

name = "Clustering_Power"
PlotDendrogram.setup_dendrogram(array_of_arrays_power, array_of_BMs, name)
name = "HeatMapClust_Power"
PlotHeatMap.get_order(array_of_arrays_power, array_of_BMs, basic_configurations, name)

