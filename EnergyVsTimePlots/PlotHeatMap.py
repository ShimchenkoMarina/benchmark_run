
import os
import sys

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import string
from matplotlib import colors
from matplotlib import rc

def print_heatmap(data, y,x, name):
    plt.rcParams["ps.useafm"] = True
    rc('font', **{'family':'sans-serif', 'sans-serif':['FreeSans']})
    plt.rcParams['pdf.fonttype'] = 42 #print(array)
    data = np.asarray(data)
    min_v = np.min(data)
    max_v = np.max(data)
    if max_v <= 1:
        max_v = 1.01
    if min_v >= 1:
        min_v = 0.99
    #print(name)
    #print("max is", max_v)
    #print("min is", min_v)
    #print("data is ", data)
    #print("len = " + str(len(x)))
    NUM = int(len(x) / 2)
    #NUM = int(len(x))
    fig, axs = plt.subplots(1, NUM, sharey=True, figsize=(len(x)/2,len(y)))
    divnorm=colors.TwoSlopeNorm(vcenter=1.0, vmax=max_v, vmin=min_v)
    for i in range(0, NUM):
        #print("part data is ", data[:, i*1:i*1 + 1])
        a1 = axs[i].imshow(data[:,i*1:i*1 +1 ], cmap="PiYG_r",
            norm=divnorm, aspect='auto',
            interpolation='nearest', extent=(0, 1, len(y), 0))
        #a1 = axs[i].imshow(data[:, i:i + 1], cmap="PiYG_r",
        #    norm=divnorm, aspect='auto',
        #    interpolation='nearest', extent=(0, 1, len(y), 0))
        axs[i].set_xticks(np.arange(1))
        axs[i].set_yticks(np.arange(len(y)))
        axs[i].set_xticklabels(x[i*1:i*1 + 1])
        axs[i].set_yticklabels(y)
        axs[i].xaxis.grid(True)
        start = 0
        #if i == 0:
        #    start = 1
        #else:
        #    start = 0
        #print(data)
        for j in range(start,1):
            for k in range(0,len(y)):
                print(str(k) + " j = " + str(j) + " i ="  + str(i))
                print("single data ", data[k:k + 1, (i*1 + j):(i*1 + j + 1)])
                axs[i].text(j + 0.5, k + 0.5, data[k:k + 1, i*1 + j:i*1 + j + 1][0][0], ha="center", va="center", color="black")
        #axs[i].grid(color='grey', linestyle='-', linewidth=1)
        # Rotate the tick labels and set their alignment.
        plt.setp(axs[i].get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
        plt.setp(axs[i].get_yticklabels(), rotation=0, ha="right",
             rotation_mode="anchor")
    #im = ax.imshow(data)
    #sns.heatmap(data, annot=True,  linewidths=.1, vmin=0, vmax=10, cmap="Greens")
    #sns.heatmap(data, linewidths=.1, vmin=0, vmax=2, cmap="PiYG")
    # We want to show all ticks...
    for ax,l in zip(axs,["1x", "1.5", "2x", "4x"]):
        ax.set_xticklabels([])
        ax.set_xlabel(l)
    plt.colorbar(a1)
    #axs.set_xticks(np.arange(len(x)))
    #axs.set_yticks(np.arange(len(y)))
    # ... and label them with the respective list entries
    #axs.set_xticklabels(x)
    #axs.set_yticklabels(y)


    #axs.set_title(name)
    fig.savefig("./pngs/" + name + ".pdf", bbox_inches='tight',dpi=200)
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
    if len(lst) > 1:
        for i in range(len(bms)):
            ordered_data.append([])
            ordered_bms.append([])
        shift = 0
        count = 1
        if len(lst) != 0:
            max_count = max(lst)
        while count < int(max_count) + 1:
            for index, i in enumerate(lst):
                if int(i) == count:
                    if len(ordered_data[int(i) -1 + shift]) == 0:
                        ordered_data[int(i) -1 + shift] = data[index]
                        ordered_bms[int(i) -1 + shift] = bms[index]
                    else:
                        shift = shift + 1
                        print(ordered_data)
                        print(int(i) - 1 + shift)
                        print(data)
                        print(index)
                        ordered_data[int(i) -1 + shift] = data[index]
                        ordered_bms[int(i) -1 + shift] = bms[index]
            count = count + 1
        print_heatmap(data, bms, confs, name)
    elif len(lst) == 1:
        print(data)
        ordered_bms = bms
        ordered_confs, ordered_data_0 = zip(*sorted(zip(confs, data[0])))
        ordered_data = []
        ordered_data.append(ordered_data_0)
        print(ordered_data)
        print(ordered_confs)
        print_heatmap(ordered_data, ordered_bms, ordered_confs, name)

if __name__ == '__main__':
    order = get_order()
    data = sys.arg[1]
    bms = sys.arg[2]
    ordered_data = []
    for i in range(len(bms)):
        ordered_data.append([])
    for index, i in enumerate(order):
        ordered_data[i] = data[index]
