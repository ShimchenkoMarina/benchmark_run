#!/usr/bin/python3
import sys
import os
benchmarks_cut = {"h2": 5, "fop": 10, "avrora": 3, "jython": 5, "luindex": 7, "lusearch": 1, "pmd": 8, "sunflow": 4, "xalan": 4} 
def process_file(input_dir, output_dir, file_num):
    write = False
    i = 0
    with open(os.path.join(input_dir, file_num), 'r') as reader:
        cut = 14
        for bench_name in benchmarks_cut:
            if input_dir.find(bench_name):
                cut = int(benchmarks_cut[bench_name])
        with open(os.path.join(output_dir, file_num), "a") as writer:
            for line in reader.readlines():
                if "Done" in line:
                    write = True
                    i = i + 1
                if write and i > cut:
                    writer.write(line)

def main():
    if len(sys.argv) != 4:
        print("Usage process_file.py input_dir raw_dir file_num")
        exit(1)
    process_file(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
