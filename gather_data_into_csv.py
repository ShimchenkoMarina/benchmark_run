import pandas as pd
import os
from utils.UniqueRuns import UniqueRuns
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as plticker
import csv
import sys
order = []
bms = list()
rows = []
fields = ["BMs"]

STR_TYPE = "Type"
STR_N = "N"
STR_MEAN = "Mean"
STR_STD_MEAN = "Relative Standard Deviation"
STR_STD = "Standard Deviation"
STR_PERF = "Performance"

def read_data(sample, data, configuration_name, benchmark_name):
    df = pd.DataFrame(columns=[configuration_name])
    for file in data:
        #print(file)
        #print("\n")
        if sample in file:
            try:
                curr_df = pd.read_csv(file, header=None)
            except pd.errors.EmptyDataError:
                curr_df = pd.DataFrame()
            if not curr_df.empty:
                #df = df.append(pd.DataFrame(curr_df.values, columns=[configuration_name]), ignore_index=True)
                df_new = pd.DataFrame(curr_df.values, columns=[configuration_name])
                df = pd.concat([df, df_new])
            else:
                df = pd.DataFrame(columns=[configuration_name])
    return df

def extract_ordered_data(data, sample):
    ordered_data = list()
    for conf in data:
        fields.append(conf)
        order.append(conf)
        ordered_data.append((conf, data[conf]))
    return ordered_data


def analyze_data(sample, data, baseline, baseline_name, benchmark_name):
    results_aggregated = baseline[0].copy()
    results_points = baseline[1].copy()

    for (configuration, data) in extract_ordered_data(data, sample):
        if configuration == baseline_name:
            continue
        d = read_data(sample, data, configuration, benchmark_name)
        std = d.std()
        mean = d.mean()
        result = pd.DataFrame({
            STR_TYPE: configuration,
            STR_N: d.size,
            STR_MEAN: mean,
            STR_STD: std,
            STR_STD_MEAN: std / mean
                })
        results_points = results_points.join(d, how="outer")
        results_aggregated = pd.concat([results_aggregated, result])
    results_aggregated.index = range(1, len(results_aggregated.index) + 1)

    return results_aggregated, results_points

def analyze_baseline(sample, data, baseline, benchmark_name):
    #print("data =", data)
    #print("sample =", sample)
    #print("baseline =", baseline)
    #print("benchmark_name =", benchmark_name)

    d = read_data(sample, data, baseline, benchmark_name)
    std = d.std()
    mean = d.mean()
    result_aggregated = pd.DataFrame({
        STR_TYPE: baseline,
        STR_N: d.size,
        STR_MEAN: mean,
        STR_STD: std,
        STR_STD_MEAN: std / mean,
        STR_PERF: 0
       })

    return result_aggregated, d

def normalized_data(sample, df, baseline_name):
    result = []
    b = float(df.loc[df[STR_TYPE] == baseline_name][STR_MEAN].values[0])
    for o in order:
        if "GC" not in sample:
            if o == baseline_name:
                result.append(1.0)
                continue
            result.append(float(df.loc[df[STR_TYPE] == o][STR_MEAN].values[0])/b)
        else:
            result.append(float(df.loc[df[STR_TYPE] == o][STR_MEAN].values[0]))
    return result

def find_best_baseline(res):
    min_value = res[STR_MEAN].values[0]
    conf_name = ""
    for index, number in enumerate(res[STR_MEAN]):
        if number < min_value:
            min_value = number
            conf_name = res[STR_TYPE].values[index]
    if (conf_name == ""):
        conf_name = res[STR_TYPE].values[0]
    return conf_name


def store_result(sample, result, res_folder, benchmark_name, baseline_name):
    #So I need to create a list like this
    #fields = [bms, GC1, GC2, GC3, ....]
    #rows = [[bm1, energy1, energy2, energy3, ...],
    #        [bm2, energy1, energy2, energy3, ...],
    #       ...     #       ]
    #if "perf" in sample:
        #print(result)
    row = [benchmark_name]

    result_aggregated, result_points = result
    normilized_results = normalized_data(sample, result_aggregated, baseline_name)
    for number in normilized_results:
        row.append("{:.2f}".format(number))
    rows.append(row)

