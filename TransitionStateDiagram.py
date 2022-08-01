import numpy as np
import matplotlib.pyplot as plt

# Identify thred to core placement
def extract_pid(pid):
    imprint = [] # contains P for P-core and E for E-core.
    with open("/home/marina/Project/benchmark_run/scheduler.txt", 'r') as reader:
        for line in reader.readlines():
            if pid in line:
                curr_cpu = int(line.split("->")[1])
                if curr_cpu >=16:
                    imprint.append("E")
                else:
                    imprint.append("P")
    return imprint

def display(array):
    fig = plt.figure()
    x_labels = ["P", "E"]
    print(array.count("P"))
    y_labels = [array.count("P"), array.count("E")]
    plt.bar(x_labels, y_labels)
    plt.savefig("PVSE_java20")

# Read the pids of GC threads
def main():
    PE_array = []
    with open("/home/marina/Project/benchmark_run/GC_pids.txt", 'r') as reader:
            for line in reader.readlines():
                pid = line.split(" ")[3].strip()
                PE_array.extend(extract_pid(pid))
    display(PE_array)
main()
