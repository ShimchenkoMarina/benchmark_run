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
basic_configurations = ["j16Z", "j16Ser", "j16G1", "j16Shen", "j16P_n1", "j16P_n2", "j16P_n4", "j13Ser", "j13CMS", "j13P_n1", "j13P_n2", "j13P_n4"]
HEAP_SIZES = {
        "h2_small_t4": "210m",#100min #300m
        "h2_large_t4": "750m",#400min #1200m
        "h2_huge_t4": "2000m", 
        "avrora_large": "27m",#15min #45m
        "fop_default": "75m",#45min #135m
        "jython_large": "75m",#45min #135m
        "luindex_default": "21m",#7min 
        "lusearch_large": "21m", #7min
        "pmd_large": "150m", 
        "sunflow_large": "60m", 
        "xalan_large": "35m", 
        "jme_def": "10m",
        "zxing_def":              "20m",
        "tradesoap_small":        "21m",
        "tradesoap_large":        "27m", 
        "tradesoap_huge":         "27m", 
        "tradesoap_def":          "27m", 
        "graphchi_def":           "700m", 
        "biojava_def":            "525m", 
        "hazelcast":              "5000m", 
        "speckbb2015":            "32g", 
        "als":                    "1455m",#apache-spark485min
        "chi-square":             "1455m",#485min
        "dec-tree":               "1455m",#485min
        "gauss-mix":              "1455m",#485min
        "log-regression":         "1455m",#485min
        "movie-lens":             "1455m",#485min
        "naive-bayes":            "3825m",#1275min(1600m1)
        "page-rank":              "1875m",#625min(835m1)
        "akka-uct":               "705m",#concurrency235min
        "fj-kmeans":              "285m",#95min(150m1)
        "reactors":               "1500m",#500 min(900m1)
        #"db-shootout":            "20m",#database java version <= 11
        #"neo4j-analytics":        "20m", #java version <=15 supported only
        "future-genetic":         "30m",#functional 10min
        "mnemonics":              "180m",#60min
        "par-mnemonics":          "180m",#60min
        #"rx-scrabble":            "35m",#no GC invoke at all
        "scrabble":               "330m",#110min
        "dotty":                  "180m",#scala 60min
        "philosophers":           "30m",#10min
        "scala-doku":             "105m",#35min
        "scala-kmeans":           "105m",#35min
        "scala-stm-bench7":       "930m",#310min
        "finagle-chirper":        "180m",#web 60m min
        "finagle-http":           "105m",#35min
}

def find_heap_size(bm_name):
    for (bm, size) in HEAP_SIZES.items():
        if bm_name in bm:
            return size

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
for energy_pack_file, perf_file, meanl_file in zip(energy_pack_files, perf_files, meanl_files):
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
    
    time_label = "Time"
    if "hazelcast" in data1['BM'][0]:
        # Reads data from the first configuration
        original_data1 = pd.read_csv(meanl_file, sep=';', index_col="BMs")
        # Organizes it for plotting
        data1 = original_data1.stack().reset_index()
        data1.columns = ['BM', 'GC', 'MeanL']
        replace_data = data1["MeanL"]
        for idx, data in enumerate(replace_data):
            if type(data) is str:
                replace_data[idx] = np.nan
        data1["MeanL"] = replace_data
        time_label = "MeanL"

    #Figure the basic configurations
    #Find default heap size
    min_heap_size = find_heap_size(data1['BM'][0])
    for conf in basic_configurations:
            for index, GC in enumerate(data1["GC"]):
                if conf + str(min_heap_size) in GC and "P" not in GC:
                    array_perf.append(data1[time_label][index])
                    break
                if "P" in GC and conf[:4] + str(min_heap_size) in GC:
                    array_perf.append(data1[time_label][index])
                    break
            for index, GC in enumerate(data2["GC"]):
                if conf + str(min_heap_size) in GC and "P" not in GC:
                    array_energy_pack.append(data2["Energy"][index])
                    break
                if "P" in GC and conf[:4] + str(min_heap_size) in GC:
                    array_energy_pack.append(data2["Energy"][index])
                    break
    if len(array_perf) == len(basic_configurations) and len(array_energy_pack) == len(basic_configurations):
        array_of_arrays_perf.append(array_perf) 
        array_of_arrays_energy_pack.append(array_energy_pack) 
        array_of_BMs.append(data1["BM"][0])
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

