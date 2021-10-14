import pandas as pd
import os
from utils.UniqueRuns import UniqueRuns
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as plticker

#baseline_name = "G1"
#order = ["G1", "PGC", "SGC", "ZGC", "HCSGC", "m1"]
baseline_name = "j16SerH"
#all_order = ["j16P_n2", "j16P_n1", "j16P_n4", "j13P_n4", "j13P_n1", "j13P_n2", "j13CMS", "j16Ser", "j16Z", "j16G1", "j13Ser", "j16ShenH", "j16SerH", "j16ZH", "j16G1H", "j16PH_n1", "j16PH_n2", "j16PH_n4"]
all_order = ["j16SerH", "j13P_n4", "j13P_n1", "j13P_n2", "j13CMS", "j13Ser", "j16ShenH", "j16ZH", "j16G1H", "j16PH_n1", "j16PH_n2", "j16PH_n4"]
order = []
baseline_priority = ["Ser", "CMS", "P", "Z"]
bms = list()

plt.rcParams.update({'font.size': 14})

pd.options.display.width = 0
STR_TYPE = "Type"
STR_N = "N"
STR_MEAN = "Mean"
STR_STD_MEAN = "Relative Standard Deviation"
STR_STD = "Standard Deviation"
STR_PERF = "Performance"
STR_CI_LOWER = "CI Lower"
STR_CI_UPPER = "CI Upper"
column_names = [STR_TYPE, STR_N, STR_MEAN, STR_STD, STR_STD_MEAN, STR_PERF]

df_style = """
.mystyle {
    font-size: 11pt;
    font-family: Arial;
    border-collapse: collapse;
    border: 1px solid silver;
    #width: 100%;

}

.mystyle td, th {
    padding: 5px;
    width: 100px;
}

.mystyle tr:nth-child(even) {
    background: #E0E0E0;
}

.mystyle tr:hover {
    background: silver;
    cursor: pointer;
}"""


def HTML_template(table, css, title, gc_tag):
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Results - """ + title + """</title>
  <style>
  """ + css + """
  </style>
</head>

<body>
<h2>""" + title + """</h2>
<a href="table.tex">Latex code for table</a><br/><br/>
""" + table + """
<br />
<a href="errorbar_"""+ gc_tag +""".eps"><img src="errorbar_"""+ gc_tag +""".svg" height="80%" width="80%"/></a>
</body>
</html>
    """
#<a href="boxplot_"""+ gc_tag + """.eps"><img src="boxplot_"""+ gc_tag + """.svg" height="40%" /></a>

def bootstrapped_ci(df_input):
    columns = [STR_CI_LOWER, STR_CI_UPPER]
    df_result_sep = pd.DataFrame(columns=columns)
    columns = ["yerr"]
    df_result = pd.DataFrame(columns=columns)

    for (columnName, columnData) in df_input.iteritems():
        df = pd.DataFrame()
        for i in range(0, 10):
            df = df.append(df_input[columnName].sample(n=10000, replace=True).reset_index()[columnName])
        mean = df.mean(axis=0)
        ci_lower = mean.quantile(0.025)
        ci_upper = mean.quantile(0.975)
        df_result.loc[columnName] = (ci_upper - ci_lower)/2
        df_result_sep.loc[columnName] = [ci_lower, ci_upper]

    #print(df_result.loc[:,["yerr"]])
    #print(df_result_sep[STR_CI_LOWER])
    #print(df_result_sep[STR_CI_UPPER])
    df_result = pd.to_numeric(df_result["yerr"], errors="raise", downcast="float")
    return df_result, df_result_sep

def format_columns(df):
    df[STR_MEAN] = df[STR_MEAN].astype(float).map("{: .2f}".format)
    df[STR_STD] = df[STR_STD].astype(float).map("{: .2f}".format)
    df[STR_STD_MEAN] = df[STR_STD_MEAN].astype(float).map("{:.2%}".format)
    df[STR_PERF] = df[STR_PERF].astype(float).map("{:.2%}".format)
    df[STR_CI_LOWER] = df[STR_CI_LOWER].astype(float).map("{:.2f}".format)
    df[STR_CI_UPPER] = df[STR_CI_UPPER].astype(float).map("{:.2f}".format)

def read_data(sample, data, configuration_name, benchmark_name):
    df = pd.DataFrame(columns=[configuration_name])
    for file in data:
        if sample in file:
            curr_df = pd.read_csv(file, header=None)
            df = df.append(pd.DataFrame(curr_df.values, columns=[configuration_name]), ignore_index=True)
    return df

def extract_ordered_data(data):
    ordered_data = list()
    for o in order:
        ordered_data.append((o, data[o]))
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
        #print("result", result)
        results_points = results_points.join(d, how="outer")
        results_aggregated = results_aggregated.append(result)
    results_aggregated = results_aggregated.sort_values(by=[STR_PERF])
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
    print("baseline_name", baseline_name)
    b = float(df.loc[df[STR_TYPE] == baseline_name][STR_MEAN].values[0])
    for o in order:
        if o == baseline_name:
            continue
        result.append(100.0 * (float(df.loc[df[STR_TYPE] == o][STR_MEAN].values[0])/b - 1))
    return result

