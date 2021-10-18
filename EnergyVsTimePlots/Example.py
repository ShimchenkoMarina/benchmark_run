#!/usr/bin/env python
# coding: utf-8

# # Scatterplots: median time vs energy - size 1

# In[1]:


import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


# Reads data from the first configuration
original_data1 = pd.read_csv('table_perf.csv', sep=';', index_col="BMs")
# Organizes it for plotting
data1 = original_data1.stack().reset_index()
data1.columns = ['BM', 'GC', 'Time']
#print(data1)

# Reads data from the second configuration
original_data2 = pd.read_csv('table_energy.csv', sep=';', index_col="BMs")
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
    plt.sca(ax[index])
    plt.title(region)
    sns.scatterplot(data=plot_data, x='Time', y='Energy')
plt.savefig("New_plot")
