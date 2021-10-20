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


energy_files = [f for f in listdir(os.getcwd()) if (f.endswith(".csv") and f.startswith("table_energy"))]
energy_files = sorted(energy_files)
perf_files = [f for f in listdir(os.getcwd()) if (f.endswith(".csv") and f.startswith("table_perf"))]
perf_files = sorted(perf_files)
for energy_file, perf_file in zip(energy_files, perf_files):
    # Reads data from the first configuration
    original_data1 = pd.read_csv(perf_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data1 = original_data1.stack().reset_index()
    data1.columns = ['BM', 'GC', 'Time']
    
    # Reads data from the second configuration
    original_data2 = pd.read_csv(energy_file, sep=';', index_col="BMs")
    # Organizes it for plotting
    data2 = original_data2.stack().reset_index()
    data2.columns = ['BM', 'GC', 'Energy']
    
    # Organizes information related to the regions and configurations used
    configurations = original_data1.columns
    regions1 = original_data1.index
    regions2 = original_data2.index
    regions = [value for value in regions1 if value in regions2]
    
    
    # In[3]:
    
    
    # Generate scatterplots
    fig,ax = plt.subplots(len(regions),1, figsize=(10,len(regions)*15))
    for index, region in enumerate(regions):
        left = data1[(data1['BM'] == region)]
        right = data2[(data2['BM'] == region)]
        plot_data = pd.merge(left, right, on='GC')
        plt.sca(ax)
        plt.title(region)
        sns.scatterplot(data=plot_data, s=300, x='Time', y='Energy', hue=plot_data['GC'], palette = sns.color_palette("ch:s=.25,rot=-.25", n_colors=len(plot_data['GC'])))
        plt.savefig(region)