def store_result(sample, result, res_folder, benchmark_name, baseline_name):
    result_aggregated, result_points = result
    '''print(order)
    #manipulating order
    main_el = order[0]
    print(main_el)
    new_order = []
    new_order.append(order[0])
    for el in order[1:len(order)]:
        print(el[0:4])
        if el[0:4] != main_el[0:4]:
            main_el = el
            new_order.append(el)
        if el[0:4] == main_el[0:4]:
            el = el[4:len(el)]
            new_order.append(el)
    print(new_order)
    order = new_order
    print(order)'''


    result_dir = os.path.join("processed_results", res_folder, benchmark_name)
    pathlib.Path(result_dir).mkdir(parents=True, exist_ok=True)

    df_error, df_result_sep = bootstrapped_ci(result_points)
    #print(df_result_sep)
    merged = pd.merge(result_aggregated, df_result_sep, how='outer', left_on=["Type"], right_index=True)
    result_aggregated = merged
    format_columns(result_aggregated)
    result_aggregated.rename(index=lambda s: benchmark_name, inplace=True)

    figure = plt.figure()
    plt.ylabel('')
    #result_points.boxplot() IF USING THIS VERIFY CORECTNESS!
    plt.xticks(rotation='vertical')
    plt.margins(0.5)
    plt.subplots_adjust(bottom=0.4)
    figure.savefig(os.path.join(result_dir, "boxplot_"+sample +".svg"), format="svg")
    figure.savefig(os.path.join(result_dir, "boxplot_"+sample +".eps"), format="eps")
    plt.close(figure)

    figure = plt.figure()
    plt.ylabel('')
    #plt.errorbar(result_points.mean().index, result_points.mean(), yerr=df_error, marker='x', linestyle='', capsize=8, markersize="8"   )
    plt.errorbar(result_points.mean().index, result_points.mean(), marker='^', linestyle='', capsize=8, markersize="8"   )

    plt.xticks(range(0, len(order) + 1, 1), rotation='vertical')
    plt.subplots_adjust(bottom=0.4)
    figure.savefig(os.path.join(result_dir, "errorbar_"+sample +".svg"), format="svg")
    figure.savefig(os.path.join(result_dir, "errorbar_"+sample +".eps"), format="eps")
    plt.close(figure)
    #print("res_agg = ", result_aggregated)
    n = normalized_data(result_aggregated, baseline_name)
    x = np.arange(len(order))
    width =0.7
    fig, ax = plt.subplots()
    plt.axhline(0, color='k')

    col = []
    for val in n:
        if val < 0:
            col.append('blue')
        elif val >= 0:
            col.append('#5f81c1')
    ax.bar(x + width/2, n, width, color = col)
    ax.set_ylabel('')
    ax.set_title('')
    ax.set_xticks(x)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
    #print(ax.get_xticks())
    ax.set_xticklabels(order)
