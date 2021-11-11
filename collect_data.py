import subprocess
import os
import pathlib
from os.path import isfile, join
from os import listdir
import platform
from timeit import default_timer as timer
import sys, getopt

#Parameters for running
#PASSES = 1 
#HEAP_RUNS = 1

#Path variables
CLASSPATH_jRAPL="/scratch/Project/jRAPL"
CLASSPATH_jRAPL_java13="/scratch/Project/jRAPL_13"
CLASSPATH_jRAPL_java15="/scratch/Project/jRAPL_15"
CLASSPATH_DACAPO="/scratch/Project/Dacapo_jar:/scratch/Project/Dacapo_jar/harness:/scratch/Project/Dacapo_jar/dacapo-9.12-MR1-bach.jar"
CLASSPATH_DACAPO_NEW_java16="/scratch/Project/DaCapo2021_java16.jar"
CLASSPATH_DACAPO_NEW_java15="/scratch/Project/DaCapo2021_java15.jar"
CLASSPATH_DACAPO_NEW_java13="/scratch/Project/DaCapo2021_java13.jar"
CLASSPATH_RENAISSANCE="/scratch/Project/renaissance/target/renaissance-gpl-0.13.0-5-g76e6065.jar"
MyCallback_RENAISSANCE="/scratch/Project/renaissance/plugins/energy-utils/target/plugin-energyutils-assembly-0.0.2.jar"
CLASSPATH_HAZELCAST="/scratch/Project/jet-gc-benchmark/target/hazelcast-jet-4.2.jar:/scratch/Project/jet-gc-benchmark/target/jet-gc-benchmark-1.0-SNAPSHOT-jar-with-dependencies.jar:/scratch/Project/jRAPL_jar/build/Energy.jar:/scratch/Project/jet-gc-benchmark/target/classes/"
FLAGS_HAZELCAST="--add-modules java.se --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.nio=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED"

#Java versions
JAVA16 = "java "
JAVA16_HOT = "/scratch/jdk-16/bin/java "
JAVA15M1 = "/scratch/Project/openjdk-m1/build/linux-x86_64-server-release/images/jdk/bin/java "
JAVA13 = "/scratch/jdk-13/bin/java "
JAVA_LOG = " -Xlog:gc* "

#Specify here which bm+java you want to run
Which_BM = {
        #"DaCapo21_j16", 
        #"DaCapo21_j15M1", 
        #"DaCapo21_j13",
        "DaCapo_j16", 
        #"DaCapo_j15M1", 
        #"DaCapo_j13", 
        #"HazelCast_j16",
        #"HazelCast_j15M1",
        #"HazelCast_j13",
        #"Renaissance_j13",
        "Renaissance_j16",
        #"Renaissance_j15M1",
} 

#Specify GCs for each java version
GC13 = { "j13CMS": "-XX:+UseConcMarkSweepGC",
	 "j13Ser": "-XX:+UseSerialGC",
	 "j13P": "-XX:+UseParallelGC",
}

GCHCast16 = { 
	 'j16Z': '-XX:+UseZGC' ,
         'j16Shen': "-XX:+UseShenandoahGC",
	 'j16G1': '-XX:+UseG1GC',
}

GC15M1 = { 
	 'j15Z': '-XX:+UseZGC' 
}

GCHCast13 = { 
        "j13CMS": "-XX:+UseConcMarkSweepGC",
	"j13Z": "-XX:+UnlockExperimentalVMOptions -XX:+UseZGC" ,
}

GC16 = { 'j16Ser': '-XX:+UseSerialGC',
	 'j16P': '-XX:+UseParallelGC',
	 'j16G1': '-XX:+UseG1GC',
	 'j16Z': '-XX:+UseZGC' ,
         'j16Shen': "-XX:+UseShenandoahGC",
}

NUM_THREADS= {
	 'n1' : '-XX:ParallelGCThreads=1',
	 'n2' : '-XX:ParallelGCThreads=2',
	 'n4' : '-XX:ParallelGCThreads=4',
         'ndef': ' '
}

#Specify bms
BM_DaCapo = {
      #"h2_small_t4":             	" h2 -size small -n 50 -t 4 -c ",#50
      #"h2_large_t4":             	" h2 -size large -n 30 -t 4 -c ",#30
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
      "hazelcast":             	" org.example.StreamingRound3 [10k, 20k, 40k ... 100k]"
      #"hazelcast":             	" " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST + " org.example.StreamingRound3 [10k, 20k, 40k ... 100k]"
      }
