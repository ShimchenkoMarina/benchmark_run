#Olof's project collect data
import subprocess
import threading
import _thread
import warnings
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
JAVA20_CRITICAL = ""
JAVA20_GEN=""
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
    if "JAVA20_CRITICAL"==variable:
        JAVA20_CRITICAL=line.split("=")[1].split("\"")[1]
    if "JAVA20_GEN"==variable:
        JAVA20_GEN=line.split("=")[1].split("\"")[1]
    if "JAVA20_MARK"==variable:
        JAVA20_MARK=line.split("=")[1].split("\"")[1]

FLAGS_HAZELCAST="--add-modules java.se --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.nio=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED"

#Java log
JAVA_LOG = " -Xlog:gc* "
JAVA_LOG_ALLOCATION_RATE = "-Xlog:gc+stats"
#Specify here which bm+java you want to run
Which_BM = {
            #"DaCapo",
            #"HazelCast",
            "specjbb2015",
            #"Renaissance",
}
GC_threads = {
        "8" : "-XX:ConcGCThreads=8", 
        #"4"  : "-XX:ConcGCThreads=4"
}
HW_conf = {
        #"8P8E": ""
        #"8P" : "numactl -C 0-15 sudo ", 
        "4P4E"  : "numactl -C 0-7,16-19"
}

#Specify GCs for each java version
GC = {
    'Z': '-XX:+UseZGC' ,
}
#Specify bms
BM_DaCapo = {
          #"jme_small":              " jme -size small -n 50",#20
          #"jme_def":                " jme -size default -n 20",#20
          #"jme_large":              " jme -size large -n 10",#20
          #"lusearch_def_t2":        " lusearch -size default -n 20 -t 2",#20
          #"lusearch_def_t4":        " lusearch -size default -n 20 -t 4",#20
          #"lusearch_def_t6":        " lusearch -size default -n 20 -t 6",#20
          #"lusearch_def_t8":        " lusearch -size default -n 20 -t 8",#20
          #"lusearch_def":           " lusearch -size default -n 20",#20
          #"lusearch_large_t2":      " lusearch -size large -n 5 -t 2",#5
          #"lusearch_large_t4":      " lusearch -size large -n 5 -t 4",#5
          #"lusearch_large_t6":      " lusearch -size large -n 5 -t 6",#5
          #"lusearch_large_t8":      " lusearch -size large -n 5 -t 8",#5
          #"lusearch_large":         " lusearch -size large -n 5",#5
          #"lusearch_huge_t2":       " lusearch -size huge -n 5 -t 2",#5
          #"lusearch_huge_t4":       " lusearch -size huge -n 5 -t 4",#5
          #"lusearch_huge_t6":       " lusearch -size huge -n 5 -t 6",#5
          #"lusearch_huge_t8":       " lusearch -size huge -n 5 -t 8",#5
          #"lusearch_huge":          " lusearch -size huge -n 5",#5
          #"lusearch_small":         " lusearch -size small -n 50",#50
          #"spring_small_t2":        " spring -size small -n 50 --ignore-validation",#50
          #"spring_def_t2":          " spring -size default -n 20 --ignore-validation",#20
          #"spring_large_t2":        " spring -size large -n 5 --ignore-validation -t 2",#5
          #"spring_large":           " spring -size large -n 5 --ignore-validation",#5
          #"tomcat_small_t8":        " tomcat -size small -n 50",#50
          #"tomcat_def_t2":          " tomcat -size default -n 20 -t 2",#20
          #"tomcat_def_t4":          " tomcat -size default -n 20 -t 4",#20
          #"tomcat_def_t6":          " tomcat -size default -n 20 -t 6",#20
          #"tomcat_def_t8":          " tomcat -size default -n 20 -t 8",#20
          #"tomcat_def":             " tomcat -size default -n 20",#20
          #"tomcat_large_t2":        " tomcat -size large -n 5 -t 2",#5
          #"tomcat_large_t4":        " tomcat -size large -n 5 -t 4",#5
          #"tomcat_large_t6":        " tomcat -size large -n 5 -t 6",#5
          #"tomcat_large_t8":        " tomcat -size large -n 5 -t 8",#5
          #"tomcat_large":           " tomcat -size large -n 5",#5
          #"kafka_def":              " kafka -size default -n 20",#20
          "kafka_small":            " Harness kafka -size small -n 50 -c MyCallback",#50
          "h2_large_t2":            " Harness h2 -size large -n 5 -t 2 -c MyCallback",#5
          "h2_large":               " Harness h2 -size large -n 5 -c MyCallback",#5
          "h2_huge_t2":             " Harness h2 -size huge -n 5 -t 2 -c MyCallback",#5
          "h2_huge":                " Harness h2 -size huge -n 5 -c MyCallback",#5


}

