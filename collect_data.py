import subprocess
import os
import pathlib
from os.path import isfile, join
from os import listdir
import platform
from timeit import default_timer as timer
import sys, getopt

#Path variables
CLASSPATH_jRAPL=""
CLASSPATH_jRAPL_java13=""
CLASSPATH_jRAPL_java15=""
CLASSPATH_DACAPO=""
CLASSPATH_DACAPO_NEW_java16=""
CLASSPATH_DACAPO_NEW_java16_likwid=""
CLASSPATH_DACAPO_NEW_java15=""
CLASSPATH_DACAPO_NEW_java13=""
CLASSPATH_DACAPO_NEW_java13_likwid=""
CLASSPATH_RENAISSANCE=""
MyCallback_RENAISSANCE=""
MyCallback_RENAISSANCE_likwid=""
CLASSPATH_HAZELCAST_java16=""
CLASSPATH_HAZELCAST_java13=""
CLASSPATH_likwid=""
CONFIG_SPEC=""
CLASSPATH_SPEC_java16=""
CLASSPATH_SPEC_java16_likwid=""
CLASSPATH_SPEC_java13_likwid=""
CLASSPATH_SPEC_java13=""
JAVA13 = ""
JAVA16_HOT = ""

file = open('path_file.txt', 'r')
for line in file:
    variable = line.split("=")[0]
    if "CLASSPATH_jRAPL_java13" in variable:    
        CLASSPATH_jRAPL_java13=line.split("=")[1].split("\"")[1]
        continue
    if "CLASSPATH_jRAPL_java15" in variable:    
        CLASSPATH_jRAPL_java15=line.split("=")[1].split("\"")[1]
        continue
    if "CLASSPATH_jRAPL" in variable:
        CLASSPATH_jRAPL=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_likwid" in variable:    
        CLASSPATH_likwid=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_DACAPO_NEW_java16_likwid" in variable:
        CLASSPATH_DACAPO_NEW_java16_likwid=line.split("=")[1].split("\"")[1]
        continue
    if "CLASSPATH_DACAPO_NEW_java16" in variable:
        CLASSPATH_DACAPO_NEW_java16=line.split("=")[1].split("\"")[1]
        continue
    if "CLASSPATH_DACAPO_NEW_java15" in variable:    
        CLASSPATH_DACAPO_NEW_java15=line.split("=")[1].split("\"")[1]
        continue
    if "CLASSPATH_DACAPO_NEW_java13_likwid" in variable:
        CLASSPATH_DACAPO_NEW_java13_likwid=line.split("=")[1].split("\"")[1]
        continue
    if "CLASSPATH_DACAPO_NEW_java13" in variable:   
        CLASSPATH_DACAPO_NEW_java13=line.split("=")[1].split("\"")[1]
        continue
    if "CLASSPATH_DACAPO" in variable:    
        CLASSPATH_DACAPO=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_RENAISSANCE" in variable:    
        CLASSPATH_RENAISSANCE=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_HAZELCAST_java16" in variable:    
        CLASSPATH_HAZELCAST_java16=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_HAZELCAST_java13" in variable:    
        CLASSPATH_HAZELCAST_java13=line.split("=")[1].split("\"")[1]
    if "MyCallback_RENAISSANCE_likwid" in variable:
        MyCallback_RENAISSANCE_likwid=line.split("=")[1].split("\"")[1]
        continue
    if "MyCallback_RENAISSANCE" in variable:
        MyCallback_RENAISSANCE=line.split("=")[1].split("\"")[1]
    if "CONFIG_SPEC" in variable:
        CONFIG_SPEC=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_SPEC_java16_likwid" in variable:
        CLASSPATH_SPEC_java16_likwid=line.split("=")[1].split("\"")[1]
        continue
    if "CLASSPATH_SPEC_java16" in variable:
        CLASSPATH_SPEC_java16=line.split("=")[1].split("\"")[1]
    if "CLASSPATH_SPEC_java13_likwid" in variable:
        CLASSPATH_SPEC_java13_likwid=line.split("=")[1].split("\"")[1]
        continue
    if "CLASSPATH_SPEC_java13" in variable:
        CLASSPATH_SPEC_java13=line.split("=")[1].split("\"")[1]
    if "JAVA16_HOT" in variable:
        JAVA16_HOT=line.split("=")[1].split("\"")[1]
    if "JAVA13" in variable:
        JAVA13=line.split("=")[1].split("\"")[1]

FLAGS_HAZELCAST="--add-modules java.se --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.nio=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED"

