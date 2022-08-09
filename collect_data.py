#Olof's project collect data
import subprocess
from subprocess import Popen
import os
import pathlib
from os.path import isfile, join
from os import listdir
import platform
from timeit import default_timer as timer
import sys, getopt

#Path variables
CONFIG_SPEC=""
CLASSPATH_SPEC=""
JAVA20 = ""
JAVA20_OLOF = ""
JAVA20_GEN=""

file = open('../benchmark_run/path_file.txt', 'r')
for line in file:
    variable = line.split("=")[0]
    if "CONFIG_SPEC" in variable:
        CONFIG_SPEC=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_SPEC" in variable:
        CLASSPATH_SPEC=line.split("=")[1].split("\"")[1]
        continue
    if "JAVA20"==variable:
        JAVA20=line.split("=")[1].split("\"")[1]
    if "JAVA20_OLOF"==variable:
        JAVA20_OLOF=line.split("=")[1].split("\"")[1]
    if "JAVA20_GEN"==variable:
        JAVA20_GEN=line.split("=")[1].split("\"")[1]

FLAGS_HAZELCAST="--add-modules java.se --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.nio=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED"

#Java log
JAVA_LOG = " -Xlog:gc* -XX:+DisableExplicitGC"

#Specify here which bm+java you want to run
Which_BM = {
        #"DaCapo21_j16",
        #"DaCapo21_j15M1",
        #"DaCapo21_j13",
        #"DaCapo_j16",
        #"DaCapo_j15M1",
        #"DaCapo_j13",
        #"HazelCast_j16",
        #"HazelCast_j15M1",
        #"HazelCast_j13",
        #"Renaissance_j13",
        #"Renaissance_j16",
        #"Renaissance_j15M1",
        "specjbb2015_j20",
        "specjbb2015_j20_olof",
        "specjbb2015_j20_gen_clean",
        #"specjbb2015_j13"
        #"specjbb2015_j15M1"
        #"DaCapo21_j16_likwid",
        #"DaCapo21_j15M1_likwid",
        #"DaCapo21_j13_likwid",
        #"DaCapo_j16_likwid",
        #"DaCapo_j15M1_likwid",
        #"DaCapo_j13_likwid",
        #"HazelCast_j16_likwid",
        #"HazelCast_j15M1_likwid",
        #"HazelCast_j13_likwid",
        #"Renaissance_j13_likwid",
        #"Renaissance_j16_likwid",
        #"Renaissance_j15M1_likwid",
        #"specjbb2015_j16_likwid"
        #"specjbb2015_j13_likwid"
        #"specjbb2015_j15M1_likwid"
}

#Specify GCs for each java version
GC = {
    'Z': '-XX:+UseZGC' ,
}


#Specify bms
BM_Hazelcast = {
      "hazelcast":             	" org.example.StreamingRound3 [10k, 20k, 40k ... 100k]"
      }
BM_specjbb2015 = {
      #"specjbb15":             	" -m COMPOSITE -ikv -p "
      "specjbb15":             	" -m COMPOSITE"
      }
BM_specjbb2015_j20_gen = {
      "specjbb15":             	" -m COMPOSITE"
      }
BM_specjbb2015_j20_olof = {
      "specjbb15":             	" -m COMPOSITE"
      }