BM_DaCapo2021 = {
      #"zxing_def":                  	" zxing -n 25 -c ",
      "tradesoap_small":             	" tradesoap -size small -n 15 -c ",#only young
      "tradesoap_large":             	" tradesoap -size large -n 15 -c ",#only young
      "tradesoap_huge":             	" tradesoap -size huge -n 15 -c ",#only young
      "tradesoap_def":             	" tradesoap -n 15 -c ",#only young generation
      #"tomcat_small":             	" tomcat -size small",#fails with validation
      #"tomcat_large":             	" tomcat -size large",#fails with validation
      #"tomcat_def":             	" tomcat",#fails with validations
      #"kafka_def":             	" kafka",#broken, does not run
      #"graphchi_large":             	" graphchi -size large",#big data needed
      #"graphchi_huge":             	" graphchi -size huge",#big data needed
      "graphchi_def":             	" graphchi -n 25 -c ",#is it latency oriented?
      "jme_def":             	        " jme -n 25 -c ",#For some reason there is System.gc calls inside of this bm
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
      "naive-bayes":            "naive-bayes --plugin ",
      "page-rank":              "page-rank --plugin ",
      "akka-uct":               "akka-uct --plugin ",#concurrency
      "fj-kmeans":              "fj-kmeans --plugin ",
      "reactors":               "reactors --plugin ",
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
	"h2_small_t4": "300m",#100min
	"h2_large_t4": "1200m",#400min 
	"h2_huge_t4": "2g", 
	"avrora_large": "45m",#15min
	"fop_default": "135m",#45min 
	"jython_large": "135m",#45min 
	"luindex_default": "21m",#7min 
	"lusearch_large": "21m", #7min
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
	"hazelcast": "5g", 
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

#We need to decide which space between heap sizes we want. In theory we want to have 
#twice less GC cycles with the next heap size. 
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
            if ("m" not in HS_conf):
                 start_Value = "g"
    if (start_HS < 100 and start_Value == "m"):
        space = 25
    if (start_HS > 100 and start_Value == "m"):
        space = 100
    if (start_Value == "g"):
        space = 1
    for i in range (0, HEAP_RUNS):
        conf = param_max + str(start_HS + space*i) + start_Value + param_min + str(start_HS+ space*i) + start_Value
        tag = str(start_HS + space*i) + start_Value
        HS[tag] = conf
    #print(HS)
    return HS

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
        if (start_Value == "g"):
            space = 1
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
            
        

def execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC, JAVA, JAVA_LOG, Callback, CLASSPATH):
    #print("Benchmarking " + BM_tag)
    for i in range(0, PASSES):
        for (GC_tag, GC_conf) in GC.items():
            #print(GC[GC_tag])
                HS = heap_size_array(BM_tag, HEAP_RUNS)
                
                if (GC_conf == '-XX:+UseParallelGC'):
                    for (THR_tag, THR_conf) in NUM_THREADS.items():
                        for (HS_tag, HS_conf) in HS.items():
                            start = timer()
                            result_path = os.path.join(os.getcwd(), "results", BM_tag, GC_tag + HS_tag, THR_tag)
                            os.system("sudo mkdir -p " + result_path)
                            os.system("sudo chmod 777 " + result_path)
                            binary_hot = " ".join(["sudo numactl --cpunodebind=0 --membind=0", JAVA, JAVA_LOG, HS_conf, GC_conf, THR_conf, CLASSPATH, BM_conf, Callback])
                            print(binary_hot)
                            collect_data(binary_hot, result_path)
                            end = timer()
                            minutes = round((end - start) / 60.0, 3)
                else:
                    for (HS_tag, HS_conf) in HS.items():
                        start = timer()
                        result_path = os.path.join(os.getcwd(), "results", BM_tag, GC_tag + HS_tag)
                        os.system("sudo mkdir -p " + result_path)
                        os.system("sudo chmod 777 " + result_path)
                        binary_hot = " ".join(["sudo numactl --cpunodebind=0 --membind=0 ", JAVA, JAVA_LOG, HS_conf, GC_conf, CLASSPATH, BM_conf, Callback])
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
      opts, args = getopt.getopt(argv,"hr:s:",["runs=","sizes="])
    except getopt.GetoptError:
      print('collect_data.py -r <number_of_runs> -s <how_many_heap_sizes_to_run>')
      sys.exit(2)
    for opt, arg in opts:
        print(opt)
        print(arg)
        if opt == '-h':
            print('collect_data.py -r <number_of_runs> -s <how_many_heap_sizes_to_test>')
            sys.exit()
        elif opt in ("-r", "--runs"):
            PASSES = int(arg)
            
        elif opt in ("-s", "--sizes"):
            HEAP_RUNS = int(arg)
    print("Starting to collect data with " + str(PASSES) + " passes")
    for BM in Which_BM:
        print(BM)
        if BM == "DaCapo_j16": 
            for (BM_tag, BM_conf) in BM_DaCapo.items():
                find_heap_size(BM_tag, BM_conf, JAVA16_HOT, "MyCallback", " -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness")
                #execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, JAVA_LOG, "MyCallback", "-XX:+DisableExplicitGC -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness")
        elif BM == "DaCapo_j13":
            for (BM_tag, BM_conf) in BM_DaCapo.items():
                execute_bm(iPASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, JAVA_LOG, "MyCallback_java13", " -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness")
        elif BM == "DaCapo_j15M1":
            for (BM_tag, BM_conf) in BM_DaCapo.items():
                #find_heap_size(BM_tag, BM_conf, JAVA15M1, "MyCallback_java15", " -cp " + CLASSPATH_jRAPL_java15 + ":" + CLASSPATH_DACAPO + " Harness")
                execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC15M1, JAVA15M1, JAVA_LOG, "MyCallback_java15", " -cp " + CLASSPATH_jRAPL_java15 + ":" + CLASSPATH_DACAPO + " Harness")
        elif BM == "DaCapo21_j16":
            for (BM_tag, BM_conf) in BM_DaCapo2021.items():
                execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, JAVA_LOG, "MyCallback", " -jar " + CLASSPATH_DACAPO_NEW_java16)
        elif BM == "DaCapo21_j15M1":
            for (BM_tag, BM_conf) in BM_DaCapo2021.items():
                execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC15M1, JAVA15M1, JAVA_LOG, "MyCallback_java15", " -jar " + CLASSPATH_DACAPO_NEW_java15)
        elif BM == "DaCapo21_j13":
            for (BM_tag, BM_conf) in BM_DaCapo2021.items():
                execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, JAVA_LOG, "MyCallback_java13", " -jar " + CLASSPATH_DACAPO_NEW_java13)
        elif BM ==  "HazelCast_j16":    
            for (BM_tag, BM_conf) in BM_Hazelcast.items():
                execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GCHCast16, JAVA16_HOT, "", "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST)
        elif BM ==  "HazelCast_j15M1":    
            for (BM_tag, BM_conf) in BM_Hazelcast.items():
                find_heap_size(BM_tag, BM_conf, JAVA15M1, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST)
                #execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC15M1, JAVA15M1, "", "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST)
        elif BM ==  "HazelCast_j13":    
            for (BM_tag, BM_conf) in BM_Hazelcast.items():
                execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GCHCast13, JAVA13, "", "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST)
        elif BM ==  "Renaissance_j13":    
            for (BM_tag, BM_conf) in BM_Renaissance.items():
                execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC13, JAVA13, JAVA_LOG, MyCallback_RENAISSANCE, " -jar " + CLASSPATH_RENAISSANCE)
        elif BM ==  "Renaissance_j16":    
            for (BM_tag, BM_conf) in BM_Renaissance.items():
                find_heap_size(BM_tag, BM_conf, JAVA16_HOT, MyCallback_RENAISSANCE, " -jar " + CLASSPATH_RENAISSANCE)
            #    execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC16, JAVA16_HOT, JAVA_LOG, MyCallback_RENAISSANCE, " -jar " + CLASSPATH_RENAISSANCE)
        elif BM ==  "Renaissance_j15M1":    
            for (BM_tag, BM_conf) in BM_Renaissance.items():
                #find_heap_size(BM_tag, BM_conf, JAVA15M1, MyCallback_RENAISSANCE, " -jar " + CLASSPATH_RENAISSANCE)
                execute_bm(PASSES, HEAP_RUNS, BM_tag, BM_conf, GC15M1, JAVA15M1, JAVA_LOG, MyCallback_RENAISSANCE, " -jar " + CLASSPATH_RENAISSANCE)

if __name__ == "__main__": main(sys.argv[1:])
