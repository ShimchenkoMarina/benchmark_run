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
import csv

def read_data(name):
    array_of_BMs = []
    array_of_arrays_features = []
    Ar_keys = []
    Ar_keys.append("BM")
    flag = "clean"

    with open('all_data_' + name + '.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            temp = []
            x = row.keys() 
            for key in x:
                if key == "BMs":
                    array_of_BMs.append(row[key])
                else:
                    if flag == "clean":
                        Ar_keys.append(key)
                    temp.append(row[key])
            flag = "dirty"
            array_of_arrays_features.append(temp)
    #print(Ar_keys)
    return array_of_arrays_features, array_of_BMs, Ar_keys

def norm_per_BM(data, BMs, GCs, name):
    for i in range(1, len(data[0])):
        temp = []
        for bm in data:
            temp.append(bm[i])
        temp = np.array(temp).astype(np.float64)
        maxN = np.amax(temp)
        for index, el in enumerate(temp):
            temp[index] = el / maxN
        for index, bm in enumerate(data):
            data[index][i] = temp[index]
    
    f = open('./norm_data/all_data_' + name + '_norm_per_BM.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(GCs)
    for index, bm in enumerate(BMs):
        row = data[index]
        row.insert(0,bm)
        writer.writerow(row)
    f.close()


def norm_per_GC(data, BMs, GCs, name):
    for index, bm in enumerate(data):
        temp = np.array(bm).astype(np.float64)
        maxN = np.amax(temp)
        for index_x, el in enumerate(bm):
            data[index][index_x] = float(el) / maxN
    
    f = open('./norm_data/all_data_'+ name + '_norm_per_GC.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(GCs)
    for index, bm in enumerate(BMs):
        row = data[index]
        row.insert(0,bm)
        writer.writerow(row)
    f.close()

def norm_per_G1(data, BMs, GCs, name):
    index_G1 = 0
    for index, key in enumerate(GCs):
        if "G11.0" in key:
            index_G1 = index
            break
    for index, bm in enumerate(data):
        temp = np.array(bm).astype(np.float64)
        maxN = temp[index_G1 - 1]
        for index_x, el in enumerate(bm):
            data[index][index_x] = maxN / float(el)
    
    f = open('./norm_data/all_data_'+ name+'_norm_G1.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(GCs)
    for index, bm in enumerate(BMs):
        row = data[index]
        row.insert(0,bm)
        writer.writerow(row)
    f.close()
    
def main():
    data, BMs, GCs = read_data("energy")
    norm_per_BM(data, BMs, GCs, "energy")
    data, BMs, GCs = read_data("energy")
    norm_per_GC(data, BMs, GCs, "energy")
    data, BMs, GCs = read_data("energy")
    norm_per_G1(data, BMs, GCs, "energy")
    data, BMs, GCs = read_data("perf")
    norm_per_BM(data, BMs, GCs, "perf")
    data, BMs, GCs = read_data("perf")
    norm_per_GC(data, BMs, GCs, "perf")
    data, BMs, GCs = read_data("perf")
    norm_per_G1(data, BMs, GCs, "perf")

main()

