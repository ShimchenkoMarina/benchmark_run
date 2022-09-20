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
CLASSPATH_RN=""
CLASSPATH_DACAPO=""
CLASSPATH_HAZELCAST=""
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
    if "JAVA20_GEN"==variable:
        JAVA20_GEN=line.split("=")[1].split("\"")[1]

FLAGS_HAZELCAST="--add-modules java.se --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.nio=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED"

#Java log
JAVA_LOG = " -Xlog:gc* "
JAVA_LOG_ALLOCATION_RATE = "-Xlog:gc+stats"
#Specify here which bm+java you want to run
Which_BM = {
            #"DaCapo_j20_olof",
            #"DaCapo_j20_gen_clean",
            #"HazelCast_j20_olof",
            #"HazelCast_j20_gen_clean",
            #"HazelCast_j20_olof_static",
            #"HazelCast_j20_gen_clean_static",
            #"Renaissance_j20_gen_clean_static",
            #"Renaissance_j20_olof_static",
            #"Renaissance_j15M1",
            #"specjbb2015_j20_olof",
            #"specjbb2015_j20_gen_clean",
            #"specjbb2015_j20_olof_static",
            #"specjbb2015_j20_gen_clean_static",
            #"specjbb2015_j20_olof_static_allocation_rate",
            #"specjbb2015_j20_gen_clean_static_allocation_rate",
            "HazelCast_j20_olof_static_allocation_rate",
            "HazelCast_j20_gen_clean_static_allocation_rate",
            "Renaissance_j20_gen_clean_static_allocation_rate",
            "Renaissance_j20_olof_static_allocation_rate",
}

#Specify GCs for each java version
GC = {
    'Z': '-XX:+UseZGC' ,
}
#Specify bms
BM_DaCapo = {
          #"h2_small_t4":                " h2 -size small -n 50 -t 4 -c ",#50
          #"h2_large_t4":                " h2 -size large -n 30 -t 4 -c ",#30
          #"h2_huge_t4":                " h2 -size huge -n 10 -t 4 -c ",
          #"tradesoap_huge_n25":        "-cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness tradebeans -size huge -n 1 -t 4 -c " concurrency bug -- skip
          #"tradebeans_huge_t4":        "-cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness tradebeans -size huge -n 25 -t 4 -c ",
          "avrora_large":               " avrora -size large -n 17 -t 1",
          "fop_default":                " fop -n 50 ",
          #"jython_large":               " jython -size large -n 20 -c ",
          "luindex_default":            " luindex -n 30 ",
          #"lusearch_large":            " lusearch -size large -n 20 -c ",
          "pmd_large":                  " pmd -size large -n 30 ",
          ##"sunflow_large":              " sunflow -size large -n 20 ",
          ##"xalan_large":                " xalan -size large -n 20 "


}

#Specify bms
BM_Hazelcast = {
      "hazelcast_100":             	" org.example.StreamingRound2 [20k, 40k, 60k, 80k, 100k]",
      "hazelcast_75":             	" org.example.StreamingRound2 [20k, 40k, 60k, 80k]",
      "hazelcast_50":             	" org.example.StreamingRound2 [20k, 40k, 60k]",
      "hazelcast_25":             	" org.example.StreamingRound2 [20k, 40k]",
      }
#BM_specjbb2015 = {
      #"specjbb15":             	" -m COMPOSITE -ikv -p "
      #"specjbb15_100":             	" -m COMPOSITE",#IR=21000
      #"specjbb15_75":             	" -m COMPOSITE",#IR=15750
      #"specjbb15_50":             	" -m COMPOSITE",#IR=10500
      #"specjbb15_25":             	" -m COMPOSITE",#IR=5250
#      }
BM_specjbb2015 = {
      "specjbb15_100":             	" -m COMPOSITE",
      #"specjbb15_75":             	" -m COMPOSITE",
      #"specjbb15_50":             	" -m COMPOSITE",
      #"specjbb15_25":             	" -m COMPOSITE",
      }
