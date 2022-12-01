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
from termcolor import colored
import seaborn as sns

def display_violin(bms, data):
    print(bms)
    fig = plt.figure()
    plt.rcParams["ps.useafm"] = True
    rc('font', **{'family':'sans-serif', 'sans-serif':['FreeSans']})
    plt.rcParams['pdf.fonttype'] = 42
        
    sns.violinplot(data)
    ax = plt.gca()
    #plt.xticks(ticks=np.arange(len(bms)), labels=np.array(bms), rotation=45)
    ax.set_xticklabels(np.array(bms), rotation=90)
    plt.legend()
    fig.tight_layout()
    fig.savefig("./EnergyVsTimePlots/pngs/predicted_workers_" + bms[0][:-4] + ".pdf")
    plt.clf()


# Read the pids of GC threads
def main():
    global threads
    runs = glob.glob("./raw_dir/results_predicted_workers/finagle-chirper_s16/*/predicted_workers/*.txt")
    print(runs)
    #this array should have the following format:{type: [/home/..../file_pack.txt,file_cpu.txt, file_dram.txt],  }
    bms = []
    gcs = []
    # Creates a list containing 5 lists, each of 8 items, all set to 0
    all_data = []
    for file_name in runs:
        res_folder = file_name.split("/")[2]
        bm = file_name.split("/")[3]
        gc_conf = file_name.split("/")[4]
        bms.append(bm + "_" + gc_conf[-3:])
        print(res_folder)
        print(bm)
        print(gc_conf)
        data = []
        with open(file_name, 'r') as reader:
            for line in reader.readlines():
                line =line.replace(",", ".").strip()
                if float(line) < 100 and float(line) > 0:
                    data.append(float(line))
        #print(data)
        #print("\n")
        all_data.append(data)
        data = []
    display_violin(bms, all_data)
main()