BM_Renaissance = {
      #"als":             	"als --plugin ",#apache-spark
      #"chi-square":      	"chi-square --plugin ",
      #"dec-tree":               "dec-tree --plugin ",
      #"gauss-mix":              "gauss-mix --plugin ",
      #"log-regression":         "log-regression --plugin ",
      #"movie-lens":             "movie-lens --plugin ",
      #"naive-bayes":            "naive-bayes --plugin ",
      #"page-rank":              "page-rank --plugin ",
      #"akka-uct":               "akka-uct --plugin ",#concurrency
      #"fj-kmeans":              "fj-kmeans --plugin ",
      #"reactors":               "reactors --plugin ",
      #"db-shootout":            "db-shootout --plugin ",#database java version <= 11
      #"neo4j-analytics":        "neo4j-analytics --plugin ", #java version <=15 supported only
      #"future-genetic":         "future-genetic --plugin ",#functional
      #"mnemonics":              "mnemonics --plugin ",
      #"par-mnemonics":          "par-mnemonics --plugin ",
      #"rx-scrabble":            "rx-scrabble --plugin ",
      #"scrabble":               "scrabble --plugin ",
      #"dotty":                  "dotty --plugin ",#scala
      #"philosophers":           "philosophers --plugin ",
      #"scala-doku":             "scala-doku --plugin ",
      #"scala-kmeans":           "scala-kmeans --plugin ",
      #"scala-stm-bench7":       "scala-stm-bench7 --plugin ",
      #"finagle-chirper":        "finagle-chirper --plugin ",#web
      #"finagle-http":           "finagle-http --plugin ",
}
#The maximum heap size for each application is set to 3X of its respective minimum heap size
HEAP_SIZES = {
        "hazelcast": "5000m",
        "specjbb15": "16000m",
        "als":             	"1455m",#apache-spark485min
        "chi-square":      	"1455m",#485min
        "dec-tree":               "1455m",#485min
        "gauss-mix":              "1455m",#485min
        "log-regression":         "1455m",#485min
        "movie-lens":             "1455m",#485min
        "naive-bayes":            "3825m",#1275min(1600m1)
        "page-rank":              "1875m",#625min(835m1)
        "akka-uct":               "705m",#concurrency235min
        "fj-kmeans":              "285m",#95min(150m1)
        "reactors":               "1500m",#500 min(900m1)
        "future-genetic":         "30m",#functional 10min
        "mnemonics":              "180m",#60min
        "par-mnemonics":          "180m",#60min
        "scrabble":               "330m",#110min
        "dotty":                  "180m",#scala 60min
        "philosophers":           "30m",#10min
        "scala-doku":             "105m",#35min
        "scala-kmeans":           "105m",#35min
        "scala-stm-bench7":       "930m",#310min
        "finagle-chirper":        "180m",#web 60m min
        "finagle-http":           "105m",#35min
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
    for i in range (0, HEAP_RUNS):
        if "spec" not in BM_tag:
            conf = param_max + str(start_HS + space*i) + start_Value + param_min + str(start_HS+ space*i) + start_Value
        else:
            if i >=3:
                space = inst(start_HS)
            conf = param_max + str(start_HS + space*i) + start_Value
        tag = str(1 + i*0.5)
        HS[tag] = conf
    return HS

def find_2xdrop(BM_tag, BM_conf, JAVA, Callback, CLASSPATH):
    start_HS = 5
    start_Value = "m"
    param_max = "-Xmx"
    param_min = " -Xms"
    space = 0
    found = False
    i = 0
    HS = {}
    for (HS_tag, HS_conf) in HEAP_SIZES.items():
        #print (HS_conf)
        if (HS_tag == BM_tag):
            start_HS = int(''.join(filter(str.isdigit, HS_conf)))
    space = int(start_HS * 0.1) #10% bigger heap size
    GC_cycles_cur = 0
    GC_cycles_start = 0
    GC_cycles = 0
    while not found:
        HS_conf = param_max + str(start_HS + space*i) + start_Value + param_min + str(start_HS+ space*i) + start_Value
        print(HS_conf)
        HS_tag = str(start_HS + space*i) + start_Value
        result_path = os.path.join(os.getcwd(), "find_2xdrop", BM_tag, HS_tag)
        os.system("sudo mkdir -p " + result_path)
        os.system("sudo chmod 777 " + result_path)
        binary = " ".join([JAVA, JAVA_LOG,  HS_conf, '-XX:+UseSerialGC' , CLASSPATH, BM_conf, Callback])
        print(binary)
        collect_data(binary, result_path)
        f_path = os.path.join(result_path, get_current_result_name(result_path))
        not_break = True
        with open(f_path, 'r') as reader:
            for line in reader.readlines():
                if "GC(" in line:
                    GC_cycles = int(line.split("(")[1].split(")")[0])
        if GC_cycles_start == 0:
            GC_cycles_start = GC_cycles
        else:
            GC_cycles_cur = GC_cycles
        if GC_cycles_start != 0 and GC_cycles_cur != 0 and GC_cycles_start/GC_cycles_cur > 2:
            found = True
            with open("./find_2xdrop/heap_size_report.txt", 'a') as writer:
                writer.write("For " + BM_tag + " use " + str(i) + "\n")
        i = i + 1

def find_heap_size(BM_tag, BM_conf, JAVA, Callback, CLASSPATH):
    start_HS = 5
    start_Value = "m"
    param_max = "-Xmx"
    param_min = " -Xms"
    space = 0
    found = False
    i = 0
    while not found:
        HS_conf = param_max + str(start_HS + space*i) + start_Value + param_min + str(start_HS+ space*i) + start_Value
        HS_tag = str(start_HS + space*i) + start_Value
        if (start_HS < 100 and start_Value == "m"):
            space = 10
        if (start_HS > 99 and start_Value == "m"):
            space = 25
        if (start_HS > 999 and start_Value == "m"):
            space = 150
        result_path = os.path.join(os.getcwd(), "find_heap_size", BM_tag, HS_tag)
        os.system("sudo mkdir -p " + result_path)
        os.system("sudo chmod 777 " + result_path)
        binary = " ".join(["sudo numactl --cpunodebind=0 --membind=0 ",  JAVA,  HS_conf, '-XX:+UseSerialGC' , CLASSPATH, BM_conf, Callback])
        print(binary)
        collect_data(binary, result_path)
        f_path = os.path.join(result_path, get_current_result_name(result_path))
        not_break = True
        with open(f_path, 'r') as reader:
            for line in reader.readlines():
                if "The following benchmarks failed:" in line or "java.lang.OutOfMemoryError" in line:
                    i = i + 1
                    not_break = False
                    break
        if not_break:
            found = True
            with open("./find_heap_size/heap_size_report.txt", 'a') as writer:
                writer.write("For " + BM_tag + " use " + HS_tag + "\n")
            #to_results = os.path.join(os.getcwd(), "results", BM_tag)
            #binary = " ".join(["sudo numactl --cpunodebind=0 --membind=0 ",  JAVA, JAVA_LOG,  HS_conf, '-XX:+UseSerialGC' , CLASSPATH, BM_conf, Callback])
            #collect_data(binary, to_results)
            #print(binary)


#TODO: add GROUP_TAG into the path when run for features collecting.
def execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC, GC_pid_tag, JAVA_tag, JAVA, JAVA_LOG, Callback, CLASSPATH, COMMAND, RES_FOLDER):
    #print("Benchmarking " + BM_tag)
    for (GC_tag, GC_conf) in GC.items():
        HS = heap_size_array(BM_tag, HEAP_RUNS)
        for (HS_tag, HS_conf) in HS.items():
            for i in range(0, PASSES):
                start = timer()
                result_path = os.path.join(os.getcwd(), RES_FOLDER, BM_tag, JAVA_tag + GC_tag + HS_tag)
                os.system("sudo mkdir -p " + result_path)
                os.system("sudo chmod 777 " + result_path)
                binary_hot = " ".join([COMMAND, JAVA, JAVA_LOG, HS_conf, GC_conf, CLASSPATH, BM_conf, Callback])
                print(binary_hot)
                collect_data(binary_hot, result_path)
                end = timer()
                minutes = round((end - start) / 60.0, 3)
                if "hazelcast" in BM_tag:
                    f1_path = os.path.join(result_path, get_current_result_name(result_path))
                    f2_path = os.path.join(os.getcwd(), "histo-latency/0")
                    # opening first file in append mode and second file in read mode
                    f1 = open(f1_path, 'a+')
                    f2 = open(f2_path, 'r')
                    # appending the contents of the second file to the first file
                    f1.write(f2.read())
                    os.system("sudo rm -rf " + f2_path)
            os.system("mkdir  ../benchmark_run/results_pids/" + BM_tag +"/")
            os.system("mkdir  ../benchmark_run/results_pids/" + BM_tag +"/"+ JAVA_tag + GC_tag + HS_tag + "/")
            os.system("mv ../benchmark_run/scheduler.txt ../benchmark_run/results_pids/" + BM_tag +"/"+ JAVA_tag + GC_tag + HS_tag + "/")
            os.system("mv ../benchmark_run/GC_pids" + GC_pid_tag + ".txt ../benchmark_run/results_pids/" + BM_tag + "/" + JAVA_tag + GC_tag + HS_tag + "/GC_pids.txt")

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
        COMMAND = "sudo ./../rapl-tools/AppPowerMeter "
        RES_FOLDER = "../benchmark_run/results"
        if BM ==  "HazelCast_j15M1":
                for (BM_tag, BM_conf) in BM_Hazelcast.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC15M1, JAVA15M1, "", "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST, COMMAND, RES_FOLDER)
        elif BM ==  "HazelCast_j13":
                for (BM_tag, BM_conf) in BM_Hazelcast.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, "", "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST_java13, COMMAND, RES_FOLDER)
        elif BM ==  "Renaissance_j13":
                for (BM_tag, BM_conf) in BM_Renaissance.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, JAVA_LOG, MyCallback_RENAISSANCE, " -jar " + CLASSPATH_RENAISSANCE, COMMAND, RES_FOLDER)
        elif BM ==  "Renaissance_j16":
                for (BM_tag, BM_conf) in BM_Renaissance.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, JAVA_LOG, MyCallback_RENAISSANCE_likwid, " -jar " + CLASSPATH_RENAISSANCE, COMMAND, RES_FOLDER)
        elif BM ==  "Renaissance_j15M1":
                for (BM_tag, BM_conf) in BM_Renaissance.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC15M1, JAVA15M1, JAVA_LOG, MyCallback_RENAISSANCE, " -jar " + CLASSPATH_RENAISSANCE, COMMAND, RES_FOLDER)
        elif BM ==  "specjbb2015_j20_gen_clean":
            #print(JAVA20_GEN)
            JAVA_tag = "j20G"
            GC_pid_tag = "_java20_gen_clean"
            os.system("rm -rf ../benchmark_run/GC_pids_java20_gen_clean.txt")
            for (BM_tag, BM_conf) in BM_specjbb2015_j20_gen.items():
                execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC, GC_pid_tag, JAVA_tag, JAVA20_GEN, JAVA_LOG, CONFIG_SPEC, " -jar " + CLASSPATH_SPEC, COMMAND, RES_FOLDER)
        elif BM ==  "specjbb2015_j20_olof":
            #print(JAVA20_OLOF)
            GC_pid_tag = "_java20_olof"
            JAVA_tag = "j20YinYan"
            os.system("rm -rf ../benchmark_run/GC_pids_java20_olof.txt")
            for (BM_tag, BM_conf) in BM_specjbb2015_j20_olof.items():
                execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC, GC_pid_tag, JAVA_tag, JAVA20_OLOF, JAVA_LOG, CONFIG_SPEC, " -jar " + CLASSPATH_SPEC, COMMAND, RES_FOLDER)
        elif BM ==  "specjbb2015_j20":
            GC_pid_tag = ""
            #print(JAVA20)
            JAVA_tag = "j20"
            os.system("rm -rf ../benchmark_run/GC_pids.txt")
            for (BM_tag, BM_conf) in BM_specjbb2015.items():
                execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC, GC_pid_tag,  JAVA_tag, JAVA20, JAVA_LOG, CONFIG_SPEC, " -jar " + CLASSPATH_SPEC, COMMAND, RES_FOLDER)
if __name__ == "__main__": main(sys.argv[1:])

