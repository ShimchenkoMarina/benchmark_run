import numpy as np
from utils.UniqueRuns import UniqueRuns
import matplotlib.pyplot as plt
import os
from os import listdir
from os.path import isfile, join
import gather_data_into_csv
import glob
from matplotlib import rc
import multiprocessing
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
threads = {
    "": []
}

def process():
    global threads
    max_thr = len(threads)
    data = []
    lol = []
    how_many_on_E = 0
    how_many_on_P = 0
    for name in threads:
        lol.append(threads[name])
    for i in range(0, len(lol[0])):
        for j in range(0, len(lol)):
            if lol[j][i] >= 16:
                how_many_on_E = how_many_on_E + 1
            else:
                how_many_on_P = how_many_on_P + 1
        data.append(how_many_on_E / max_thr)
        how_many_on_E = 0
        how_many_on_P = 0
    print(data)
    return data

def display_single(bm, gc_conf):
    global threads
    fig = plt.figure()
    plt.rcParams["ps.useafm"] = True
    rc('font', **{'family':'sans-serif', 'sans-serif':['FreeSans']})
    plt.rcParams['pdf.fonttype'] = 42
    # use axis={'both', 'x', 'y'} to choose axis
    plt.locator_params(axis="both", integer=True, tight=True)
    data = process()
    plt.fill_between( x=range(0, len(data)), y1=data, y2= [0] * len(data), color="green", alpha=0.4)
    #plt.plot(data, color= "green")
    plt.legend()
    fig.tight_layout()
    fig.savefig("./EnergyVsTimePlots/pngs/gc_sched_" + bm + "_" + gc_conf + ".pdf")
    plt.clf()

def clean_threads():
    global threads
    threads.clear()

def parse_line(L):
    global threads
    name = L.split(":")[0].strip()
    if "->" in L:
        core = int(L.split(">")[1].strip())
    else:
        core = int(L.split(":")[1].strip())
    flag = False
    for thr in threads:
        if name == thr:
            flag = True
            threads[name].append(core)
    if not flag:
        l = []
        l.append(core)
        threads[name] = l
    return

def print_threads():
    for thr in threads:
        print(thr + " : ", *threads[thr])
    return

# Read the pids of GC threads
def main():
    runs = glob.glob("./results_pids/spec*s8/*/GC_pids.txt")
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
        print(res_folder)
        print(bm)
        print(gc_conf)
        PE_array = []#array which contains core types: P, E
        if "GC_pids" in file_name:
            with open(file_name, 'r') as reader:
                for line in reader.readlines():
                    if "Z" in line and "name" not in line:
                        parse_line(line)
                print_threads()
                display_single(bm, gc_conf)
                clean_threads()
                #print_threads()
main()
