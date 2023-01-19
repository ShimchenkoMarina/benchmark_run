import subprocess
import os
import pathlib
from os.path import isfile, join
from os import listdir
import platform
from timeit import default_timer as timer
import sys, getopt
import signal
import time
import shlex
import psutil
#Path variables
JAVA20 = ""
JAVA20_CPUO = ""
CLASSPATH_DACAPO=""
CLASSPATH_HAZELCAST=""
CLASSPATH_RENAISSANE=""
CLASSPATH_SPEC=""
MyCallback_RENAISSANCE=""

file = open('path_file.txt', 'r')
for line in file:
    variable = line.split("=")[0]
    if "CLASSPATH_DACAPO" in variable:    
        CLASSPATH_DACAPO=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_HAZELCAST" in variable:    
        CLASSPATH_HAZELCAST=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_RENAISSANCE" in variable:    
        CLASSPATH_RENAISSANCE=line.split("=")[1].split("\"")[1]
    if "MyCallback_RENAISSANCE" in variable:    
        MyCallback_RENAISSANCE=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_SPEC" in variable:    
        CLASSPATH_SPEC=line.split("=")[1].split("\"")[1]
    if "JAVA20_CPUO" in variable:
        JAVA20_CPUO=line.split("=")[1].split("\"")[1]
    if "JAVA20" in variable and "_CPUO" not in variable:
        JAVA20=line.split("=")[1].split("\"")[1]

FLAGS_HAZELCAST="--add-modules java.se --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.nio=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED"

JAVA_LOG = " -Xlog:gc* "

#Specify here which bm+java you want to run
Which_BM = {
        "Dacapo",
        "Renaissance",
        "Hazelcast",
        "Spec",
} 

#Specify GCs for each java version
GC = { 
    "j20Z": "-XX:+UseZGC",
}

NUMA = { 
    "_8": "numactl -C 0-7 ",
    "_16": "numactl -C 0-15 ",
    "_32": " ",
}


CPUO = {"1": "-Xgco1", "2":"-Xgco2", "5":"-Xgco5", "10":"-Xgco10"}
#CPUO = {"15": "-Xgco15", "20":"-Xgco20", "5":"-Xgco5", "10":"-Xgco10", "45": "-Xgco45"}

#Specify bms
BM_DaCapo = {
      "h2_small":             	" h2 -size small -n 50",#50
      #"h2_large":             	" h2 -size large -n 30",#30
      #"h2_huge":              	" h2 -size huge -n 10",
      "lusearch_large":          	" lusearch -size large -n 20",
      "lusearch_large_t8":          	" lusearch -size large -n 20 -t 8",
      "lusearch_large_t6":          	" lusearch -size large -n 20 -t 6",
      "lusearch_large_t4":          	" lusearch -size large -n 20 -t 4",
      "lusearch_large_t2":          	" lusearch -size large -n 20 -t 2",
      "lusearch_def":          	" lusearch -size default -n 20",
      "lusearch_def_t8":          	" lusearch -size default -n 20 -t 8",
      "lusearch_def_t6":          	" lusearch -size default -n 20 -t 6",
      "lusearch_def_t4":          	" lusearch -size default -n 20 -t 4",
      "lusearch_def_t2":          	" lusearch -size default -n 20 -t 2",

}
BM_Hazelcast = {
      "hazelcast_100":             	" org.example.StreamingRound3 100000",
      "hazelcast_400":             	" org.example.StreamingRound3 400000",
      "hazelcast_800":             	" org.example.StreamingRound3 800000",
      "hazelcast_20":             	" org.example.StreamingRound3 20000"
      }
BM_specjbb2015 = {
      "specjbb15_100":             	" -m COMPOSITE -ikv -p ../spec/config/specjbb2015100.props",
      "specjbb15_75":             	" -m COMPOSITE -ikv -p ../spec/config/specjbb201575.props",
      "specjbb15_50":             	" -m COMPOSITE -ikv -p ../spec/config/specjbb201550.props",
      "specjbb15_25":             	" -m COMPOSITE -ikv -p ../spec/config/specjbb201525.props",
      }

