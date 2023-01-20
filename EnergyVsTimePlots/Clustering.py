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
import PlotBars
# In[2]:
bench = ""
#TODO: and P_def
#basic_configurations_for_spec = ["j20GZ1.0", "j20GZ1.5", "j20GZ2.0", "j20GZ4.0",
#                        "j20YinYanZ1.0", "j20YinYanZ1.5","j20YinYanZ2.0","j20YinYanZ4.0"]
#basic_configurations_for_spec = ["j20GZ1.0", "j20YinYanZ1.0", "j20MARKZ1.0", "j20GZ1.5", "j20YinYanZ1.5", "j20MARKZ1.5","j20GZ2.0", "j20YinYanZ2.0","j20MARKZ2.0", "j20GZ4.0","j20YinYanZ4.0", "j20MARKZ4.0"]
#basic_configurations_for_spec = ["j20GZ1.0", "j20YinYanZ1.0", "j20GZ1.5", "j20YinYanZ1.5","j20GZ2.0", "j20YinYanZ2.0", "j20GZ4.0","j20YinYanZ4.0"]
#basic_configurations_for_hazelcast = ["j20GZ1.0", "j20YinYanZ1.0", "j20GZ1.2", "j20YinYanZ1.2","j20GZ1.3", "j20YinYanZ1.3","j20GZ1.5","j20YinYanZ1.5"]
#basic_configurations_for_the_rest = ["j20GZ1.0", "j20YinYanZ1.0", "j20GZ1.5", "j20YinYanZ1.5","j20GZ2.0", "j20YinYanZ2.0","j20GZ2.5","j20YinYanZ2.5"]
#basic_configurations_for_hazelcast = ["j20GZ1.0", "j20GZ1.2", "j20GZ1.3", "j20GZ1.5",
#                        "j20YinYanZ1.0", "j20YinYanZ1.2","j20YinYanZ1.3","j20YinYanZ1.5"]
                        #"j20Z1.0", "j20Z1.5", "j20Z2.0", "j20Z4.0"]
#basic_configurations_for_the_rest = ["j20GZ1.0", "j20GZ1.5", "j20GZ2.0", "j20GZ2.5",
#                        "j20YinYanZ1.0", "j20YinYanZ1.5","j20YinYanZ2.0","j20YinYanZ2.5"]
basic_configurations_for_the_rest = ["GZ1.0_8P", "GZ1.5_8P", "GZ2.0_8P", "GZ1.0_4E4E", "GZ1.5_4E4E", "GZ2.0_4E4E", "YYZ1.0_4E4E", "YYZ1.5_4E4E", "YYZ2.0_4E4E"]
basic_configurations = []

AOAs_perf = []
AOAs_energy = []
AOAs_power = []
AOAs_gc = []
AOAs_stalls = []
AOAs_pause = []
AOAs_latency = []
AOAs_cpu = []
AOAs_alloc_avg = []
AOAs_alloc_max = []
array_of_BMs = []

dict = {"energy": 0,
        "perf": 1,
        "power": 2,
        "latency": 3,
        "cpu_util": 24,
        "alloc_avg": 25,
        "alloc_max": 26,
        "gc": 21,
        "stalls": 23}

def fill_in_global_arrays(local_array, what, bm):
    global dict
    print(what)
    if dict[what] > 20:
        if int(len(local_array)) == int(len(basic_configurations)):
            #print("yes")
            return local_array
        else:
            print("Not true for " + bm + " " + what + " with lengts " + str(len(local_array)) + "/" + str(len(basic_configurations)))
            return []
    else:
        if int(len(local_array)) == int(len(basic_configurations) - 3):
            #print("yes")
            return local_array
        else:
            print("Not true for " + bm + " " + what + " with lengts " + str(len(local_array)) + "/" + str(len(basic_configurations)))
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
    return data

def renormalize(array):
    empty_array = [0] * int(len(array) - 3)
    #empty_array = [round((item2/ item1), 2) for item1, item2 in  zip(array[::2], array[1::2])]
    empty_array[0] = round(array[3]/array[0], 2)
    empty_array[1] = round(array[4]/array[1], 2)
    empty_array[2] = round(array[5]/array[2], 2)
    empty_array[3] = round(array[6]/array[0], 2)
    empty_array[4] = round(array[7]/array[1], 2)
    empty_array[5] = round(array[8]/array[2], 2)
    #print(empty_array)
    return empty_array

