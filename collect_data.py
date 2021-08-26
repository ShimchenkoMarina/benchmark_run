import subprocess
import os
import pathlib
from os.path import isfile, join
from os import listdir
import platform
from timeit import default_timer as timer

PASSES = 5
HEAP_RUNS = 1
MACHINE_NAME = "x86"
COMMIT_ID = "1"
CLASSPATH_jRAPL="/home/marina/workspace/2021NewProject/OpenJDK/jRAPL"
CLASSPATH_jRAPL_java14="/home/marina/workspace/2021NewProject/OpenJDK/jRAPL_java14"
CLASSPATH_jRAPL_java13="/home/marina/workspace/2021NewProject/OpenJDK/jRAPL_java13"
CLASSPATH_DACAPO="/home/marina/workspace/2021NewProject/OpenJDK/Dacapo_jar:/home/marina/workspace/2021NewProject/OpenJDK/Dacapo_jar/harness:~/workspace/2021NewProject/OpenJDK/Dacapo_jar/dacapo-9.12-MR1-bach.jar"
#EnergyCheckUtils="EnergyCheckUtils"
#ENERGY_SRC="/home/marina/workspace/2021NewProject/OpenJDK/jRAPL/EnergyCheckUtils.java"
#PERF_SRC="/home/marina/workspace/2021NewProject/OpenJDK/jRAPL/PerfCheckUtils.java"
DACAPO="/home/marina/workspace/2021NewProject/OpenJDK/Dacapo_jar/dacapo-9.12-MR1-bach.jar"

#M1_MAX_OBJECT_SIZE_EXEC = "/usr/bin/time --verbose /home/jonas/jdk/m1_max_object_size/build/linux-x86_64-server-release/jdk/bin/java -Xms4g -Xmx4g -Xlog:gc"
#GC = { "m1_max_object_size_256kB": "-XX:+UseZGC -XX:+UsePartialEvacuation -XX:+UseLazyRelocate"}
JAVA16 = "java -Xlog:gc "
JAVA16_HOT = "/usr/lib/jvm/adoptopenjdk-16-hotspot-amd64/bin/java -Xlog:gc* "
#JAVA16 = "java "
#JAVAC16 ="javac "
JAVA14 = "/usr/lib/jvm/jdk-14.0.2/bin/java -Xlog:gc "
JAVA13 = "/usr/lib/jvm/jdk-13/bin/java -Xlog:gc "
#JAVA14 = "/usr/lib/jvm/jdk-14.0.2/bin/java "
#JAVAC14="/usr/lib/jvm/jdk-14.0.2/bin/javac "
GC13 = { "j13CMS": "-XX:+UseConcMarkSweepGC",
	 "j13Ser": "-XX:+UseSerialGC",
	 "j13P": "-XX:+UseParallelGC",
}
GC16 = { #'j16Ser': '-XX:+UseSerialGC',
	 #'j16P': '-XX:+UseParallelGC',
	 #'j16G1': '-XX:+UseG1GC',
	 'j16G15l': '-XX:+UseG1GC -XX:MaxGCPauseMillis=5',
	 #'j16Z': '-XX:+UseZGC' ,
	 #'j16ZUnCom': '-XX:+UseZGC -XX:-ZUncommit' ,
         #'j16Shen': "-XX:+UseShenandoahGC"
         #'j16ShenOpps': "-XX:+UseShenandoahGC -XX:+UseCompressedOops"
}

NUM_THREADS= {
	 'n1' : '-XX:ParallelGCThreads=1',
	 'n2' : '-XX:ParallelGCThreads=2',
	 'n4' : '-XX:ParallelGCThreads=4'
}
BM16 = {
      #"EnergyCheckUtils":              	EnergyCheckUtils,
      #"h2_small_t4":             	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness h2 -size small -n 25 -t 4 -c MyCallback",
      #"h2_large_t4":             	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness h2 -size large -n 15 -t 4 -c MyCallback",
      #"h2_huge_t4":              	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness h2 -size huge -n 10 -t 4 -c MyCallback",
      #"tradesoap_huge_n25":     	"-cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness tradebeans -size huge -n 1 -t 4 -c MyCallback" concurrency bug -- skip
      #"tradebeans_huge_t4":      	"-cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness tradebeans -size huge -n 25 -t 4 -c MyCallback",
      #"avrora_large":            	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness avrora -size large -n 7 -c MyCallback",
      #"fop_default":             	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness fop -n 30 -c MyCallback",
      #"jython_large":            	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness jython -size large -n 10 -c MyCallback",
      #"luindex_default":         	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness luindex -n 15 -c MyCallback",
      #"lusearch_large":          	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness lusearch -size large -n 10 -c MyCallback",
      #"pmd_large":               	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness pmd -size large -n 15 -c MyCallback",
      #"sunflow_large":           	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness sunflow -size large -n 10 -c MyCallback",
      #"xalan_large":             	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness xalan -size large -n 10 -c MyCallback"

}
BM13 = {
      #"EnergyCheckUtils":              	EnergyCheckUtils,
      "h2_small_t4":             	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness h2 -size small -n 25 -t 4 -c MyCallback_java13",
      #"h2_large_t4":             	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness h2 -size large -n 15 -t 4 -c MyCallback_java13",
      #"h2_huge_t4":              	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness h2 -size huge -n 8 -t 4 -c MyCallback_java13",
      #"tradesoap_huge_n25":     	"-cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness tradebeans -size huge -n 1 -t 4 -c MyCallback" concurrency bug -- skip
      #"tradebeans_huge_t4":      	"-cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness tradebeans -size huge -n 25 -t 4 -c MyCallback",
      #"avrora_large":            	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness avrora -size large -n 7 -c MyCallback_java13",
      #"fop_default":             	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness fop -n 25 -c MyCallback_java13",
      #"jython_large":            	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness jython -size large -n 10 -c MyCallback_java13",
      #"luindex_default":         	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness luindex -n 15 -c MyCallback_java13",
      #"lusearch_large":          	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness lusearch -size large -n 10 -c MyCallback_java13",
      #"pmd_large":               	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness pmd -size large -n 15 -c MyCallback_java13",
      #"sunflow_large":           	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness sunflow -size large -n 10 -c MyCallback_java13",
      #"xalan_large":             	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness xalan -size large -n 10 -c MyCallback_java13" 
}