#Specify bms
BM_Hazelcast = {
      #"hazelcast_1500":             " org.example.StreamingRound2 1500000",
      #"hazelcast_400":             	" org.example.StreamingRound2 400000",
      #"hazelcast_100":             	" org.example.StreamingRound2 100000",
      #"hazelcast_400":             	" org.example.StreamingRound2 400000",
      #"hazelcast_20":             	" org.example.StreamingRound2 20000",
      #"hazelcast_150":             	" org.example.StreamingRound2 15000",
      #"hazelcast_200":             	" org.example.StreamingRound2 200000",
      #"hazelcast_250":             	" org.example.StreamingRound2 250000",
      #"hazelcast_300":             	" org.example.StreamingRound2 300000",
      }
BM_specjbb2015 = {
      "specjbb15_100":             	" -m COMPOSITE -p ../spec/config/specjbb2015100.props -ikv",
      "specjbb15_75":             	" -m COMPOSITE -p ../spec/config/specjbb201575.props -ikv",
      "specjbb15_50":             	" -m COMPOSITE -p ../spec/config/specjbb201550.props -ikv",
      "specjbb15_25":             	" -m COMPOSITE -p ../spec/config/specjbb201525.props -ikv",
      #"specjbb15_100":             	" -m COMPOSITE -p ../spec/config/specjbb2015.props",
      #"specjbb15_75":             	" -m COMPOSITE -p ../spec/config/specjbb2015.props",
      #"specjbb15_50":             	" -m COMPOSITE -p ../spec/config/specjbb2015.props",
      #"specjbb15_25":             	" -m COMPOSITE -p ../spec/config/specjbb2015.props ",
      }