def add_BM(BM):
    global array_of_BMs
    array_of_BMs.append(BM) if BM not in array_of_BMs else array_of_BMs

def process_files(files, array_global, array_type):
    global basic_configurations
    global dict
    for f in files:
        print(f)
        array_local = []
        data = read_data(f)
        bm = data["BM"][0]
        print(bm)
        add_BM(bm)
        #if "spec" in bm:
        #    basic_configurations = basic_configurations_for_spec
        #elif "hazelcast" in bm:
        #    basic_configurations = basic_configurations_for_hazelcast
        #else:
        basic_configurations = basic_configurations_for_the_rest
        if dict[array_type] < 21:
            array_local = renormalize(fill_in_local_arrays(data))
        else:
            array_local = fill_in_local_arrays(data)
        array_global.append(fill_in_global_arrays(array_local, array_type, bm))

def main_bm(BM):
    global AOAs_perf
    global AOAs_energy
    global AOAs_power
    global AOAs_gc
    global AOAs_stalls
    global AOAs_pause
    global AOAs_latency
    global AOAs_cpu
    global AOAs_alloc_avg
    global AOAs_alloc_max
    global array_of_BMs
    global basic_configurations

    energy_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_energy_" + BM))])
    power_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_power_" + BM))])
    perf_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_perf_" + BM))])
    #gc_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_GC_cycles_" + BM))])
    #stalls_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_stalls_" + BM))])
    #max_pause_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_pause_" + BM))])
    latency_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_latency_" + BM))])
    cpu_util_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_cpu_utilization_" + BM))])
    #allocation_rate_avg_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_allocation_rate_avg_" + BM))])
    #allocation_rate_max_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_allocation_rate_max_" + BM))])

    process_files(energy_files, AOAs_energy, "energy")
    process_files(perf_files, AOAs_perf, "perf")
    #process_files(max_pause_files, AOAs_pause, "pause")
    process_files(latency_files, AOAs_latency, "latency")
    process_files(power_files, AOAs_power, "power")
    #process_files(gc_files, AOAs_gc, "gc")
    #process_files(stalls_files, AOAs_stalls, "stalls")
    process_files(cpu_util_files, AOAs_cpu, "cpu_util")
    #process_files(allocation_rate_avg_files, AOAs_alloc_avg, "alloc_avg")
    #process_files(allocation_rate_max_files, AOAs_alloc_max, "alloc_max")


    #print("gc ", AOAs_pause)
    print_graphs(BM)
    #print_paper_graphs(BM)
    #for file1, file2 in zip(energy_files, perf_files):
    #    print(file1 + "  --> " + file2)
    '''for energy_file, perf_file, power_file , gc_file, stalls_file, pause_file in zip(energy_files, perf_files, power_files, gc_files, stalls_files, max_pause_files):
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
        #print(data1)
        data6 = read_data(pause_file)
        bm = data5["BM"][0]
        array_of_BMs.append(bm)
        if "spec" in data5["BM"][0]:
            basic_configurations = basic_configurations_for_spec
        elif "hazelcast" in data5["BM"][0]:
            basic_configurations = basic_configurations_for_hazelcast
        else:
            basic_configurations = basic_configurations_for_the_rest
        array_energy = renormalize(fill_in_local_arrays(data2))
        array_perf = renormalize(fill_in_local_arrays(data1))
        array_power = renormalize(fill_in_local_arrays(data3))
        array_gc = fill_in_local_arrays(data4)
        array_stalls = fill_in_local_arrays(data5)
        array_pauses = fill_in_local_arrays(data6)
        AOAs_pause.append(fill_in_global_arrays(array_pauses, "pause", bm))
        AOAs_energy.append(fill_in_global_arrays(array_energy, "energy", bm))
        AOAs_power.append(fill_in_global_arrays(array_power, "power", bm))
        AOAs_perf.append(fill_in_global_arrays(array_perf, "perf", bm))
        AOAs_gc.append(fill_in_global_arrays(array_gc, "gc", bm))
        AOAs_stalls.append(fill_in_global_arrays(array_stalls, "stalls", bm))'''
    #print("gc ", AOAs_alloc_avg)
    #print("gc ", AOAs_alloc_max)
    #print("gc ", AOAs_gc)
    #print("gc ", AOAs_stalls)
    #print("gc ", AOAs_pause)
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

