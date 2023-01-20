import analyze_file
import matplotlib.pyplot as plt
from matplotlib import rc
import os
import glob

def parse_CPU_Util(folder, file, N):
    CPU_Util = []
    with open("output.txt", 'r') as reader:
        for line in reader.readlines():
            numbers = analyze_file.separate_number_chars(line)
            if numbers[0].strip().isnumeric():
                CPU_util = (int(numbers[12]) + int(numbers[13]))*32/100*N
                CPU_Util.append(CPU_util)
    with open(folder + "/" + file, "a") as writer:
        writer.write("CPU utilization: " + str(analyze_file.avg(CPU_Util)) + "\n")
    os.system("cp output.txt "  + folder)
    #print(str(analyze_file.avg(CPU_Util)))
