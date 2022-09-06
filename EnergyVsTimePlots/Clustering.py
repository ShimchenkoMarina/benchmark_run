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
basic_configurations_for_spec = ["j20GZ1.0", "j20GZ1.5", "j20GZ2.0", "j20GZ4.0",
                        "j20YinYanZ1.0", "j20YinYanZ1.5","j20YinYanZ2.0","j20YinYanZ4.0"]
basic_configurations_for_hazelcast = ["j20GZ1.0", "j20GZ1.2", "j20GZ1.3", "j20GZ1.5",
                        "j20YinYanZ1.0", "j20YinYanZ1.2","j20YinYanZ1.3","j20YinYanZ1.5"]
                        #"j20Z1.0", "j20Z1.5", "j20Z2.0", "j20Z4.0"]
basic_configurations_for_the_rest = ["j20GZ1.0", "j20GZ1.5", "j20GZ2.0", "j20GZ2.5",
                        "j20YinYanZ1.0", "j20YinYanZ1.5","j20YinYanZ2.0","j20YinYanZ2.5"]
basic_configurations = []

AOAs_perf = []
AOAs_energy = []
AOAs_power = []
AOAs_gc = []
AOAs_stalls = []
AOAs_pause = []
array_of_BMs = []

def fill_in_global_arrays(local_array, what, bm):
    if len(local_array) == len(basic_configurations):
            print("yes")
            return local_array
    else:
            print("Not true for " + bm + " " + what + " with lengts " + str(len(local_array)))
            return []

def fill_in_local_arrays(data):
    global basic_configurations
    local_array = []
    for conf in basic_configurations:
            fail = True
            for index, GC in enumerate(data["GC"]):
                if conf == GC:
                    fail = False
                    local_array.append(data["Time"][index])
                    break
            if fail:
                print("Failed: ", data["BM"][0] + " " + conf)
    return local_array.copy()

def read_data(file_name):
    original_data = pd.read_csv("./tables/" + file_name, sep=';', index_col="BMs")
    # Organizes it for plotting
    data = original_data.stack().reset_index()
    data.columns = ['BM', 'GC', 'Time']
    #replace_data = data["Time"]
    #for idx, data in enumerate(replace_data):
    #    if type(data) is str:
    #        replace_data[idx] = np.nan
    #data["Time"] = replace_data
    return data





def main():
    global AOAs_perf
    global AOAs_energy
    global AOAs_power
    global AOAs_gc
    global AOAs_stalls
    global AOAs_pause
    global array_of_BMs
    global basic_configurations
    energy_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + "static.csv") and f.startswith("table_energy_"))])
    power_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + "static.csv") and f.startswith("table_power"))])
    perf_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + "static.csv") and f.startswith("table_perf"))])
    gc_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + "static.csv") and f.startswith("table_GC"))])
    stalls_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + "static.csv") and f.startswith("table_stalls"))])
    max_pause_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + "static.csv") and f.startswith("table_max_latency"))])

    #for file1, file2 in zip(energy_files, perf_files):
    #    print(file1 + "  --> " + file2)
    for energy_file, perf_file, power_file , gc_file, stalls_file, pause_file in zip(energy_files, perf_files, power_files, gc_files, stalls_files, max_pause_files):
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
        array_pauses = []
        data1 = read_data(perf_file)
        data2 = read_data(energy_file)
        data3 = read_data(power_file)
        data4 = read_data(gc_file)
        data5 = read_data(stalls_file)
        print(data1)
        data6 = read_data(pause_file)
        bm = data5["BM"][0]
        array_of_BMs.append(bm)
        if "spec" in data5["BM"][0]:
            basic_configurations = basic_configurations_for_spec
        elif "hazelcast" in data5["BM"][0]:
            basic_configurations = basic_configurations_for_hazelcast
        else:
            basic_configurations = basic_configurations_for_the_rest
        array_energy = fill_in_local_arrays(data2)
        array_perf = fill_in_local_arrays(data1)
        array_power = fill_in_local_arrays(data3)
        array_gc = fill_in_local_arrays(data4)
        array_stalls = fill_in_local_arrays(data5)
        array_pauses = fill_in_local_arrays(data6)
        AOAs_pause.append(fill_in_global_arrays(array_pauses, "pause", bm))
        AOAs_energy.append(fill_in_global_arrays(array_energy, "energy", bm))
        AOAs_power.append(fill_in_global_arrays(array_power, "power", bm))
        AOAs_perf.append(fill_in_global_arrays(array_perf, "perf", bm))
        AOAs_gc.append(fill_in_global_arrays(array_gc, "gc", bm))
        AOAs_stalls.append(fill_in_global_arrays(array_stalls, "stalls", bm))
        print("gc ", AOAs_gc)
    print_graphs()
    #print("bms", array_of_BMs)
    #print("perf", AOAs_perf)
    #print("energy", AOAs_energy)
    #print(data2)
    #print(data3)
    #print(data4)
    #print(data4["BM"][0])
    #print(len(array_energy))
#for index, bm in enumerate(array_of_BMs):
#    #if "kmeans" in bm:
#        print(AOAs_energy[index])

'''f = open('./all_data/all_data_perf.csv', 'w')
writer = csv.writer(f)
writer.writerow(basic_configurations)
for index, bm in enumerate(array_of_BMs):
    #print(bm)
    row = AOAs_perf[index]
    row.insert(0,bm)
    #print(row)
    writer.writerow(row)
f.close()

f = open('./all_data/all_data_energy.csv', 'w')
writer = csv.writer(f)
writer.writerow(basic_configurations)
for index, bm in enumerate(array_of_BMs):
    row = list(AOAs_energy[index])
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
    row = list(AOAs_power[index])
    row.insert(0,bm)
    #print(row)
    #row.insert(0,bm)
    #print(row)
    writer.writerow(row)
f.close()
'''
def print_graphs():
    global AOAs_perf
    global AOAs_energy
    global AOAs_power
    global AOAs_gc
    global AOAs_stalls
    global AOAs_pause
    global array_of_BMs
    global basic_configurations
    #print("bms", array_of_BMs)
    #print("perf", AOAs_perf)
    #print("energy", AOAs_energy)
    #print("stalls ",AOAs_stalls)
    #print("gc ", AOAs_gc)
    PlotGC.prepare(array_of_BMs, AOAs_gc, AOAs_stalls, AOAs_pause, basic_configurations)
    name = "Clustering_Perf"
    PlotDendrogram.setup_dendrogram(AOAs_perf, array_of_BMs, name)
    name = "HeatMapClust_Perf"
    PlotHeatMap.get_order(AOAs_perf, array_of_BMs, basic_configurations, name)
    #name = "HeatMapClust_Energy_full_perf_order"
    #PlotHeatMap.get_order(AOAs_energy_pack, array_of_BMs, basic_configurations, name)

    name = "Clustering_Energy"
    PlotDendrogram.setup_dendrogram(AOAs_energy, array_of_BMs, name)
    name = "HeatMapClust_Energy"
    PlotHeatMap.get_order(AOAs_energy, array_of_BMs, basic_configurations, name)

    name = "Clustering_Power"
    PlotDendrogram.setup_dendrogram(AOAs_power, array_of_BMs, name)
    name = "HeatMapClust_Power"
    PlotHeatMap.get_order(AOAs_power, array_of_BMs, basic_configurations, name)
main()