BM_Renaissance = {
      #"finagle-chirper":        "finagle-chirper ",#web
      #"finagle-http":           "finagle-http",
}
#The maximum heap size for each application is set to 3X of its respective minimum heap size
HEAP_SIZES = {
        "h2_huge_t2":       "3500m",
        "h2_large_t2":      "3500m",
        "h2_huge":          "3500m",
        "h2_large":         "3500m",
        "tomcat_small_t8":  "139m", 
        "tomcat_def_t2":    "144m",
        "tomcat_def_t4":    "144m",
        "tomcat_def_t6":    "144m",
        "tomcat_def_t8":    "144m",
        "tomcat_def":       "144m",
        "tomcat_large_t2":  "144m",
        "tomcat_large_t4":  "144m",
        "tomcat_large_t6":  "144m",
        "tomcat_large_t8":  "144m",
        "tomcat_large":     "144m",
        "kafka_def":        "691m",
        "kafka_small":      "240m",
        "finagle-chirper":  "518m",
        "finagle-http":     "414m",
        "hazelcast_100":    "1680m",
        "hazelcast_20":     "1728m",
        "hazelcast_250":    "2016m",
        "hazelcast_400":    "2304m",
        "specjbb15_25":     "16000m",
        "specjbb15_50":     "16000m",
        "specjbb15_75":     "16000m",
        "specjbb15_100":    "16000m",
        "lusearch_def_t2":  "200m",
        "lusearch_def_t4":  "288m",
        "lusearch_def_t6":  "595m",
        "lusearch_def_t8":  "714m",
        "lusearch_def":     "1027m",
        "lusearch_large_t2":"300m",
        "lusearch_large_t4":"360m",
        "lusearch_large_t6":"518m",
        "lusearch_large_t8":"1072m",
        "lusearch_large":   "2221m",
        "lusearch_small":   "144m",
        "lusearch_huge_t2": "300m",
        "lusearch_huge_t4": "300m",
        "lusearch_huge_t6": "300m",
        "lusearch_huge_t8": "360m",
        "lusearch_huge":    "1072m",
        "jme_def":          "72m",
        "jme_small":        "72m",
        "jme_large":        "84m",
        "spring_small_t2":  "206m",
        "spring_large_t2":  "240m",
        "spring_large":     "714m",
        "spring_def_t2":    "206m",
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
def start_heap_size(BM_tag):
    for (HS_tag, HS_conf) in HEAP_SIZES.items():
        #print (HS_conf)
        if HS_tag==BM_tag:
            start_HS = int(''.join(filter(str.isdigit, HS_conf)))
    return start_HS

def get_HS_conf(HS_Value):
    start_Value = "m"
    param_max = "-Xmx"
    param_min = " -Xms"
    return param_max + str(HS_Value) + start_Value + param_min + str(HS_Value) + start_Value

def allocation_stalls(file):
    print(file)
    with open(file, 'r') as reader:
            for line in reader.readlines():
                if "Allocation Stall (" in line:
                    return True
    return False

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

last_HS = 1

def push_HS(val):
    global last_HS
    last_HS = val

def pop_HS():
    global last_HS
    return last_HS

#TODO: add GROUP_TAG into the path when run for features collecting.
def execute_bm(HS_value, BM_tag, BM_conf, HW_tag, HW, GC,JAVA_tag, JAVA, JAVA_LOG, Callback, CLASSPATH, COMMAND, RES_FOLDER):
    for (GC_tag, GC_conf) in GC.items():
        HS = get_HS_conf(HS_value)
        result_path = os.path.join(os.getcwd(), RES_FOLDER, BM_tag, JAVA_tag + "_H" + str(HS_value) + "_" + HW_tag)
        os.system("sudo mkdir -p " + result_path)
        os.system("sudo chmod 777 " + result_path)
        #Sometimes Allocation Stall does not show up after one run. 
        i = 0
        flag = False
        while i < 3:
            cmd = "vmstat 1 >> output.txt"
            vmstat = pipe_fopen(cmd)
            binary_hot = " ".join([HW, COMMAND, JAVA, JAVA_LOG, HS, GC_conf, CLASSPATH, BM_conf, Callback])
            print(binary_hot)
            collect_data(binary_hot, result_path)
            vmstat.kill()
            os.system("./cache-flush")
            i = i + 1
            if allocation_stalls(result_path + "/" + get_current_result_name(result_path)):
                HS_value = int(HS_value * 1.2)
                HS = get_HS_conf(HS_value)
                os.system("rm -rf output.txt")
                execute_bm(HS_value, BM_tag, BM_conf, HW_tag, HW, GC, JAVA_tag, JAVA, JAVA_LOG, Callback, CLASSPATH, COMMAND, RES_FOLDER)
                flag = True
                break
        if i == 3 and flag==False:
            #print("no")
            #Check the CPU utilization
            CPUUtil.parse_CPU_Util(result_path)
            os.system("rm -rf output.txt")
            #push_HS(HS_value)



def main(argv):
    PASSES=6
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
    for BM in Which_BM:
        print(BM)
        COMMAND = ""
        JAVA_LOG_local = JAVA_LOG
        RES_FOLDER = "../benchmark_run/test3"
        BM_suffix = ""
        GC_pid_tag = ""
        JAVA_tag = "" 
        JAVA_local = JAVA20_YinYan
            
        if "specjbb2015" in BM:
                for (BM_tag, BM_conf) in BM_specjbb2015.items():
                    for (GC_thread_tag, GC_thread_conf) in GC_threads.items():
                        GC_thread_full_tag = "_T" + str(GC_thread_tag)
                        for (HW_conf_tag, HW) in HW_conf.items():
                            JAVA_local = JAVA20_YinYan
                            HS_value = start_heap_size(BM_tag)
                            os.system("rm -rf output.txt")
                            execute_bm(HS_value, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, CONFIG_SPEC, " -jar " + CLASSPATH_SPEC, COMMAND, RES_FOLDER)
                            
                            #JAVA_local = JAVA20_GEN
                            #HS_value = start_heap_size(BM_tag)
                            #os.system("rm -rf output.txt")
                            #execute_bm(HS_value, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, CONFIG_SPEC, " -jar " + CLASSPATH_SPEC, COMMAND, RES_FOLDER)
        elif "Renaissance" in BM:
                for (BM_tag, BM_conf) in BM_Renaissance.items():
                    for (GC_thread_tag, GC_thread_conf) in GC_threads.items():
                        GC_thread_full_tag = "_T" + str(GC_thread_tag)
                        for (HW_conf_tag, HW) in HW_conf.items():
                            HS_value = start_heap_size(BM_tag)
                            os.system("rm -rf output.txt")
                            execute_bm(HS_value, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC,JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " -jar " + CLASSPATH_RN, COMMAND, RES_FOLDER)
        elif "HazelCast" in BM:
                for (BM_tag, BM_conf) in BM_Hazelcast.items():
                    for (GC_thread_tag, GC_thread_conf) in GC_threads.items():
                        GC_thread_full_tag = "_T" + str(GC_thread_tag)
                        for (HW_conf_tag, HW) in HW_conf.items():
                            HS_value = start_heap_size(BM_tag)
                            os.system("rm -rf output.txt")
                            execute_bm(HS_value, BM_tag + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST, COMMAND, RES_FOLDER)

        elif "DaCapo" in BM:
                for (BM_tag, BM_conf) in BM_DaCapo.items():
                    for (GC_thread_tag, GC_thread_conf) in GC_threads.items():
                        GC_thread_full_tag = "_T" + str(GC_thread_tag)
                        for (HW_conf_tag, HW) in HW_conf.items():
                            JAVA_local = JAVA20_YinYan
                            HS_value = start_heap_size(BM_tag)
                            #for t in range(2, 10, 2):
                            os.system("rm -rf output.txt")
                            #BM_suffix = "_t" + str(t)
                            execute_bm(HS_value, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " -cp " + CLASSPATH_DACAPO, COMMAND, RES_FOLDER)
                            #HS_value = pop_HS()

                            JAVA_local = JAVA20_GEN
                            HS_value = start_heap_size(BM_tag)
                            os.system("rm -rf output.txt")
                            execute_bm(HS_value, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " -cp " + CLASSPATH_DACAPO, COMMAND, RES_FOLDER)
                            #os.system("rm -rf output.txt")
                            #HS_value = start_heap_size(BM_tag)
                            #BM_suffix = "_tND"
                            #GC_thread_tag = "_T" + str(GC_thread_tag)
                            #execute_bm(HS_value, BM_tag + BM_suffix + GC_thread_full_tag, BM_conf, HW_conf_tag, HW, GC, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads " + GC_thread_conf, "", " -jar " + CLASSPATH_DACAPO, COMMAND, RES_FOLDER)

if __name__ == "__main__": main(sys.argv[1:])

