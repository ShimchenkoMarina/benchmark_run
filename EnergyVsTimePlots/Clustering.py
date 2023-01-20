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
basic_configurations = ["j20Z", "j20Z_CPUO1", "j20Z_CPUO2", "j20Z_CPUO5","j20Z_CPUO10"]
#basic_configurations = ["j20Z", "j20Z_CPUO1", "j20Z_CPUO2", "j20Z_CPUO5","j20Z_CPUO10", "j20Z_CPUO15", "j20Z_CPUO20", "j20Z_CPUO45"]
#basic_configurations = ["j20Z", "j20Z_CPUO5","j20Z_CPUO10", "j20Z_CPUO15", "j20Z_CPUO20", "j20Z_CPUO45"]
#basic_configurations = []

AOAs_perf = []
AOAs_energy = []
AOAs_power = []
AOAs_memory = []
AOAs_pause = []
AOAs_gc = []
AOAs_soft_max = []
array_of_BMs = []

def fill_in_global_arrays( local_array, what, bm):
    global dict
    print(what)
    if int(len(local_array)) == int(len(basic_configurations)):
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
    empty_array = [0] * int(len(array) /2)
    empty_array = [round((item2/ item1), 2) for item1, item2 in  zip(array[::2], array[1::2])]
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
        print(data.empty)
        if not data.empty:
            print(data)
            bm = data["BM"][0]
            add_BM(bm)
            print(bm)
            array_local = fill_in_local_arrays(data)
            array_global.append(fill_in_global_arrays( array_local, array_type, bm))

def main_bm(BM):
    global AOAs_perf
    global AOAs_energy
    global AOAs_power
    global AOAs_memory
    global AOAs_pause
    global AOAs_gc
    global AOAs_soft_max
    global array_of_BMs
    global basic_configurations

    total_energy_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_total_energy_" + BM))])
    average_power_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_average_power_" + BM))])
    perf_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_perf_" + BM))])
    memory_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_memory_" + BM))])
    latency_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_max_latency_" + BM))])
    gc_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_gc_" + BM))])
    soft_max_files = sorted([f for f in listdir(os.getcwd() + "/tables/") if (f.endswith(bench + ".csv") and f.startswith("table_soft_max_capacity_" + BM))])
    #print(soft_max_files)
    process_files(total_energy_files, AOAs_energy, "total_energy")
    process_files(perf_files, AOAs_perf, "perf")
    process_files(latency_files, AOAs_pause, "latency")
    process_files(average_power_files, AOAs_power, "average_power")
    process_files(memory_files, AOAs_memory, "memory")
    process_files(gc_files, AOAs_gc, "gc")
    process_files(soft_max_files, AOAs_soft_max, "soft_max_capacity")

    #print("gc ", AOAs_energy)
    print_graphs(BM)

def main():
    for bm in ["h2_small"]:
        main_bm(bm)

def print_graphs(bm):
    global AOAs_perf
    global AOAs_energy
    global AOAs_power
    global AOAs_memory
    global AOAs_pause
    global AOAs_gc
    global AOAs_soft_max
    global array_of_BMs
    global basic_configurations
    #Soft Max Capacity
    #-----------------------------
    bms = []
    data = []
    for x, y in zip(array_of_BMs, AOAs_soft_max):
        if y != []:
            bms.append(x)
            data.append(y)
    print(bms)
    print(data)
    PlotBars.prepare(bms, data, basic_configurations, "Soft_Max")
    #---------------------------
    #GC
    bms = []
    data = []
    for x, y in zip(array_of_BMs, AOAs_gc):
        if y != []:
            bms.append(x)
            data.append(y)
    PlotBars.prepare(bms, data, basic_configurations, "GC")
    #Perf
    #-----------------------------
    bms = []
    data = []
    for x, y in zip(array_of_BMs, AOAs_perf):
        if y != []:
            bms.append(x)
            data.append(y)
    #---------------------------
    name = "Clustering_Perf"
    #print(array_of_BMs)
    if len(array_of_BMs) > 1:
        PlotDendrogram.setup_dendrogram(data, bms, name)
    name = "HeatMapClust_Perf"
    PlotHeatMap.get_order(data, bms, basic_configurations, name)
    #Energy
    #-----------------------------
    bms = []
    data = []
    for x, y in zip(array_of_BMs, AOAs_energy):
        if y != []:
            bms.append(x)
            data.append(y)
    #---------------------------
    name = "Clustering_Energy"
    if len(array_of_BMs) > 1:
        PlotDendrogram.setup_dendrogram(data, bms, name)
    name = "HeatMapClust_Energy"
    PlotHeatMap.get_order(data, bms, basic_configurations, name)
    #Power
    #-----------------------------
    bms = []
    data = []
    for x, y in zip(array_of_BMs, AOAs_power):
        if y != []:
            bms.append(x)
            data.append(y)
    #---------------------------
    name = "Clustering_Power"
    if len(array_of_BMs) > 1:
        PlotDendrogram.setup_dendrogram(data, bms, name)
    name = "HeatMapClust_Power"
    PlotHeatMap.get_order(data, bms, basic_configurations, name)
    #Memory
    #-----------------------------
    bms = []
    data = []
    for x, y in zip(array_of_BMs, AOAs_memory):
        if y != []:
            bms.append(x)
            data.append(y)
    #---------------------------
    #print(data)
    name = "Clustering_Memory"
    if len(array_of_BMs) > 1:
        PlotDendrogram.setup_dendrogram(data, bms, name)
    name = "HeatMapClust_Memory"
    PlotHeatMap.get_order(data, bms, basic_configurations, name)

main()