HEAP_SIZES = {
	"h2_small_t4": "510m", 
	"h2_large_t4": "1g", 
	"h2_huge_t4": "4g", 
	"avrora_large": "20g", 
	"fop_default": "75m", 
	"jython_large": "75m", 
	"luindex_default": "21m", 
	"lusearch_large": "21m", 
	"pmd_large": "150m", 
	"sunflow_large": "60m", 
	"xalan_large": "35m" 
}

def get_next_result_name(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return str(len(files) + 1) + ".txt"


def collect_data(binary, result_path):
    app = subprocess.Popen(binary, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,shell=True,bufsize=1)
    pathlib.Path(result_path).mkdir(parents=True, exist_ok=True)
    result_file = os.path.join(result_path, get_next_result_name(result_path))
    with open(result_file, "w") as writeFile:
        for line in app.stdout:
            writeFile.write(line)

    writeFile.close()
    return result_file

def heap_size_array(BM_tag):
    start_HS = 1
    start_Value = "m"
    param_max = "-Xmx"
    param_min = " -Xms"
    space = 0 
    HS = {}
    for (HS_tag, HS_conf) in HEAP_SIZES.items():
        print (HS_conf)
        if (HS_tag == BM_tag):
            start_HS = int(''.join(filter(str.isdigit, HS_conf)))
            if ("m" not in HS_conf):
                 start_Value = "g"
    if (start_HS < 100 and start_Value == "m"):
        space = 10
    if (start_HS > 100 and start_Value == "m"):
        space = 50
    if (start_Value == "g"):
        space = 1
    for i in range (0, HEAP_RUNS):
        conf = param_max + str(start_HS + space*i) + start_Value + param_min + str(start_HS+ space*i) + start_Value
        tag = str(start_HS + space*i) + start_Value
        HS[tag] = conf
    print(HS)
    return HS

def main():
    print("Starting to collect data with " + str(PASSES) + " passes")

    for (BM_tag, BM_conf) in BM16.items():
        print("Benchmarking " + BM_tag)
        for i in range(0, PASSES):
            for (GC_tag, GC_conf) in GC16.items():
                print(GC16[GC_tag])
                if (GC_conf == '-XX:+UseParallelGC'):
                    for (THR_tag, THR_conf) in NUM_THREADS.items():
                        HS = heap_size_array(BM_tag)
                        for (HS_tag, HS_conf) in HS.items():
                            start = timer()
                            binary_hot = " ".join(["sudo", JAVA16_HOT, HS_conf, GC_conf, THR_conf, BM_conf])
                            print(binary_hot)
                            result_path_hot = os.path.join(os.getcwd(), "results", BM_tag, GC_tag + HS_tag, THR_tag)
                            collect_data(binary_hot, result_path_hot)
                            end = timer()
                            minutes = round((end - start) / 60.0, 3)
                            print("Pass " + str(i) + " took " + str(minutes) + " minutes")
                else: 
                    HS = heap_size_array(BM_tag)
                    for (HS_tag, HS_conf) in HS.items():
                        start = timer()
                        binary_hot = " ".join(["sudo", JAVA16_HOT, HS_conf, GC_conf, BM_conf])
                        print(binary_hot)
                        result_path_hot = os.path.join(os.getcwd(), "results", BM_tag, GC_tag + HS_tag)
                        collect_data(binary_hot, result_path_hot)
                        end = timer()
                        minutes = round((end - start) / 60.0, 3)
                        print("Pass " + str(i) + " took " + str(minutes) + " minutes")
            
            #binary = " ".join([JAVAC14, PERF_SRC])
            #print(binary)
            #binary = " ".join([JAVAC14, ENERGY_SRC])
            #print(binary)'''
    for (BM_tag, BM_conf) in BM13.items():
        print("Benchmarking " + BM_tag)
        for i in range(0, PASSES):
            for (GC_tag, GC_conf) in GC13.items():
                print(GC_conf)
                if (GC_conf == '-XX:+UseParallelGC'):
                    for (THR_tag, THR_conf) in NUM_THREADS.items():
                        HS = heap_size_array(BM_tag)
                        for (HS_tag, HS_conf) in HS.items():
                            start = timer()
                            binary = " ".join(["sudo", JAVA13, HS_conf, GC_conf, THR_conf, BM_conf])
                            print(binary)
                            result_path = os.path.join(os.getcwd(), "results", BM_tag, GC_tag + HS_tag, THR_tag)
                            collect_data(binary, result_path)
                            end = timer()
                            minutes = round((end - start) / 60.0, 3)
                            print("Pass " + str(i) + " took " + str(minutes) + " minutes")
                else:
                    HS = heap_size_array(BM_tag)
                    for (HS_tag, HS_conf) in HS.items():
                        start = timer()
                        binary = " ".join(["sudo", JAVA13, HS_conf, GC_conf, BM_conf])
                        print(binary)
                        result_path = os.path.join(os.getcwd(), "results", BM_tag, GC_tag+ HS_tag)
                        collect_data(binary, result_path)
                        end = timer()
                        minutes = round((end - start) / 60.0, 3)
                        print("Pass " + str(i) + " took " + str(minutes) + " minutes")

if __name__ == "__main__":
    main()
