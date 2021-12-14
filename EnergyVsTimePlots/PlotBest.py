#!/usr/bin/env python
# coding: utf-8

# # Scatterplots: median time vs energy - size 1

# In[1]:

import os
from os import listdir
from os.path import isfile, join
import matplotlib.patches as mpatches
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

#Output
#    x axis - benchmark names
#    y axis - two dots, connected with vertical line; with two versions
BMs = []
vmin = []
vmax = []
legend = []
def find_gaps(data1, data2, time_label, min_heap_size):
    temp_data = data1
    for idx, data in enumerate(data1["GC"]):
        if str(min_heap_size) not in data:
            temp_data.drop(idx, inplace = True)
    data1 = temp_data 
    data1.reset_index(drop=True, inplace=True)
    temp_data = data2
    for idx, data in enumerate(data2["GC"]):
        if str(min_heap_size) not in data:
            temp_data.drop(idx, inplace = True)
    data2 = temp_data 
    data2.reset_index(drop=True, inplace=True)
    if len(data1["GC"] ) != len(data2["GC"]) or data1.empty or data2.empty:
        if data1.empty or data2.empty:
            return
        if len(data1["GC"]) < len(data2["GC"]):
            temp_data = data2
            for idx, GC in enumerate(data2["GC"]):
                found = False
                for GC2 in data1["GC"]:
                    if GC2 == GC:
                        found = True
                        break
                if not found:
                    temp_data.drop(idx, inplace = True)
            data2 = temp_data
        if len(data1["GC"]) > len(data2["GC"]):
            temp_data = data1
            for idx, GC in enumerate(data1["GC"]):
                found = False
                for GC2 in data2["GC"]:
                    if GC2 == GC:
                        found = True
                        break
                if not found:
                    temp_data.drop(idx, inplace = True)
            data1 = temp_data
        if len(data1["GC"] ) != len(data2["GC"]):
            return
    minE = data2["Energy"][0]
    minE_idx = 0
    BMs.append(data1["BM"][0])
    for idx, data in enumerate(data2["Energy"]):
        if data < minE and minE_idx < len(data1[time_label]):
            minE = data
            minE_idx = idx
    minP = data1[time_label][minE_idx]
    minP_idx = minE_idx
    
    for idx, data in enumerate(data1[time_label]):
        if data < minP and idx < len(data2["Energy"]):
            minP = data
            minP_idx = idx
    if data1["GC"][minP_idx] == data2["GC"][minE_idx]:
        vmin.append(0)
        vmax.append(0)
        legend.append(data2["GC"][minE_idx])
    else:
        vmin.append(0) 
        vmax.append(data2["Energy"][minE_idx] - data2["Energy"][minP_idx])
        legend.append(data2["GC"][minE_idx] + " " + data2["GC"][minP_idx])

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
    find_gaps(data1, data2, time_label, min_heap_size)
lines = []
fig, ax = plt.subplots()
clrs = sns.color_palette('gnuplot', n_colors=len(BMs))
for x, y1, y2, leg, clr in zip(BMs, vmin, vmax, legend, clrs):
    if y2 != 0:
        plt.vlines(x, y1, y2, colors=clr, linestyles='solid', label=leg)
    else:
        plt.vlines(x, y1, y2, colors=clr, linestyles='dotted', label=leg)
ax.legend(loc='center left', fancybox=True, ncol=1, bbox_to_anchor=(1, 1.05))
plt.xticks(rotation = 90)
plt.savefig("Best_Gaps", bbox_inches='tight',dpi=100)
#matplotlib.pyplot.vlines(x, ymin, ymax, colors='k', linestyles='solid', label='', *, data=None, **kwargs)
