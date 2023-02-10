#Olof's project collect data
import subprocess
import threading
import _thread
from subprocess import Popen
import os
import pathlib
from os.path import isfile, join
from os import listdir
import platform
from timeit import default_timer as timer
import sys, getopt
import CPUUtil

#Path variables
CONFIG_SPEC=""
CLASSPATH_SPEC=""
CLASSPATH_RN=""
CLASSPATH_DACAPO=""
CLASSPATH_HAZELCAST=""
JAVA20 = ""
JAVA20_OLOF = ""
JAVA20_YinYan = ""
JAVA20_RESTRICTED = ""
JAVA20_GEN=""
JAVA20_4P4P=""
JAVA20_4P4E=""
JAVA20_MARK=""

file = open('../benchmark_run/path_file.txt', 'r')
for line in file:
    variable = line.split("=")[0]
    if "CONFIG_SPEC" in variable:
        CONFIG_SPEC=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_SPEC" in variable:
        CLASSPATH_SPEC=line.split("=")[1].split("\"")[1]
        continue
    if "CLASSPATH_HAZELCAST" in variable:
        CLASSPATH_HAZELCAST=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_DACAPO" in variable:
        CLASSPATH_DACAPO=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_RN" in variable:
        CLASSPATH_RN=line.split("=")[1].split("\"")[1]
    if "JAVA20"==variable:
        JAVA20=line.split("=")[1].split("\"")[1]
    if "JAVA20_OLOF"==variable:
        JAVA20_OLOF=line.split("=")[1].split("\"")[1]
    if "JAVA20_YinYan"==variable:
        JAVA20_YinYan=line.split("=")[1].split("\"")[1]
    if "JAVA20_RESTRICTED"==variable:
        JAVA20_RESTRICTED=line.split("=")[1].split("\"")[1]
    if "JAVA20_GEN"==variable:
        JAVA20_GEN=line.split("=")[1].split("\"")[1]
    if "JAVA20_MARK"==variable:
        JAVA20_MARK=line.split("=")[1].split("\"")[1]
    if "JAVA20_4P4P"==variable:
        JAVA20_4P4P=line.split("=")[1].split("\"")[1]
    if "JAVA20_4P4E"==variable:
        JAVA20_4P4E=line.split("=")[1].split("\"")[1]

FLAGS_HAZELCAST="--add-modules java.se --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.nio=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED"

#Java log
JAVA_LOG = " -Xlog:gc* "
JAVA_LOG_ALLOCATION_RATE = "-Xlog:gc+stats"
#Specify here which bm+java you want to run
Which_BM = {
            "DaCapo",
            #"HazelCast",
            #"specjbb2015",
            #"Renaissance_static",
            #"DaCapo_j20_yinyan_static",
            #"DaCapo_j20_critical_static",
            #"DaCapo_j20_gen_clean_static",
            #"DaCapo_j20_olof_static_pids",
            #"DaCapo_j20_gen_clean_static_pids",
            #"DaCapo_j20_gen_clean_static_perf",
            #/"DaCapo_j20_olof_static_allocation_rate",
            #/"DaCapo_j20_gen_clean_static_allocation_rate",
            #"HazelCast_j20_olof",
            #"HazelCast_j20_gen_clean",
            #"HazelCast_j20_olof_static",
            #"HazelCast_j20_yinyan_static",
            #"HazelCast_j20_critical_static",
            #"HazelCast_j20_gen_clean_static",
            #"HazelCast_j20_gen_clean_static_perf",
            #"HazelCast_j20_gen_clean_static_pids",
            #"Renaissance_j20_gen_clean_static",
            #"Renaissance_j20_gen_clean_static_pids",
            #"Renaissance_j20_olof_static",
            #"Renaissance_j20_yinyan_static",
            #"Renaissance_j20_critical_static",
            #"Renaissance_j15M1",
            #"specjbb2015_j20_olof",
            #"specjbb2015_j20_gen_clean",
            #"specjbb2015_j20_olof_static",
            #"specjbb2015_j20_yinyan_static",
            #"specjbb2015_j20_critical_static",
            #"specjbb2015_j20_gen_clean_static",
            #"specjbb2015_j20_gen_clean_static_pids",
            #"specjbb2015_j20_gen_clean_static_perf",
            #"specjbb2015_j20_mark_static",
            #"specjbb2015_j20_olof_static_allocation_rate",
            #"specjbb2015_j20_gen_clean_static_allocation_rate",
            #/"HazelCast_j20_olof_static_allocation_rate",
            #"HazelCast_j20_gen_clean_static_allocation_rate",
            #"Renaissance_j20_gen_clean_static_allocation_rate",
            #"Renaissance_j20_olof_static_allocation_rate",
}
GC_threads = {
        #"4" : "-XX:ConcGCThreads=4", 
        "8"  : "-XX:ConcGCThreads=8"
}