#BM_specjbb2015_j20_olof = {
      #"specjbb15_100":             	" -m COMPOSITE",
      #"specjbb15_75":             	" -m COMPOSITE",
      #"specjbb15_50":             	" -m COMPOSITE",
      #"specjbb15_25":             	" -m COMPOSITE",
      #}
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
      "finagle-chirper":        "finagle-chirper ",#web
      "finagle-http":           "finagle-http",
}
#The maximum heap size for each application is set to 3X of its respective minimum heap size
HEAP_SIZES = {
        "hazelcast": "1200m",#1200
        "specjbb15": "16000m",#16000
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
        "finagle-chirper":        "200m",#web 60m min
        "finagle-http":           "70m",#35min
        "avrora_large": "25m",#15min-45
        "fop_default": "55m",#45min-135
        "jython_large": "55m",#45min-135
        "luindex_default": "17m",#7min-21
        "lusearch_large": "17m", #7min-40
        "pmd_large": "70m",#150(3x)
        "sunflow_large": "30m",#60(3x)
        "xalan_large": "20m",#35(3x)
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
    if "hazelcast" not in BM_tag:
        space = int(start_HS * 0.5)
    else:
        space = 100
    tag = ""
    for i in range (0, HEAP_RUNS):
        if "spec" not in BM_tag:
            conf = param_max + str(start_HS + space*i) + start_Value + param_min + str(start_HS+ space*i) + start_Value
            if "hazelcast" not in BM_tag:
                tag = str(1 + i*0.5)
            else:
                tag = str(1 + round(i/11, 1))
        else:
            if i >=3:
                space = int(start_HS)
            conf = param_max + str(start_HS + space*i) + start_Value
            tag = str(1.0 + i)
        HS[tag] = conf
    return HS

#TODO: add GROUP_TAG into the path when run for features collecting.
def execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC, GC_pid_tag, JAVA_tag, JAVA, JAVA_LOG, Callback, CLASSPATH, COMMAND, RES_FOLDER):
    #print("Benchmarking " + BM_tag)
    for (GC_tag, GC_conf) in GC.items():
        HS = heap_size_array(BM_tag, HEAP_RUNS)
        for (HS_tag, HS_conf) in HS.items():
            for i in range(0, PASSES):
                #start = timer()
                result_path = os.path.join(os.getcwd(), RES_FOLDER, BM_tag, JAVA_tag + GC_tag + HS_tag)
                os.system("sudo mkdir -p " + result_path)
                os.system("sudo chmod 777 " + result_path)
                os.system("echo "  + BM_tag + " " + JAVA_tag + " >> output.txt")
                binary_hot = " ".join([COMMAND, JAVA, JAVA_LOG, HS_conf, GC_conf, CLASSPATH, BM_conf, Callback])
                print(binary_hot)
                collect_data(binary_hot, result_path)
                os.system("echo 777 >> output.txt")
                #end = timer()
                #minutes = round((end - start) / 60.0, 3)
                #if "hazelcast" in BM_tag:
                #    f1_path = os.path.join(result_path, get_current_result_name(result_path))
                #    f2_path = os.path.join(os.getcwd(), "histo-latency/0")
                #    # opening first file in append mode and second file in read mode
                #    f1 = open(f1_path, 'a+')
                #    f2 = open(f2_path, 'r')
                #    # appending the contents of the second file to the first file
                #    f1.write(f2.read())
                #    os.system("sudo rm -rf " + f2_path)
            #os.system("mkdir  ../benchmark_run/results_pids/" + BM_tag +"/")
            #os.system("mkdir  ../benchmark_run/results_pids/" + BM_tag +"/"+ JAVA_tag + GC_tag + HS_tag + "/")
            #os.system("mv ../benchmark_run/scheduler.txt ../benchmark_run/results_pids/" + BM_tag +"/"+ JAVA_tag + GC_tag + HS_tag + "/")
            #os.system("mv ../benchmark_run/GC_pids" + GC_pid_tag + ".txt ../benchmark_run/results_pids/" + BM_tag + "/" + JAVA_tag + GC_tag + HS_tag + "/GC_pids.txt")

