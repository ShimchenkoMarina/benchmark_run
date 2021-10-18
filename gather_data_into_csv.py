import pandas as pd
import os
from utils.UniqueRuns import UniqueRuns
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as plticker
import csv

#baseline_name = "j16SerH"
#all_order = ["j16SerH", "j13P_n4", "j13P_n1", "j13P_n2", "j13CMS", "j13Ser", "j16ShenH", "j16ZH", "j16G1H", "j16PH_n1", "j16PH_n2", "j16PH_n4"]
order = []
#baseline_priority = ["Ser", "CMS", "P", "Z"]
bms = list()
rows_energy = []
rows_perf = []
rows_latency = []
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
        if sample in file:
            curr_df = pd.read_csv(file, header=None)
            df = df.append(pd.DataFrame(curr_df.values, columns=[configuration_name]), ignore_index=True)
    return df

def extract_ordered_data(data):
    ordered_data = list()
    for conf in data:
        fields.append(conf) 
        ordered_data.append((conf, data[conf]))
    return ordered_data


def analyze_data(sample, data, baseline, baseline_name, benchmark_name):
    results_aggregated = baseline[0].copy()
    results_points = baseline[1].copy()
    
    for (configuration, data) in extract_ordered_data(data):
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
            STR_STD_MEAN: std / mean,
            STR_PERF: 1 - mean.divide(baseline[0][STR_MEAN].values[0])  # 1- row$mean/baseline
                })
        results_points = results_points.join(d, how="outer")
        results_aggregated = results_aggregated.append(result)
    #results_aggregated = results_aggregated.sort_values(by=[STR_PERF])
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

def normalized_data(df, baseline_name):
    result = [0.0]
    b = float(df.loc[df[STR_TYPE] == baseline_name][STR_MEAN].values[0])
    for o in order:
        if o == baseline_name:
            continue
        result.append(100.0 * (float(df.loc[df[STR_TYPE] == o][STR_MEAN].values[0])/b - 1))
    return result

def store_result(sample, result, res_folder, benchmark_name, baseline_name):
    #So I need to create a list like this
    #fields = [bms, GC1, GC2, GC3, ....]
    #rows = [[bm1, energy1, energy2, energy3, ...],
    #        [bm2, energy1, energy2, energy3, ...],
    #       ...     #       ]
    row = [benchmark_name]

    result_aggregated, result_points = result
    result_dir = os.path.join("processed_results", res_folder, benchmark_name)
    pathlib.Path(result_dir).mkdir(parents=True, exist_ok=True)
    for number in result_aggregated[STR_MEAN].astype(float).map("{: .2f}".format):
        row.append(number)
    if "energy" in sample:
        rows_energy.append(row)
    if "perf" in sample:
        rows_perf.append(row)
    if "latency" in sample:
        rows_latency.append(row)

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
        baseline_name = ""
        dict_for_benchmark = {}
        for conf_runs in allconf_runs:
            for conf in conf_runs:
                if baseline_name == "":
                    baseline_name = conf
                append_value(dict_for_benchmark, conf, conf_runs[conf])
        #print(dict_for_benchmark[baseline_name])
        #TODO: add latency parcing
        #TODO: add multiple measurements handeling
        measurement = ["energy_pack", "perf"]
        for m in measurement:
            baseline = analyze_baseline(m, dict_for_benchmark[baseline_name], baseline_name, benchmark_name)
            result = analyze_data(m, dict_for_benchmark, baseline, baseline_name, benchmark_name)
            store_result(m, result, res_folder, benchmark_name, baseline_name)
    with open (os.path.join("/scratch/Project/benchmark_run/EnergyVsTimePlots", "table_energy.csv"), "w") as f:
        write = csv.writer(f, skipinitialspace=True, delimiter=';', quoting=csv.QUOTE_NONE)
        write.writerow(fields)
        write.writerows(rows_energy)
    with open (os.path.join("/scratch/Project/benchmark_run/EnergyVsTimePlots", "table_perf.csv"), "w") as f:
        write = csv.writer(f, skipinitialspace=True, delimiter=';', quoting=csv.QUOTE_NONE)
        write.writerow(fields)
        write.writerows(rows_perf)
    '''with open (os.path.join("/scratch/Project/benchmark_run/EnergyVsTimePlots", "table_latency.csv"), "w") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows_latency)'''

if __name__ == "__main__":
    main()