#Specify GCs for each java version
GC = {
    'Z': '-XX:+UseZGC' ,
}

HW_conf = {
        #"8P8E": ""
        #"8P" : "numactl -C 0-15  ", 
        "4P4E"  : "numactl -C 0-7,16-19",
        "4P4P"  : "numactl -C 0-15"
}
#Specify bms
BM_DaCapo = {
          "lusearch_def_t2":        " Harness lusearch -size default -n 20 -t 2 -c MyCallback",#20
          "lusearch_def_t4":        " Harness lusearch -size default -n 20 -t 4  -c MyCallback ",#20
          #"lusearch_def_t6":        " Harness lusearch -size default -n 20 -t 6  -c MyCallback ",#20
          #"lusearch_def_t8":        " Harness lusearch -size default -n 20 -t 8  -c MyCallback ",#20
          #"lusearch_def":           " Harness lusearch -size default -n 20 -c MyCallback ",#20
          "lusearch_large_t2":      " Harness lusearch -size large -n 5 -t 2 -c MyCallback ",#5
          "lusearch_large_t4":      " Harness lusearch -size large -n 5 -t 4  -c MyCallback",#5
          #"lusearch_large_t6":      " Harness lusearch -size large -n 5 -t 6 -c MyCallback ",#5
          #"lusearch_large_t8":      " Harness lusearch -size large -n 5 -t 8 -c MyCallback ",#5
          #"lusearch_large":         " Harness lusearch -size large -n 5 -c MyCallback ",#5
          "lusearch_small":         " Harness lusearch -size small -n 50  -c MyCallback",#50
          "spring_small_t2":        " Harness spring -size small -n 50 -c MyCallback",#50
          "spring_def_t2":          " Harness spring -size default -n 20 -t 2 -c MyCallback",#20
          "spring_large_t2":        " Harness spring -size large -n 5 -t 2 -c MyCallback",#5
          ##"spring_large":           " Harness spring -size large -n 5 -c MyCallback",#5
          "tomcat_small_t4":        " Harness tomcat -size small -n 50 -t 4 -c MyCallback ",#50
          "tomcat_def_t2":          " Harness tomcat -size default -n 20 -t 2 -c MyCallback ",#20
          "tomcat_def_t4":          " Harness tomcat -size default -n 20 -t 4 -c MyCallback ",#20
          #"tomcat_def_t6":          " Harness tomcat -size default -n 20 -t 6 -c MyCallback ",#20
          #"tomcat_def_t8":          " Harness tomcat -size default -n 20 -t 8 -c MyCallback ",#20
          #"tomcat_def":             " Harness tomcat -size default -n 20 -c MyCallback ",#20
          "tomcat_large_t2":        " Harness tomcat -size large -n 5 -t 2  -c MyCallback",#5
          "tomcat_large_t4":        " Harness tomcat -size large -n 5 -t 4 -c MyCallback ",#5
          #"tomcat_large_t6":        " Harness tomcat -size large -n 5 -t 6 -c MyCallback ",#5
          #"tomcat_large_t8":        " Harness tomcat -size large -n 5 -t 8 -c MyCallback ",#5
          #"tomcat_large":           " Harness tomcat -size large -n 5 -c MyCallback ",#5
          "kafka_def":              " Harness kafka -size default -n 20 -c MyCallback ",#20
          "kafka_small":            " Harness kafka -size small -n 50 -c MyCallback ",#50
          "h2_large_t2":            " Harness h2 -size large -n 5 -t 2 -c MyCallback ",#5
          "h2_large_t4":               " Harness h2 -size large -n 5 -t 4 -c MyCallback",#5
          "jme_small":              " Harness jme -size small -n 50 -c MyCallback",#20
          "jme_def":                " Harness jme -size default -n 20 -c MyCallback",#20
          "jme_large":              " Harness jme -size large -n 10 -c MyCallback",#20
}