BM_Renaissance = {
      "finagle-chirper":        "finagle-chirper --plugin ",#web
      "finagle-http":           "finagle-http --plugin ",
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
def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def collect_data_kill(binary, result_path):
    app = subprocess.Popen(shlex.split(binary), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,shell=False,bufsize=1)
    # If thread is active
    try:
        outs, errs = app.communicate(timeout=600)
        pathlib.Path(result_path).mkdir(parents=True, exist_ok=True)
        result_file = os.path.join(result_path, get_next_result_name(result_path))
        print(result_file)
        with open(result_file, "w") as writeFile:
            for line in outs:
                writeFile.write(line)

        writeFile.close()
        return result_file
    except subprocess.TimeoutExpired:
            kill(app.pid)
            outs, errs = app.communicate()
            pathlib.Path(result_path).mkdir(parents=True, exist_ok=True)
            result_file = os.path.join(result_path, get_next_result_name(result_path))
            print(result_file)
            with open(result_file, "w") as writeFile:
                writeFile.write(outs)

            writeFile.close()
            return result_file

#TODO: add GROUP_TAG into the path when run for features collecting. 
def execute_bm(PASSES, BM_tag, BM_conf, JAVA_tag, JAVA, JAVA_LOG, Callback, CLASSPATH, RES_FOLDER):
    #print("Benchmarking " + BM_tag)
    for i in range(0, PASSES):
        for (GC_tag, GC_conf) in GC.items():
            for (NUMA_tag, NUMA_conf) in NUMA.items():
                result_path = ""
                result_path = os.path.join(os.getcwd(), RES_FOLDER, BM_tag, GC_tag + JAVA_tag + NUMA_tag)
                os.system("sudo mkdir -p " + result_path)
                os.system("sudo chmod 777 " + result_path)
                binary_cache_flush = " ".join("./cache-flush")
                COMMAND = "sudo ../rapl-tools/AppPowerMeter " + NUMA_conf 
                binary_hot = " ".join([COMMAND, JAVA, JAVA_LOG, GC_conf, CLASSPATH, BM_conf, Callback])
                print(binary_hot)
                collect_data(binary_hot, result_path)
                if "hazelcast" in BM_tag:
                    f1_path = os.path.join(result_path, get_current_result_name(result_path))
                    f2_path = os.path.join(os.getcwd(), "histo-latency/0")
                    # opening first file in append mode and second file in read mode
                    f1 = open(f1_path, 'a+')
                    f2 = open(f2_path, 'r')
                    # appending the contents of the second file to the first file
                    f1.write(f2.read())
                    os.system("sudo rm -rf " + f2_path)

def main(argv):
    try:
      opts, args = getopt.getopt(argv,"hr:s:n:",["runs=","sizes=", "numa="])
    except getopt.GetoptError:
      print('collect_data.py -r <number_of_runs> -s <how_many_heap_sizes_to_run> -n <NUMA>')
      sys.exit(2)
    for opt, arg in opts:
        print(opt)
        print(arg)
        if opt == '-h':
            print('collect_data.py -r <number_of_runs> -s <how_many_heap_sizes_to_test> -n <use_NUMA_yes(1)_or_no(0)>')
            sys.exit()
        elif opt in ("-r", "--runs"):
            PASSES = int(arg)
        elif opt in ("-s", "--sizes"):
            HEAP_RUNS = int(arg)
        elif opt in ("-n", "--numa"):
            NUMA = int(arg)
    print("Starting to collect data with " + str(PASSES) + " passes")
    for BM in Which_BM:
        print(BM)
        binary_cache_cpufreq_set = " ".join("sudo cpupower frequency-set --governor performance")
        RES_FOLDER = "results"
        if BM == "Dacapo": 
            for (BM_tag, BM_conf) in BM_DaCapo.items():
                execute_bm(PASSES, BM_tag, BM_conf,"", JAVA20, JAVA_LOG, "", "-jar " + CLASSPATH_DACAPO, RES_FOLDER)
                for (CPUO_tag, CPUO_conf) in CPUO.items():
                    execute_bm(PASSES, BM_tag, BM_conf,"_CPUO" + CPUO_tag, JAVA20_CPUO, JAVA_LOG + CPUO_conf, "", "-jar " + CLASSPATH_DACAPO, RES_FOLDER)
        elif BM ==  "Hazelcast":    
            for (BM_tag, BM_conf) in BM_Hazelcast.items():
                execute_bm(PASSES,  BM_tag, BM_conf,"", JAVA20, JAVA_LOG, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST, RES_FOLDER)
                for (CPUO_tag, CPUO_conf) in CPUO.items():
                    execute_bm(PASSES,  BM_tag, BM_conf, "_CPUO" + CPUO_tag, JAVA20_CPUO, JAVA_LOG + CPUO_conf, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST, RES_FOLDER)
        elif BM ==  "Renaissance":    
            for (BM_tag, BM_conf) in BM_Renaissance.items():
                execute_bm(PASSES, BM_tag, BM_conf,"", JAVA20, JAVA_LOG, MyCallback_RENAISSANCE, " -jar " + CLASSPATH_RENAISSANCE,  RES_FOLDER)
                for (CPUO_tag, CPUO_conf) in CPUO.items():
                    execute_bm(PASSES, BM_tag, BM_conf,"_CPUO"+CPUO_tag, JAVA20_CPUO, JAVA_LOG + CPUO_conf, MyCallback_RENAISSANCE, " -jar " + CLASSPATH_RENAISSANCE, RES_FOLDER)
        elif BM ==  "Spec":    
            for (BM_tag, BM_conf) in BM_specjbb2015.items():
                execute_bm(PASSES, BM_tag, BM_conf,"", JAVA20, JAVA_LOG, " ", " -jar " + CLASSPATH_SPEC, RES_FOLDER)
                for (CPUO_tag, CPUO_conf) in CPUO.items():
                    execute_bm(PASSES, BM_tag, BM_conf,"_CPUO" + CPUO_tag, JAVA20_CPUO, JAVA_LOG + CPUO_conf, " ", " -jar " + CLASSPATH_SPEC, RES_FOLDER)

if __name__ == "__main__": main(sys.argv[1:])