def main():
    for bm in ["jme"]:
        #init()
        main_bm(bm)

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

def print_as_is(bm):
    global AOAs_perf
    global AOAs_energy
    global AOAs_power
    global AOAs_gc
    global AOAs_stalls
    global AOAs_pause
    global AOAs_latency
    global AOAs_cpu
    global AOAs_alloc_avg
    global AOAs_alloc_max
    global array_of_BMs
    global basic_configurations
    name = "Energy_" + bm
    PlotHeatMap.print_as_is(AOAs_energy, basic_configurations, array_of_BMs, name)

def print_paper_graphs(bm):
    global AOAs_perf
    global AOAs_energy
    global AOAs_power
    global AOAs_gc
    global AOAs_stalls
    global AOAs_pause
    global AOAs_latency
    global AOAs_cpu
    global AOAs_alloc_avg
    global AOAs_alloc_max
    global array_of_BMs
    global basic_configurations
    print("energy", AOAs_energy)
    print("power", AOAs_power)
    print("BMs", array_of_BMs)
    name = "Energy_Power_Latency_" + bm
    PlotHeatMap.print_paper_heatmap(AOAs_energy, AOAs_power, AOAs_perf, "enough", basic_configurations, array_of_BMs, name)

def print_graphs(bm):
    global AOAs_perf
    global AOAs_energy
    global AOAs_power
    global AOAs_gc
    global AOAs_stalls
    global AOAs_pause
    global AOAs_latency
    global AOAs_cpu
    global AOAs_alloc_avg
    global AOAs_alloc_max
    global array_of_BMs
    global basic_configurations
    #print("bms", array_of_BMs)
    #print("perf", AOAs_perf)
    print("energy", AOAs_energy)
    #print("stalls ",AOAs_stalls)
    #print("gc ", AOAs_gc)
    #PlotBars.prepare(array_of_BMs, AOAs_cpu, AOAs_alloc_avg, AOAs_alloc_max, basic_configurations, bm + "_util_alloc",
    #                 "cpu_utilization", "allocation_rate_avg", "allocation_rate_max", "")
    #PlotBars.prepare(array_of_BMs, AOAs_gc, AOAs_stalls, AOAs_pause, basic_configurations, bm + "_latency_gc",
    #                 "gc_cycles", "stalls", "pause", "norm")
    
    #Energy, Perf, Power
    name = "Clustering_Perf_" +bm
    if len(array_of_BMs) > 1:
        PlotDendrogram.setup_dendrogram(AOAs_perf, array_of_BMs, name)
    name = "HeatMapClust_Perf_" + bm
    PlotHeatMap.get_order(AOAs_perf, array_of_BMs, basic_configurations, name)

    name = "Clustering_Energy_" + bm
    if len(array_of_BMs) > 1:
        PlotDendrogram.setup_dendrogram(AOAs_energy, array_of_BMs, name)
    name = "HeatMapClust_Energy_" + bm
    PlotHeatMap.get_order(AOAs_energy, array_of_BMs, basic_configurations, name)

    name = "Clustering_Power_" + bm
    if len(array_of_BMs) > 1:
        PlotDendrogram.setup_dendrogram(AOAs_power, array_of_BMs, name)
    name = "HeatMapClust_Power_" + bm
    PlotHeatMap.get_order(AOAs_power, array_of_BMs, basic_configurations, name)
    
    #Latency
    name = "Clustering_Latency_" + bm
    if len(array_of_BMs) > 1:
        PlotDendrogram.setup_dendrogram(AOAs_latency, array_of_BMs, name)
    name = "HeatMapClust_Latency_" + bm
    PlotHeatMap.get_order(AOAs_latency, array_of_BMs, basic_configurations, name)

main()