def has_contents(data, sample):
    for file in data:
        if sample in file:
            return os.stat(file).st_size > 0
    return False

def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        #print("the key is in dict")
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        #print("new value for dict")
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = value

def main():
    runs = UniqueRuns()
    #this array should have the following format:{type: [/home/..../file_pack.txt,file_cpu.txt, file_dram.txt],  }
    benchmarks_conf = {}
    for res_folder, res_content  in runs.items():
        if "processed" in res_folder:
            #We need to dig deeper one level
            for (new_level, res_content_correct) in res_content.items():
                for (benchmark_name, configurations) in res_content_correct.items():
                    append_value(benchmarks_conf, benchmark_name, configurations)
        else:
            for (benchmark_name, configurations) in res_content.items():
                for (conf, conf_runs) in configurations.items():
                    #print("conf = ", conf)
                    if "P" in conf:
                        for (numthr, numthr_runs) in conf_runs.items():
                            #if numthr contains java, then it has already been processed
                            real_conf = conf + "_" + numthr
                            all_conf_runs = {}
                            all_conf_runs[real_conf] = numthr_runs
                            #print("all_conf_runs = ", all_conf_runs)
                            append_value(benchmarks_conf, benchmark_name, all_conf_runs)
                    else:
                        append_value(benchmarks_conf, benchmark_name, configurations)
    #So I need to create a list like this
    #fields = [bms, GC1, GC2, GC3, ....]
    #rows = [[bm1, energy1, energy2, energy3, ...],
    #        [bm2, energy1, energy2, energy3, ...],
    #       ...
    #       ]
    #np.savetxt("GFG.csv",
    #       rows,
    #       delimiter =", ",
    #       fmt ='% s')
    for (benchmark_name, allconf_runs) in benchmarks_conf.items():
        #print(benchmark_name)
        #if "akka-uct" not in benchmark_name:
        #    continue
        baseline_name = ""
        dict_for_benchmark = {}
        for conf_runs in allconf_runs:
            if isinstance(conf_runs, dict):
                for conf in conf_runs:
                    print(conf)
                    if baseline_name == "" and "j20GZ" in conf and str(1.0) in conf:
                        baseline_name = conf
            elif baseline_name == "" and "j20GZ" in conf_runs and str(1.0) in conf_runs:
                baseline_name = conf_runs
            append_value(dict_for_benchmark, conf_runs, allconf_runs[conf_runs])
        print("baseline", baseline_name)
        if baseline_name != "":
            #measurement = ["energy_pack", "perf", "max_latency", "mean_latency", "watts_pack", "energy_dram", "energy_cpu", "GC_cycles", "energy_pack_dram"]
            #measurement = ["energy", "power", "perf", "GC_cycles", "stalls"]
            measurement = ["GC_cycles"]
            for m in measurement:
                #print(m)
                baseline = analyze_baseline(m, dict_for_benchmark[baseline_name], baseline_name, benchmark_name)
                result = analyze_data(m, dict_for_benchmark, baseline, baseline_name, benchmark_name)
                store_result(m, result, res_folder, benchmark_name, baseline_name)
                with open (os.path.join(os.getcwd() + "/EnergyVsTimePlots/tables/", "table_" + m + "_" + benchmark_name + ".csv"), "w+") as f:
                    write = csv.writer(f, skipinitialspace=True, delimiter=';', quoting=csv.QUOTE_NONE)
                    temp_row = rows[0].copy()
                    temp_index = 0
                    for index, number in enumerate(rows[0]):
                            if "nan" in number:
                                del temp_row[index - temp_index]
                                del fields[index - temp_index]
                                temp_index = temp_index + 1
                    write.writerow(fields)
                    write.writerow(temp_row)
                rows.clear()
                fields.clear()
                order.clear()
                fields.append('BMs')

if __name__ == "__main__":
    main()
