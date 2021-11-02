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


# In[2]:
#We want to have several output graphs:
#Energy vs Perf +
#Energy vs max_Latency
#Energy vs mean_Latency
#Power vs Perf
#Power vs max_Latency
#Power vs mean_Latency

energy_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith("cast.csv") and f.startswith("table_energy"))])
perf_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith("cast.csv") and f.startswith("table_perf"))])
maxl_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith("cast.csv") and f.startswith("table_max_l"))])
meanl_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith("cast.csv") and f.startswith("table_mean_l"))])
wattsp_files = sorted([f for f in listdir(os.getcwd()) if (f.endswith("cast.csv") and f.startswith("table_watts_p"))])
for energy_file, perf_file, maxl_file, meanl_file, wattsp_file in zip(energy_files, perf_files, maxl_files, meanl_files, wattsp_files):
    # Reads data from the first configuration
    print(energy_file)
    original_data1 = pd.read_csv(perf_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data1 = original_data1.stack().reset_index()
    data1.columns = ['BM', 'GC', 'Time']
    replace_data = data1["Time"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data1["Time"] = replace_data

    # Reads data from the second configuration
    original_data2 = pd.read_csv(energy_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data2 = original_data2.stack().reset_index()
    data2.columns = ['BM', 'GC', 'Energy']
    replace_data = data2["Energy"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data2["Energy"] = replace_data

    # Reads data from the 3d configuration
    original_data3 = pd.read_csv(maxl_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data3 = original_data3.stack().reset_index()
    data3.columns = ['BM', 'GC', 'MaxL']
    replace_data = data3["MaxL"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data3["MaxL"] = replace_data
    
    # Reads data from the 4th configuration
    original_data4 = pd.read_csv(meanl_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data4 = original_data4.stack().reset_index()
    data4.columns = ['BM', 'GC', 'MeanL']
    replace_data = data4["MeanL"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data4["MeanL"] = replace_data
    
    # Reads data from the second configuration
    original_data5 = pd.read_csv(wattsp_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data5 = original_data5.stack().reset_index()
    data5.columns = ['BM', 'GC', 'WattsP']
    replace_data = data5["WattsP"]
    for idx, data in enumerate(replace_data):
        if type(data) is str:
            replace_data[idx] = np.nan
    data5["WattsP"] = replace_data

    # Organizes information related to the regions and configurations used
    #configurations = original_data1.columns
    bms1 = original_data1.index
    print(bms1)
    bms2 = original_data2.index
    print(bms2)
    bm = [value for value in bms1 if value in bms2]
    print(bm)
    regions = [["EnerPerf", "PowerPerf"], ["EnerMaxL", "EnerMeanL"], ["PowerMaxL", "PowerMeanL"]]
    
    # In[3]:
    
    
    # Generate scatterplots
    fig,ax = plt.subplots(3,2, figsize=(15, 3*15), gridspec_kw={'width_ratios': [1, 1], 'height_ratios': [1, 1, 1]})
    column_y = ""
    column_x = ""
    for index_x, tuple_region in enumerate(regions):
        for index_y, region in enumerate(tuple_region):
            if "Ener" in region:
                left = data2
                column_y = "Energy"
            elif "Power" in region:
                left = data5
                column_y = "WattsP"
            if "Perf" in region:
                right = data1
                column_x = "Time"
            elif "MaxL" in region:
                right = data3
                column_x = "MaxL"
                ax[index_x][index_y].set(xscale="log")
            elif "MeanL" in region:
                right = data4
                column_x = "MeanL"
                ax[index_x][index_y].set(xscale="log")
            plot_data = pd.merge(left, right, on='GC')
            print(plot_data)
            ax[index_x][index_y].set(title=(f'{column_y} and {column_x}'))
            plt.sca(ax[index_x][index_y])
            sns.scatterplot(data=plot_data, s=300, x=column_x, y=column_y, hue=plot_data['GC'], palette = sns.color_palette('gnuplot', n_colors=len(plot_data['GC']))).get_figure().savefig(str(bm[0]) + ".png")
            #splot.set(xscale="log")
