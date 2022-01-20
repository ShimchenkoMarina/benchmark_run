#!/usr/bin/python3
import sys
import os
 
def process_file(output_dir, file_num):
    with open(os.path.join(output_dir, file_num), 'r') as reader:
        tmp_list_of_lists = []
        with open(os.path.join(output_dir, "features.txt"), "w") as writer:
            for line in reader.readlines():
                    tmp_list = line.strip().split("|")
                    found = False
                    for el_list in tmp_list_of_lists:
                        if el_list[0].strip() == tmp_list[0].strip() :
                            found = True
                    if found == False:
                        tmp_list_of_lists.append(tmp_list)
                        #print(tmp_list_of_lists)
                        tmp_line = ""
                        for el in tmp_list:
                            tmp_line = tmp_line + "  " + el.strip()
                        print(tmp_line)
                        writer.write(tmp_line.lstrip() + "\n")
                    else: 
                        found = False
def main():
    if len(sys.argv) != 3:
        print("Usage clean_file_likwid.py raw_dir file_num")
        exit(1)
    process_file(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