#Specify bms
BM_Hazelcast = {
      #"hazelcast_400":              " org.example.StreamingRound2 400000",
      "hazelcast_250":             	" org.example.StreamingRound2 250000",
      "hazelcast_100":             	" org.example.StreamingRound2 100000",
      "hazelcast_20":             	" org.example.StreamingRound2 20000",
      }
#BM_specjbb2015 = {
      #"specjbb15":             	" -m COMPOSITE -ikv -p "
      #"specjbb15_100":             	" -m COMPOSITE",#IR=21000
      #"specjbb15_75":             	" -m COMPOSITE",#IR=15750
      #"specjbb15_50":             	" -m COMPOSITE",#IR=10500
      #"specjbb15_25":             	" -m COMPOSITE",#IR=5250
#      }
BM_specjbb2015 = {
      "specjbb15_100":             	" -m COMPOSITE -p ../spec/config/specjbb2015100.props -ikv",
      "specjbb15_75":             	" -m COMPOSITE -p ../spec/config/specjbb201575.props -ikv",
      "specjbb15_50":             	" -m COMPOSITE -p ../spec/config/specjbb201550.props -ikv",
      #"specjbb15_25":             	" -m COMPOSITE -p ../spec/config/specjbb201525.props -ikv",
      #"specjbb15_100":             	" -m COMPOSITE -p ../spec/config/specjbb2015.props",
      #"specjbb15_75":             	" -m COMPOSITE -p ../spec/config/specjbb2015.props",
      #"specjbb15_50":             	" -m COMPOSITE -p ../spec/config/specjbb2015.props",
      #"specjbb15_25":             	" -m COMPOSITE -p ../spec/config/specjbb2015.props ",
      }
BM_Renaissance = {
      "finagle-chirper":        "finagle-chirper ",#web
      "finagle-http":           "finagle-http",
}
#In this table, we have 1x heap size. 
#It is the first heap size which allows an application to run without 
#allocation stalls (+ 1x*0.2 because there is fluctuation)
HEAP_SIZES = {
        "h2_large_t2":      "5000m", #"5000m",
        "h2_large":         "7250m",#"8000m",
        "tomcat_small_t8":  "165m", 
        "tomcat_def_t2":    "175m",
        "tomcat_def_t4":    "175m",
        "tomcat_def_t6":    "175m",
        "tomcat_def_t8":    "175m",
        "tomcat_def":       "175m",
        "tomcat_large_t2":  "175m",
        "tomcat_large_t4":  "175m",
        "tomcat_large_t6":  "175m",
        "tomcat_large_t8":  "175m",
        "tomcat_large":     "260m",
        "kafka_def":        "600m", #"830m",
        "kafka_small":      "230m", #"290m",
        "finagle-chirper":  "2400m",
        "finagle-http":     "620m",
        "hazelcast_100":    "2000m",
        "hazelcast_20":     "2100m",
        "hazelcast_250":    "2900m",
        "hazelcast_400":    "3500m",
        "specjbb15_50":     "16000m", #"86000m",
        "specjbb15_75":     "23000m", #"80000m",
        "specjbb15_100":    "23000m", #"72000m",
        "lusearch_def_t2":  "240m",
        "lusearch_def_t4":  "350m",
        "lusearch_def_t6":  "700m",
        "lusearch_def_t8":  "860m",
        "lusearch_def":     "3500m",
        "lusearch_large_t2":"360m",
        "lusearch_large_t4":"430m",
        "lusearch_large_t6":"620m",
        "lusearch_large_t8":"1300m",
        "lusearch_large":   "3200m",
        "lusearch_small":   "150m", #"175m",
        "lusearch_huge_t2": "360m",
        "lusearch_huge_t4": "360m",
        "lusearch_huge_t6": "360m",
        "lusearch_huge_t8": "430m",
        "lusearch_huge":    "2060m",
        "jme_def":          "86m",
        "jme_small":        "86m",
        "jme_large":        "100m",
        "spring_small_t2":  "250m",
        "spring_large_t2":  "2900m",
        "spring_def_t2":    "520m",
}

