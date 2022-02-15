
import os
import sys

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import string


def print_heatmap(data, y,x, name):
    data = np.asarray(data) 
    fig, ax = plt.subplots(figsize=(20,20))
    im = ax.imshow(data)
    #sns.heatmap(data, annot=True,  linewidths=.1, vmin=0, vmax=2, cmap="Greens")
    sns.heatmap(data, linewidths=.1, vmin=0, vmax=2, cmap="PiYG_r")
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(x)))
    ax.set_yticks(np.arange(len(y)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(x)
    ax.set_yticklabels(y)
    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
    plt.setp(ax.get_yticklabels(), rotation=0, ha="right",
         rotation_mode="anchor")
    
    ax.set_title(name)
    fig.savefig(name, bbox_inches='tight',dpi=200)
    plt.close()

def get_order(data, bms, confs, name):
    lst = []
    with open("bridge_for_clustering.txt", 'r') as reader:
        for line in reader.readlines():
            temp_line = ' '.join(line.split())
            print(temp_line)
            if "[" in temp_line and "]" in temp_line:
                lst.append(temp_line.split("[")[1].split("]")[0].split(" "))
            elif "[" in temp_line:
                lst.append(temp_line.split("[")[1].split(" "))
            elif "]" in temp_line:
                lst.append(temp_line.split("]")[0].split(" "))
            else:
                lst.append(temp_line.split(" "))
    temp_lst = []
    for ls in lst:
        for elem in ls:
            if (elem != ""):
                temp_lst.append(int(elem))
    lst = temp_lst
    ordered_data = []
    ordered_bms = []
    for i in range(len(bms)):
        ordered_data.append([])
        ordered_bms.append([])
    shift = 0
    count = 1
    max_count = max(lst)
    while count < int(max_count) + 1:
        for index, i in enumerate(lst):
            if int(i) == count:
                if len(ordered_data[int(i) -1 + shift]) == 0:
                    ordered_data[int(i) -1 + shift] = data[index]
                    ordered_bms[int(i) -1 + shift] = bms[index]
                else:
                    shift = shift + 1
                    ordered_data[int(i) -1 + shift] = data[index]
                    ordered_bms[int(i) -1 + shift] = bms[index]
        count = count + 1
    print_heatmap(ordered_data, ordered_bms, confs, name)
            
if __name__ == '__main__':
    order = get_order()
    data = sys.arg[1]
    bms = sys.arg[2]
    ordered_data = []
    for i in range(len(bms)):
        ordered_data.append([])
    for index, i in enumerate(order):
        ordered_data[i] = data[index]