def main(argv):
    PASSES=1
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
        if "_static" not in BM:
            if BM ==  "HazelCast_j20_olof":
                GC_pid_tag = "_java20_olof"
                JAVA_tag = "j20YinYan"
                for (BM_tag, BM_conf) in BM_Hazelcast.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC, GC_pid_tag, JAVA_tag, JAVA20_OLOF, JAVA_LOG, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST, COMMAND, RES_FOLDER)
            elif BM ==  "HazelCast_j20_gen_clean":
                JAVA_tag = "j20G"
                GC_pid_tag = "_java20_gen_clean"
                for (BM_tag, BM_conf) in BM_Hazelcast.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC, GC_pid_tag, JAVA_tag, JAVA20_GEN, JAVA_LOG, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST, COMMAND, RES_FOLDER)
            elif BM == "DaCapo_j20_gen_clean":
                JAVA_tag = "j20G"
                GC_pid_tag = "_java20_gen_clean"
                for (BM_tag, BM_conf) in BM_DaCapo.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC, GC_pid_tag, JAVA_tag, JAVA20_GEN, JAVA_LOG, "", " -jar " + CLASSPATH_DACAPO, COMMAND, RES_FOLDER)
            elif BM == "DaCapo_j20_olof":
                JAVA_tag = "j20YinYan"
                GC_pid_tag = "_java20_olof"
                for (BM_tag, BM_conf) in BM_DaCapo.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC, GC_pid_tag, JAVA_tag, JAVA20_OLOF, JAVA_LOG, "", " -jar " + CLASSPATH_DACAPO, COMMAND, RES_FOLDER)
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
        else:#static
            BM_suffix = "_static"
            GC_pid_tag = ""
            JAVA_tag = ""
            JAVA_local = ""
            if "_java20_olof" in BM:
                GC_pid_tag = "_java20_olof"
                JAVA_tag = "j20YinYan"
                JAVA_local = JAVA20_OLOF
            if "_gen_clean" in BM:
                JAVA_tag = "j20G"
                GC_pid_tag = "_java20_gen_clean"
                JAVA_local = JAVA20_GEN
            if "allocation_rate" not in BM:
                JAVA_LOG_local = JAVA_LOG
            else:
                BM_suffix = BM_suffix + "_allocation_rate"
                JAVA_LOG_local = JAVA_LOG_ALLOCATION_RATE




            if "specjbb2015" in BM:
                #os.system("rm -rf ../benchmark_run/GC_pids_java20_olof.txt")
                for (BM_tag, BM_conf) in BM_specjbb2015.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag + BM_suffix, BM_conf, GC, GC_pid_tag, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads    -XX:ConcGCThreads=10", CONFIG_SPEC, " -jar " + CLASSPATH_SPEC, COMMAND, RES_FOLDER)
            elif "Renaissance" in BM:
                for (BM_tag, BM_conf) in BM_Renaissance.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag + BM_suffix, BM_conf, GC, GC_pid_tag, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads    -XX:ConcGCThreads=8", "", " -jar " + CLASSPATH_RN, COMMAND, RES_FOLDER)
            elif "HazelCast" in BM:
                for (BM_tag, BM_conf) in BM_Hazelcast.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag + BM_suffix, BM_conf, GC, GC_pid_tag, JAVA_tag, JAVA_local, JAVA_LOG_local + " -XX:-UseDynamicNumberOfGCThreads    -XX:ConcGCThreads=8", "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST, COMMAND, RES_FOLDER)


if __name__ == "__main__": main(sys.argv[1:])

