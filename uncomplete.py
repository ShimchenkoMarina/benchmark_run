#!/usr/bin/python3
import sys
import os
import re
from functools import reduce

def analyze_file(input_dir, file_num):
    file_name = os.path.join(input_dir, file_num)
    with open(os.path.join(input_dir, file_num), 'r') as reader:
        for line in reader.readlines():
            if "Exception in thread \"" in line:
                #print("fail: " + file_name)           
                exit(100)     
            if "Java heap space\"" in line:
                #print("fail: " + file_name)           
                exit(100)     

def main():
    if len(sys.argv) != 3:
        print("Usage analyze_file.py input_dir file_num")
        exit(1)
    analyze_file(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