#    ax.legend()
    fig.savefig(os.path.join(result_dir, "norm_mean_"+sample +".svg"), format="svg")
    fig.savefig(os.path.join(result_dir, "norm_mean_"+sample +".eps"), format="eps")

    table = result_aggregated.to_html(classes='mystyle')
    with open(os.path.join(result_dir, "table_"+sample +".tex"), "w") as writeFile:
        writeFile.write(result_aggregated.to_latex())

    with open(os.path.join(result_dir, "result_"+sample +".html"), "w") as writeFile:
        writeFile.write(HTML_template(table, df_style,
                                      " ".join([sample, res_folder,  benchmark_name]), sample))

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
    #print(runs)
    #this array should have the following format:{type: [/home/..../file_pack.txt,file_cpu.txt, file_dram.txt],  } 
    benchmarks_conf = {}
    for res_folder, res_content  in runs.items():
        if "processed" in res_folder:
            #We need to dig deeper one level
            for (new_level, res_content_correct) in res_content.items():
                for (benchmark_name, configurations) in res_content_correct.items():
                    #bms = list(configurations.keys())
                    #print(bms)
                    #print("bench_name = ", benchmark_name)
                    #print("configuration = ", configurations)
                    append_value(benchmarks_conf, benchmark_name, configurations)
                    #for (conf, conf_runs) in configurations.items():
                    #    all_conf_runs.clear()
                    #    all_conf_runs[conf] = conf_runs
                    #    print(conf)
                    #    print(conf_runs)
        else:
            for (benchmark_name, configurations) in res_content.items():
                #bms = list(configurations.keys())
                #print(bms)
                for (conf, conf_runs) in configurations.items():
                    #print("conf = ", conf)
                    if "P" in conf:
                        for (numthr, numthr_runs) in conf_runs.items(): 
                            #if numthr contains java, then it has already been processed
                            real_conf = conf + "_" + numthr
                            #conf_runs[real_conf] = conf_runs.pop(numthr)
                            #print(conf_runs)
                            all_conf_runs = {}
                            all_conf_runs[real_conf] = numthr_runs
                            #print("all_conf_runs = ", all_conf_runs)
                            append_value(benchmarks_conf, benchmark_name, all_conf_runs)
                            #benchmarks_conf[benchmark_name].update(all_conf_runs)
                            #print(benchmarks_conf[benchmark_name])'''
                    else:
                        append_value(benchmarks_conf, benchmark_name, configurations)
                        #print("bench_name = ", benchmark_name)
                        #print("configuration = ", configurations)
                        #benchmarks_conf[benchmark_name].update(all_conf_runs)
                        #print(benchmarks_conf[benchmark_name])'''

    for (benchmark_name, allconf_runs) in benchmarks_conf.items():
        #print("benchmark name = ", benchmark_name)
        if (benchmark_name == "h2_small_t4"):
            dict_for_benchmark = {}
            local_order = []
            local_baseline_name = ""
            #print("allconf_runs = ", allconf_runs)
            flag = 0
            for baseline_substring in baseline_priority:
                for conf_runs in allconf_runs:
                    #print("conf_runs = ", conf_runs)
                    #print("base_p = ", baseline_substring)
                    for conf in conf_runs:
                        #print("conf = ", conf)
                        if (baseline_substring not in conf): 
                            continue
                        else:
                            local_baseline_name = conf
                            flag = 1
                            break
                    if (flag == 1):
                        break
                if (flag == 1):
                    break
            
            '''for baseline_substring in baseline_priority:
                for conf_runs in allconf_runs:
                    print("conf_runs = ", conf_runs)
                    #print("base_p = ", baseline_substring)
                    #for conf in conf_runs:
                    #print("conf = ", conf)
                    if (baseline_substring not in conf_runs): 
                        continue
                    else:
                        local_baseline_name = conf_runs
                        flag = 1
                        break
                if (flag == 1):
                    break'''

            '''if (local_baseline_name == ""):
                local_baseline_name = conf_runs[0]'''
            baseline_name = local_baseline_name
            print("baseline = ", baseline_name)
            for conf_runs in allconf_runs:
                #print("conf_runs = ", conf_runs)
                #for o in all_order:
                #    if(conf_runs.get(o)):
                #        #print(conf_runs[o])
                #        order.append(o)
                #Figure out our baseline
                for conf in conf_runs:
                    print("conf = ", conf)
                    if (conf != baseline_name):
                        local_order.append(conf)
                    append_value(dict_for_benchmark, conf, conf_runs[conf])
            '''for conf_runs in allconf_runs:
                #print("conf_runs = ", conf_runs)
                #for o in all_order:
                #    if(conf_runs.get(o)):
                #        #print(conf_runs[o])
                #        order.append(o)
                #Figure out our baseline
                #for conf in conf_runs:
                #print("conf = ", conf)
                if (conf_runs != baseline_name):
                        local_order.append(conf_runs)
                append_value(dict_for_benchmark, conf_runs, allconf_runs[conf_runs])'''
            order.append(baseline_name)
            #if there are other versions with the same java version and GC
            #add them after baseline
            new_local_order = []
            for el in local_order:
                if el[0:3] == baseline_name[0:3]:
                    order.append(el)
                else: 
                    new_local_order.append(el)
            local_order = sorted(new_local_order)
            for el in local_order:
                order.append(el)
            print("order = ", order)
            measurement = ["energy_pack", "energy_dram", "energy_cpu", "perf", "watts_cpu", "watts_dram", "watts_pack"]
            #measurement = ["watts_dram"]
            #measurement = ["energy_pack", "energy_dram", "energy_cpu"]
            for m in measurement:
                #print(m)
                #print(dict_for_benchmark[baseline_name])
                if dict_for_benchmark.get(baseline_name) and has_contents(dict_for_benchmark[baseline_name], m):
                       baseline = analyze_baseline(m, dict_for_benchmark[baseline_name], baseline_name, benchmark_name)
                       result = analyze_data(m, dict_for_benchmark, baseline, baseline_name, benchmark_name)
                       #print("baseline_name = ", baseline_name)
                       store_result(m, result, res_folder, benchmark_name, baseline_name)
            order.clear()

    '''measurement = ["energy_pack", "energy_dram", "energy_cpu"]
    for (benchmark_name, allconf_runs) in benchmarks_conf.items():
        print(benchmark_name)
        for conf_runs in allconf_runs:
             for m in measurement:
                 if conf_runs.get(baseline_name) and has_contents(conf_runs[baseline_name], m):
                       baseline = analyze_baseline(m, conf_runs[baseline_name], baseline_name, benchmark_name)
                       result = analyze_data(m, conf_runs, baseline, baseline_name, benchmark_name)
                       store_result(m, result, res_folder, benchmark_name)
'''
    '''if has_contents(allconf_runs[baseline_name], m):
        baseline = analyze_baseline(m, allconf_runs[baseline_name], baseline_name, benchmark_name)
        result = analyze_data(m, allconf_runs, baseline, baseline_name, benchmark_name)
        store_result(m, result, res_folder, benchmark_name)'''
if __name__ == "__main__":
    main()
