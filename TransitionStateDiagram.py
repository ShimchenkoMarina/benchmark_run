import numpy as np
from utils.UniqueRuns import UniqueRuns
import matplotlib.pyplot as plt
import os
from os import listdir
from os.path import isfile, join
import gather_data_into_csv
import glob
from matplotlib import rc
basic_configurations = ["j20GZ1.0", "j20GZ1.5", "j20GZ2.0", "j20GZ4.0",
                        "j20YinYanZ1.0", "j20YinYanZ1.5","j20YinYanZ2.0","j20YinYanZ4.0",
                        "j20Z1.0", "j20Z1.5", "j20Z2.0", "j20Z4.0"]
# Identify thred to core placement
def extract_pid(pid, runs, bm, gc_conf):
    imprint = [] # contains P for P-core and E for E-core.
    for file_name in runs:
        if bm in file_name and gc_conf in file_name and "scheduler" in file_name:
            with open(file_name, 'r') as reader:
                for line in reader.readlines():
                    if pid in line:
                        curr_cpu = int(line.split("->")[1])
                        if curr_cpu >=16:
                            imprint.append("E")
                        else:
                            imprint.append("P")
    return imprint

def display(bms, array):
    plt.rcParams["ps.useafm"] = True
    rc('font', **{'family':'sans-serif', 'sans-serif':['FreeSans']})
    plt.rcParams['pdf.fonttype'] = 42 #print(array)
    fig, ax  = plt.subplots(len(bms), 1, sharey = True)
    y_labels = []
    if len(bms)  > 1:
        for i in range(0, len(bms)):
            for j in range(0, len(basic_configurations)):
                #print(array[i][j].count("E"))
                #print(array[i][j].count("P"))
                y_labels.append(array[i][j].count("P")/array[i][j].count("E"))
            ax[i].bar(basic_configurations, y_labels, width=0.5, color="grey")
            ax[i].set_title(bms[i])
            plt.setp(ax[i].get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    else:
        for j in range(0, len(basic_configurations)):
            y_labels.append(array[0][j].count("P")/array[0][j].count("E"))
        ax.bar(basic_configurations, y_labels, width=0.5, color="grey")
        ax.set_title(bms[0])
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    fig.tight_layout()
    fig.savefig("./EnergyVsTimePlots/pngs/PVSE.pdf")

def add_bm(all_bms, this_bm):
    flag = True
    for el in all_bms:
        if el == this_bm:
            flag = False
            break
    if flag:
        all_bms.append(this_bm)
    return all_bms

def find_index(gc):
    for index, el in enumerate(basic_configurations):
        if el == gc:
            return index

# Read the pids of GC threads
def main():
    runs = glob.glob("./results_pids/*/*/*.txt")
    #this array should have the following format:{type: [/home/..../file_pack.txt,file_cpu.txt, file_dram.txt],  }
    bms = []
    gcs = []
    # Creates a list containing 5 lists, each of 8 items, all set to 0
    w, h = len(basic_configurations), 1
    PE_combined = [[0 for x in range(w)] for y in range(h)]
    for file_name in runs:
        res_folder = file_name.split("/")[1]
        bm = file_name.split("/")[2]
        gc_conf = file_name.split("/")[3]
        bms = add_bm(bms, bm)
        #print(res_folder)
        #print(bm)
        #print(gc_conf)
        PE_array = []#array which contains core types: P, E
        if "GC_pids" in file_name:
            with open(file_name, 'r') as reader:
                for line in reader.readlines():
                    pid = line.split(" ")[3].strip()
                    PE_array.extend(extract_pid(pid, runs, bm, gc_conf))
            #print(PE_array)
            PE_combined[len(bms) - 1][find_index(gc_conf)] = PE_array

    display(bms, PE_combined)
main()