#Java versions
JAVA16 = "java "
JAVA16_HOT = "/scratch/jdk-16/bin/java "
JAVA15M1 = "/scratch/mshimche/Project/openjdk-m1/build/linux-x86_64-server-release/images/jdk/bin/java "
JAVA13 = "/scratch/jdk-13/bin/java "
JAVA_LOG = " -Xlog:gc* -XX:+DisableExplicitGC"

#Specify here which bm+java you want to run
Which_BM = {
        #"DaCapo21_j16", 
        #"DaCapo21_j15M1", 
        #"DaCapo21_j13",
        #"DaCapo_j16", 
        #"DaCapo_j15M1", 
        #"DaCapo_j13", 
        "HazelCast_j16",
        #"HazelCast_j15M1",
        "HazelCast_j13",
        #"Renaissance_j13",
        #"Renaissance_j16",
        #"Renaissance_j15M1",
        #"specjbb2015_j16"
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

GROUPS_LIKWID = { 
    #"BRANCH",
    #"CYCLE_STALLS",
    #"DATA",
    #"ENERGY",
    "ICACHE",
    #"L2CACHE",
    #"L3CACHE",
    "MEM_DP",
    #"NUMA",
    #"TLB_DATA",
}

#Specify GCs for each java version
GC13 = { 
    "j13CMS": "-XX:+UseConcMarkSweepGC",
    "j13Ser": "-XX:+UseSerialGC",
    "j13P": "-XX:+UseParallelGC",
}

GC16 = {
        'j16Z': '-XX:+UseZGC -XX:+UseNUMA' ,#TODO: Use the NUMA parameter only for NUMA
    'j16Ser': '-XX:+UseSerialGC',
    'j16P': '-XX:+UseParallelGC',
    'j16G1': '-XX:+UseG1GC -XX:+UseNUMA',
    'j16Shen': "-XX:+UseShenandoahGC -XX:+UseNUMA",
}


NUM_THREADS= {
	 'n1' : '-XX:ParallelGCThreads=1',
	 'n2' : '-XX:ParallelGCThreads=2',
	 'n4' : '-XX:ParallelGCThreads=4',
         'ndef': ' '
}

#Specify bms
BM_DaCapo = {
      "h2_small_t4":             	" h2 -size small -n 50 -t 4 -c ",#50
      "h2_large_t4":             	" h2 -size large -n 30 -t 4 -c ",#30
      #"h2_huge_t4":              	" h2 -size huge -n 10 -t 4 -c ",
      #"tradesoap_huge_n25":     	"-cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness tradebeans -size huge -n 1 -t 4 -c " concurrency bug -- skip
      #"tradebeans_huge_t4":      	"-cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness tradebeans -size huge -n 25 -t 4 -c ",
      "avrora_large":            	" avrora -size large -n 17 -c ",
      "fop_default":             	" fop -n 50 -c ",
      "jython_large":            	" jython -size large -n 20 -c ",
      "luindex_default":         	" luindex -n 30 -c ",
      "lusearch_large":          	" lusearch -size large -n 20 -c ",
      "pmd_large":               	" pmd -size large -n 30 -c ",
      "sunflow_large":           	" sunflow -size large -n 20 -c ",
      "xalan_large":             	" xalan -size large -n 20 -c "

}
BM_Hazelcast = {
      #"hazelcast_40_60":             	" org.example.StreamingRound3 [40k, 60k]",
      #"hazelcast_20_40":             	" org.example.StreamingRound3 [20k, 40k]",
      "hazelcast":             	" org.example.StreamingRound3 [10k, 20k, 40k ... 100k]",
      #"hazelcast_60_80":             	" org.example.StreamingRound3 [60k, 80k]"
      }
BM_Hazelcast_likwid = {
      "hazelcast":             	" org.example.StreamingRound3_likwid [10k, 20k, 40k ... 100k]",
      "hazelcast_20_40":             	" org.example.StreamingRound3_likwid [20k, 40k]",
      "hazelcast_40_60":             	" org.example.StreamingRound3_likwid [40k, 60k]",
      "hazelcast_60_80":             	" org.example.StreamingRound3_likwid [60k, 80k]",
      }
BM_specjbb2015 = {
      "specjbb15":             	" -m COMPOSITE -ikv -p "
      }
BM_DaCapo2021 = {
      "zxing_def":                  	" zxing -n 25 -c ",
      #"tradesoap_small":             	" tradesoap -size small -n 15 -c ",#only young
      #"tradesoap_large":             	" tradesoap -size large -n 15 -c ",#only young
      #"tradesoap_huge":             	" tradesoap -size huge -n 15 -c ",#only young
      #"tradesoap_def":             	" tradesoap -n 15 -c ",#only young generation
      #"tomcat_small":             	" tomcat -size small",#fails with validation
      #"tomcat_large":             	" tomcat -size large",#fails with validation
      #"tomcat_def":             	" tomcat",#fails with validations
      #"kafka_def":             	" kafka",#broken, does not run
      #"graphchi_large":             	" graphchi -size large",#big data needed
      #"graphchi_huge":             	" graphchi -size huge",#big data needed
      "graphchi_def":             	" graphchi -n 25 -c ",#is it latency oriented?
      #"jme_def":             	        " jme -n 25 -c ",#For some reason there is System.gc calls inside of this bm
      #"h2o_def":             	        " h2o",#latest java 11 supported
      "biojava_def":                   " biojava -n 25 -c ",#only young
      #"h2_small":             	        " h2 -size small -t 4",
      #"h2_large":             	        " h2 -size large -t 4",
      #"h2_huge":                       " h2 -size huge -t 4",
      #"h2_def":             	        " h2 -t 4",
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
      #"mnemonics":              "mnemonics --plugin ",
      #"par-mnemonics":          "par-mnemonics --plugin ",
      #"scrabble":               "scrabble --plugin ",
      #"dotty":                  "dotty --plugin ",#scala
      #"philosophers":           "philosophers --plugin ",
      #"scala-doku":             "scala-doku --plugin ",
      #"scala-kmeans":           "scala-kmeans --plugin ",
      #"scala-stm-bench7":       "scala-stm-bench7 --plugin ",
      #"finagle-chirper":        "finagle-chirper --plugin ",#web
      #"finagle-http":           "finagle-http --plugin ",
      "future-genetic":         "future-genetic --plugin ",#functional
      #"db-shootout":            "db-shootout --plugin ",#database java version <= 11
      #"neo4j-analytics":        "neo4j-analytics --plugin ", #java version <=15 supported only
      #"rx-scrabble":            "rx-scrabble --plugin ",#no GC at all
      }
#The maximum heap size for each application is set to 3X of its respective minimum heap size 
HEAP_SIZES = {
        "h2_small_t4": "300m",#100min
        "h2_large_t4": "1200m",#400min 
        "h2_huge_t4": "2000m", 
        "avrora_large": "45m",#15min
        "fop_default": "135m",#45min 
        "jython_large": "135m",#45min 
        "luindex_default": "21m",#7min 
        "lusearch_large": "40m", #7min
        "pmd_large": "150m", 
        "sunflow_large": "60m", 
        "xalan_large": "35m", 
        "jme_def": "10m",
        "zxing_def": "20m",
        "tradesoap_small": "21m",
        "tradesoap_large": "27m", 
        "tradesoap_huge": "27m", 
        "tradesoap_def": "27m", 
        "graphchi_def": "700m", 
        "biojava_def": "525m", 
        "hazelcast": "5000m", 
        "hazelcast_60_80": "5000m", 
        "hazelcast_40_60": "5000m", 
        "hazelcast_20_40": "5000m", 
        "specjbb15": "32000m", 
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
        #"db-shootout":            "20m",#database java version <= 11
        #"neo4j-analytics":        "20m", #java version <=15 supported only
        "future-genetic":         "30m",#functional 10min
        "mnemonics":              "180m",#60min
        "par-mnemonics":          "180m",#60min
        #"rx-scrabble":            "35m",#no GC invoke at all
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
        if (HS_tag == BM_tag):
            start_HS = int(''.join(filter(str.isdigit, HS_conf)))
    space = int(start_HS * 0.5) #10% bigger heap size
    for i in range (0, HEAP_RUNS):
        conf = param_max + str(start_HS + space*i) + start_Value + param_min + str(start_HS+ space*i) + start_Value
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
def execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC, JAVA, JAVA_LOG, Callback, CLASSPATH, COMMAND, RES_FOLDER):
    #print("Benchmarking " + BM_tag)
    GROUP_tag = ""
    if "likwid" in COMMAND:
        binary_set_number_of_threads = " ".join("export OMP_NUM_THREADS=32")
        GROUP_tag = COMMAND.split(" ")[5]
    for i in range(0, PASSES):
        for (GC_tag, GC_conf) in GC.items():
                HS = heap_size_array(BM_tag, HEAP_RUNS)
                print(HS)
                result_path = ""
                if (GC_conf == '-XX:+UseParallelGC'):
                    for (THR_tag, THR_conf) in NUM_THREADS.items():
                        for (HS_tag, HS_conf) in HS.items():
                            start = timer()
                            result_path = os.path.join(os.getcwd(), RES_FOLDER, BM_tag, GC_tag + HS_tag, THR_tag, GROUP_tag)
                            os.system("sudo mkdir -p " + result_path)
                            os.system("sudo chmod 777 " + result_path)
                            binary_cache_flush = " ".join("./cache-flush")
                            print(binary_cache_flush)
                            binary_hot = " ".join([COMMAND, JAVA, JAVA_LOG, HS_conf, GC_conf, THR_conf, CLASSPATH, BM_conf, Callback])
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
                else:
                    for (HS_tag, HS_conf) in HS.items():
                        start = timer()
                        result_path = os.path.join(os.getcwd(), RES_FOLDER, BM_tag, GC_tag + HS_tag, GROUP_tag)
                        os.system("sudo mkdir -p " + result_path)
                        os.system("sudo chmod 777 " + result_path)
                        binary_cache_flush = " ".join("./cache-flush")
                        print(binary_cache_flush)
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
        if "likwid" not in BM:
            if NUMA == 0:
                COMMAND = "sudo numactl --cpunodebind=0 --membind=0 "
                RES_FOLDER = "results"
            else: 
                COMMAND = "sudo "
                RES_FOLDER = "results_NUMA"
            if BM == "DaCapo_j16": 
                for (BM_tag, BM_conf) in BM_DaCapo.items():
                    #find_heap_size(BM_tag, BM_conf, JAVA16_HOT, "MyCallback", " -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness")
                    #find_2xdrop(BM_tag, BM_conf, JAVA16_HOT, "MyCallback", " -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness")
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, JAVA_LOG, "MyCallback", "-XX:+DisableExplicitGC -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness", COMMAND, RES_FOLDER)
            elif BM == "DaCapo_j13":
                for (BM_tag, BM_conf) in BM_DaCapo.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, JAVA_LOG, "MyCallback_java13", "-XX:+DisableExplicitGC -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness", COMMAND, RES_FOLDER)
            elif BM == "DaCapo_j15M1":
                for (BM_tag, BM_conf) in BM_DaCapo.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC15M1, JAVA15M1, JAVA_LOG, "MyCallback_java15", "-XX:+DisableExplicitGC -cp " + CLASSPATH_jRAPL_java15 + ":" + CLASSPATH_DACAPO + " Harness", COMMAND, RES_FOLDER)
            elif BM == "DaCapo21_j16":
                for (BM_tag, BM_conf) in BM_DaCapo2021.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, JAVA_LOG, "MyCallback", " -jar " + CLASSPATH_DACAPO_NEW_java16, COMMAND, RES_FOLDER)
            elif BM == "DaCapo21_j15M1":
                for (BM_tag, BM_conf) in BM_DaCapo2021.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC15M1, JAVA15M1, JAVA_LOG, "MyCallback_java15", " -jar " + CLASSPATH_DACAPO_NEW_java15, COMMAND, RES_FOLDER)
            elif BM == "DaCapo21_j13":
                for (BM_tag, BM_conf) in BM_DaCapo2021.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, JAVA_LOG, "MyCallback_java13", " -jar " + CLASSPATH_DACAPO_NEW_java13, COMMAND, RES_FOLDER)
            elif BM ==  "HazelCast_j16":    
                for (BM_tag, BM_conf) in BM_Hazelcast.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, JAVA_LOG, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST_java16, COMMAND, RES_FOLDER)
            elif BM ==  "HazelCast_j15M1":    
                for (BM_tag, BM_conf) in BM_Hazelcast.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC15M1, JAVA15M1, "", "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST, COMMAND, RES_FOLDER)
            elif BM ==  "HazelCast_j13":    
                for (BM_tag, BM_conf) in BM_Hazelcast.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, JAVA_LOG, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST_java13, COMMAND, RES_FOLDER)
            elif BM ==  "Renaissance_j13":    
                for (BM_tag, BM_conf) in BM_Renaissance.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, JAVA_LOG, MyCallback_RENAISSANCE, " -jar " + CLASSPATH_RENAISSANCE, COMMAND, RES_FOLDER)
            elif BM ==  "Renaissance_j16":    
                for (BM_tag, BM_conf) in BM_Renaissance.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, JAVA_LOG, MyCallback_RENAISSANCE_likwid, " -jar " + CLASSPATH_RENAISSANCE, COMMAND, RES_FOLDER)
            elif BM ==  "Renaissance_j15M1":
                for (BM_tag, BM_conf) in BM_Renaissance.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC15M1, JAVA15M1, JAVA_LOG, MyCallback_RENAISSANCE, " -jar " + CLASSPATH_RENAISSANCE, COMMAND, RES_FOLDER)
            elif BM ==  "specjbb2015_j13":    
                for (BM_tag, BM_conf) in BM_specjbb2015.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, JAVA_LOG, CONFIG_SPEC, " -jar " + CLASSPATH_SPEC_java13, COMMAND, RES_FOLDER)
            elif BM ==  "specjbb2015_j16":    
                for (BM_tag, BM_conf) in BM_specjbb2015.items():
                    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, JAVA_LOG, CONFIG_SPEC, " -jar " + CLASSPATH_SPEC_java16, COMMAND, RES_FOLDER)
        if "likwid" in BM:
            for group in GROUPS_LIKWID:
                JAVA_LOG_likwid = "-DLIKWID_PERFMON " + JAVA_LOG
                if NUMA == 0:
                    COMMAND = "sudo /usr/local/bin/likwid-perfctr -C 0-7,16-23 -g " + group +" -m "
                    RES_FOLDER = "results_likwid"
                else: 
                    COMMAND = "sudo /usr/local/bin/likwid-perfctr -C 0-31 -g " + group +" -m "
                    RES_FOLDER = "results_likwid_NUMA"
                if BM == "DaCapo_j16_likwid": 
                    for (BM_tag, BM_conf) in BM_DaCapo.items():
                        execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, JAVA_LOG_likwid, "MyCallback_likwid", " -cp " + CLASSPATH_likwid + ":" + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness", COMMAND, RES_FOLDER)
                elif BM == "DaCapo_j13_likwid": 
                    for (BM_tag, BM_conf) in BM_DaCapo.items():
                        execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, JAVA_LOG_likwid, "MyCallback_java13_likwid", " -cp " + CLASSPATH_likwid + ":" + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness", COMMAND, RES_FOLDER)
                elif BM == "DaCapo21_j16_likwid": 
                    for (BM_tag, BM_conf) in BM_DaCapo2021.items():
                        execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, JAVA_LOG_likwid, "MyCallback_likwid", " -jar " + CLASSPATH_DACAPO_NEW_java16_likwid, COMMAND, RES_FOLDER)
                elif BM == "DaCapo21_j13_likwid": 
                    for (BM_tag, BM_conf) in BM_DaCapo2021.items():
                        execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, JAVA_LOG_likwid, "MyCallback_java13_likwid", " -jar " + CLASSPATH_DACAPO_NEW_java13_likwid, COMMAND, RES_FOLDER)
                elif BM == "HazelCast_j16_likwid": 
                    for (BM_tag, BM_conf) in BM_Hazelcast_likwid.items():
                        execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, " -DLIKWID_PERFMON ", "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST_java16 + ":" + CLASSPATH_likwid, COMMAND, RES_FOLDER)
                elif BM == "HazelCast_j13_likwid": 
                    for (BM_tag, BM_conf) in BM_Hazelcast_likwid.items():
                        execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, " -DLIKWID_PERFMON ", "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST_java13 + ":" + CLASSPATH_likwid, COMMAND, RES_FOLDER)
                elif BM == "Renaissance_j13_likwid": 
                    for (BM_tag, BM_conf) in BM_Renaissance.items():
                        execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, JAVA_LOG_likwid, MyCallback_RENAISSANCE_likwid, " -jar " + CLASSPATH_RENAISSANCE, COMMAND, RES_FOLDER)
                elif BM == "Renaissance_j16_likwid": 
                    for (BM_tag, BM_conf) in BM_Renaissance.items():
                        execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, JAVA_LOG_likwid, MyCallback_RENAISSANCE_likwid, " -jar " + CLASSPATH_RENAISSANCE, COMMAND, RES_FOLDER)
                elif BM ==  "specjbb2015_j13_likwid":    
                    for (BM_tag, BM_conf) in BM_specjbb2015.items():
                        execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, JAVA_LOG_likwid, CONFIG_SPEC, " -jar " + CLASSPATH_SPEC_java13_likwid, COMMAND, RES_FOLDER)
                elif BM ==  "specjbb2015_j16_likwid":    
                    for (BM_tag, BM_conf) in BM_specjbb2015.items():
                        execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, JAVA_LOG_likwid, CONFIG_SPEC, " -jar " + CLASSPATH_SPEC_java16_likwid, COMMAND, RES_FOLDER)

if __name__ == "__main__": main(sys.argv[1:])
