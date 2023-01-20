import analyze_file
import matplotlib.pyplot as plt
from matplotlib import rc
import os
import glob
def parse_CPU_Util(folder, file):
    #print(file)
    CPU_Util = []
    with open("output.txt", 'r') as reader:
        for line in reader.readlines():
                numbers = analyze_file.separate_number_chars(line)
                #print("numb 0 = ", numbers)
                if numbers[0].strip().isnumeric():
                    CPU_util = (int(numbers[12]) + int(numbers[13]))*16/100*8
                    #print(CPU_util)
                    CPU_Util.append(CPU_util)
    with open(folder + "/" + file, "a") as writer:
        writer.write("CPU utilization: " + str(analyze_file.avg(CPU_Util)) + "\n")
    os.system("cp output.txt "  + folder)
    print(str(analyze_file.avg(CPU_Util)))
    with open("result.txt", 'a') as writer:
        writer.write(folder + " " + str(analyze_file.avg(CPU_Util)) + "\n") 
    #print_CPU_Util(folder, CPU_Util)

def print_CPU_Util(folder, data):
    fig = plt.figure()
    plt.rcParams["ps.useafm"] = True
    rc('font', **{'family':'sans-serif', 'sans-serif':['FreeSans']})
    plt.rcParams['pdf.fonttype'] = 42
    # use axis={'both', 'x', 'y'} to choose axis
    plt.locator_params(axis="both", integer=True, tight=True)
    #print(data)
    plt.plot(data, color= "green")
    plt.legend()
    fig.tight_layout()
    fig.savefig(folder + "/CPU_Util.pdf")

def find_path():
    runs = glob.glob("./results_tHU/*/*/output.txt")
    for run in runs:
        res_folder = run.split("/")[1]
        bm = run.split("/")[2]
        gc_conf = run.split("/")[3]
        print(run)
        #print(run[:-10])
        parse_CPU_Util(run[:-10])

#find_path()