def get_next_result_name(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return str(len(files) + 1) + ".txt"

def get_current_result_name(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return str(len(files)) + ".txt"

def collect_data(binary, result_path):
    app = subprocess.Popen(binary, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,shell=True,bufsize=1)
    pathlib.Path(result_path).mkdir(parents=True, exist_ok=True)
    result_file = os.path.join(result_path, get_next_result_name(result_path))
    with open(result_file, "w") as writeFile:
        for line in app.stdout:
            writeFile.write(line)

    writeFile.close()
    return result_file

#We need to decide which space between heap sizes we want.
#For consistency we can increase the heapsize of all the bms by the same amount
#that it is representative when we compare configurations
def heap_size_array(BM_tag, HEAP_RUNS):
    start_HS = 10
    start_Value = "m"
    param_max = "-Xmx"
    param_min = " -Xms"
    space = 0
    HS = {}
    for (HS_tag, HS_conf) in HEAP_SIZES.items():
        #print (HS_conf)
        if HS_tag in BM_tag:
            start_HS = int(''.join(filter(str.isdigit, HS_conf)))
    space = int(start_HS * 0.5)
    tag = ""
    for i in range (0, HEAP_RUNS):
        conf = param_max + str(start_HS + space*i) + start_Value + param_min + str(start_HS+ space*i) + start_Value
        tag = str(1 + i*0.5)
        '''if "spec" not in BM_tag:
            conf = param_max + str(start_HS + space*i) + start_Value + param_min + str(start_HS+ space*i) + start_Value
            print(conf)
            if "hazelcast" not in BM_tag:
                tag = str(1 + i*0.5)
                if (i > 7): #if (i > 3):
                    continue
            else:
                if (i == 1):
                    continue
                if (i == 4):
                    continue
                tag = str(1 + round(i/11, 1))
                print(tag)
        else:
            if (i > 3):
                continue
            tag = str(1.0 + i*0.5)
            if i >=3:
                space = int(start_HS)
                tag = str(1.0 + i)
            conf = param_max + str(start_HS + space*i) + start_Value'''
        HS[tag] = conf
    return HS

def pipe_fopen(command, background=True):

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

        def background_command_waiter(command, p):
            p.wait()
            #print(p.returncode)
            #if p.returncode != -9:
            #    warnings.warn("Command \"{0}\" exited with status {1}".format(
            #        command, p.returncode))
            #    _thread.interrupt_main()

        if background:
                thread = threading.Thread(target=background_command_waiter,args=(command, p))
                # exits abnormally if main thread is terminated .
                thread.daemon = True
                thread.start()
        else:
                background_command_waiter(command, p)
        return p

def execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, HW_tag, HW, GC, JAVA_tag, JAVA, JAVA_LOG, Callback, CLASSPATH, COMMAND, RES_FOLDER):
    for (GC_tag, GC_conf) in GC.items():
        HS = heap_size_array(BM_tag, HEAP_RUNS)
        for (HS_tag, HS_conf) in HS.items():
            for i in range(0, PASSES):
                result_path = os.path.join(os.getcwd(), RES_FOLDER, BM_tag, JAVA_tag + GC_tag + HS_tag + "_" + HW_tag)
                os.system("sudo mkdir -p " + result_path)
                os.system("sudo chmod 777 " + result_path)
                #cmd = "vmstat 1 >> output.txt"
                #vmstat = pipe_fopen(cmd)
                binary_hot = " ".join([HW, COMMAND, JAVA, JAVA_LOG, HS_conf, GC_conf, CLASSPATH, BM_conf, Callback])
                print(binary_hot)
                collect_data(binary_hot, result_path)
                #vmstat.kill()
                os.system("./cache-flush")
                if "hazelcast" in BM_tag:
                    f1_path = os.path.join(result_path, get_current_result_name(result_path))
                    f2_path = os.path.join(os.getcwd(), "histo-latency/0")
                    # opening first file in append mode and second file in read mode
                    f1 = open(f1_path, 'a+')
                    f2 = open(f2_path, 'r')
                    # appending the contents of the second file to the first file
                    f1.write(f2.read())
                    os.system("sudo rm -rf " + f2_path)
                #CPUUtil.parse_CPU_Util(result_path, get_current_result_name(result_path))
                #os.system("rm -rf output.txt")
            #os.system("mkdir  ../benchmark_run/results_pids/" + BM_tag +"/")
            #os.system("mkdir  ../benchmark_run/results_pids/" + BM_tag +"/"+ JAVA_tag + GC_tag + HS_tag + "/")
            #os.system("mv ../pytop/demofile3.txt ../benchmark_run/results_pids/" + BM_tag +"/"+ JAVA_tag + GC_tag + HS_tag + "/GC_pids.txt")
            #os.system("mv ../benchmark_run/GC_pids" + GC_pid_tag + ".txt ../benchmark_run/results_pids/" + BM_tag + "/" + JAVA_tag + GC_tag + HS_tag + "/GC_pids.txt")

def main(argv):
    PASSES=10
    HEAP_RUNS=1
    try:
        opts, args = getopt.getopt(argv,"hrs:",["runs=","sizes="])
    except getopt.GetoptError:
      print('collect_data.py -r <number_of_runs> -s <how_many_heap_sizes_to_run>')
      sys.exit(2)
    for opt, arg in opts:
        print(opt)
        print(arg)
        if opt == '-h':
            print('collect_data.py -r <number_of_runs> -s <how_many_heap_sizes_to_test> -n <use_NUMA_yes(1)_or_no(0)>')
            sys.exit()
        elif opt in ("-r", "--runs"):
            try:
                PASSES = int(arg)
            except ValueError:
                PASSES = 10
        elif opt in ("-s", "--sizes"):
            try:
                HEAP_RUNS = int(arg)
            except ValueError:
                HEAP_RUNS = 1
    print("Starting to collect data with " + str(PASSES) + " passes")
    #cmd = "../pytop/pytop -H"
    #p = Popen(cmd.split())
    for BM in Which_BM:
            print(BM)
            COMMAND = ""
            JAVA_LOG_local = ""
            JAVA_LOG_local = JAVA_LOG
            #COMMAND = "sudo ./../rapl-tools/AppPowerMeter "
            COMMAND = "sudo  "

            #RES_FOLDER = "../benchmark_run/results_test"
            RES_FOLDER = "../benchmark_run/results"

            BM_suffix = ""
            JAVA_tag = ""
            JAVA_local = ""
            PASSES=10#there
            JAVA_LOG_local = JAVA_LOG
            
            #print(JAVA_local)
            if "specjbb2015" in BM:
                COMMAND = "sudo ./../rapl-tools/AppPowerMeter "
                for (BM_tag, BM_conf) in BM_specjbb2015.items():
                    for (GC_thread_tag, GC_thread_conf) in GC_threads.items():
                        GC_thread_full_tag = "_T" + str(GC_thread_tag)
                        for (HW_conf_tag, HW) in HW_conf.items():
                            if "8P" in HW_conf_tag:
                                JAVA_local = JAVA20_GEN
                                JAVA_tag = "G"
                                os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, CONFIG_SPEC, " -jar " + CLASSPATH_SPEC, COMMAND, RES_FOLDER)
                            
                                JAVA_local = JAVA20_RESTRICTED
                                JAVA_tag = "G"
                                os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, "4P4P", HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, CONFIG_SPEC, " -jar " + CLASSPATH_SPEC, COMMAND, RES_FOLDER)

                            elif "4P4P" in HW_conf_tag:
                                JAVA_local = JAVA20_4P4P
                                JAVA_tag = "S"
                                #os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, CONFIG_SPEC, " -jar " + CLASSPATH_SPEC, COMMAND, RES_FOLDER)
                                
                            elif "4P4E" in HW_conf_tag:
                                JAVA_local = JAVA20_4P4E
                                JAVA_tag = "SYY"
                                #os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, CONFIG_SPEC, " -jar " + CLASSPATH_SPEC, COMMAND, RES_FOLDER)
            

            elif "Renaissance" in BM:
                COMMAND = "sudo ./../rapl-tools/AppPowerMeter "
                for (BM_tag, BM_conf) in BM_Renaissance.items():
                    for (GC_thread_tag, GC_thread_conf) in GC_threads.items():
                        GC_thread_full_tag = "_T" + str(GC_thread_tag)
                        for (HW_conf_tag, HW) in HW_conf.items():
                            if "8P" in HW_conf_tag:
                                JAVA_local = JAVA20_GEN
                                JAVA_tag = "G"
                                os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS,  BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC,JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " -jar " + CLASSPATH_RN, COMMAND, RES_FOLDER)
            
                                JAVA_local = JAVA20_RESTRICTED
                                JAVA_tag = "G"
                                os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS,  BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, "4P4P", HW, GC,JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " -jar " + CLASSPATH_RN, COMMAND, RES_FOLDER)
                            
                            else:
                                JAVA_local = JAVA20_GEN
                                JAVA_tag = "G"
                                os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS,  BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC,JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " -jar " + CLASSPATH_RN, COMMAND, RES_FOLDER)
                                

                                JAVA_local = JAVA20_YinYan
                                JAVA_tag = "YY"
                                os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS,  BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC,JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " -jar " + CLASSPATH_RN, COMMAND, RES_FOLDER)

            elif "HazelCast" in BM:
                COMMAND = "sudo ./../rapl-tools/AppPowerMeter "
                for (BM_tag, BM_conf) in BM_Hazelcast.items():
                    for (GC_thread_tag, GC_thread_conf) in GC_threads.items():
                        GC_thread_full_tag = "_T" + str(GC_thread_tag)
                        for (HW_conf_tag, HW) in HW_conf.items():
                            if "8P" in HW_conf_tag:
                                JAVA_local = JAVA20_GEN
                                JAVA_tag = "G"
                                os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS, BM_tag + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST, COMMAND, RES_FOLDER)
                            
                                JAVA_local = JAVA20_RESTRICTED
                                JAVA_tag = "G"
                                os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS, BM_tag + GC_thread_full_tag, BM_conf, "4P4P", HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST, COMMAND, RES_FOLDER)

                            elif "4P4P" in HW_conf_tag:
                                JAVA_local = JAVA20_4P4P
                                JAVA_tag = "S"
                                #os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS, BM_tag + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST, COMMAND, RES_FOLDER)
                                
                            elif "4P4E" in HW_conf_tag:
                                JAVA_local = JAVA20_4P4E
                                JAVA_tag = "SYY"
                                #os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS, BM_tag + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST, COMMAND, RES_FOLDER)

            elif "DaCapo" in BM:
                #COMMAND = "sudo ./../rapl-tools/AppPowerMeter "
                COMMAND = "sudo "
                for (BM_tag, BM_conf) in BM_DaCapo.items():
                    for (GC_thread_tag, GC_thread_conf) in GC_threads.items():
                        GC_thread_full_tag = "_T" + str(GC_thread_tag)
                        for (HW_conf_tag, HW) in HW_conf.items():
                            if "8P" in HW_conf_tag:
                                JAVA_local = JAVA20_GEN
                                JAVA_tag = "G"
                                os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " -cp " + CLASSPATH_DACAPO, COMMAND, RES_FOLDER)

                                JAVA_local = JAVA20_RESTRICTED
                                JAVA_tag = "G"
                                os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, "4P4P", HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " -cp " + CLASSPATH_DACAPO, COMMAND, RES_FOLDER)
                            
                            elif "4P4P" in HW_conf_tag:
                                JAVA_local = JAVA20_4P4P
                                JAVA_tag = "S"
                                #os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " -cp " + CLASSPATH_DACAPO, COMMAND, RES_FOLDER)
                                
                            elif "4P4E" in HW_conf_tag:
                                JAVA_local = JAVA20_4P4E
                                JAVA_tag = "SYY"
                                #os.system("rm -rf output.txt")
                                execute_bm(PASSES, HEAP_RUNS, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " -cp " + CLASSPATH_DACAPO, COMMAND, RES_FOLDER)


if __name__ == "__main__": main(sys.argv[1:])

