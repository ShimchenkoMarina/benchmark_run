#!/usr/bin/python3
import sys
import os
 
def process_file(input_dir, output_dir, file_num):
    write = False
    i = 0
    j = 0 #need this variable to count 3 lines after last Done, this is for RN
    with open(os.path.join(input_dir, file_num), 'r') as reader:
        cut = 5
        with open("/scratch/mshimche/Project/benchmark_run/benchmark_cut.txt", "r") as read_cut:
            for line in read_cut.readlines():
                bench_name = line.split(" ")[0].split("\"")[1]
                if input_dir.find(bench_name):
                    cut = int(line.split(" ")[1])
                    break
        with open(os.path.join(output_dir, file_num), "w") as writer:
            for line in reader.readlines():
                if "Done" in line:
                    write = True
                    i = i + 1
                if i > cut:
                    j = j + 1
                if write and i > cut and j > 4:
                    writer.write(line)
def main():
    if len(sys.argv) != 4:
        print("Usage process_file.py input_dir raw_dir file_num")
        exit(1)
    #Process latency and latency-oritnted bms separately, nothing to cut
    if "hazelcast" in sys.argv[1] or "spec" in sys.argv[1]:
        path_from = os.path.join(sys.argv[1], sys.argv[3]) 
        path_to = os.path.join(sys.argv[2], sys.argv[3])
        os.system("sudo cp " + path_from + " " + path_to)
    else: 
        process_file(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
