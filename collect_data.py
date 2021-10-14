import subprocess
import os
import pathlib
from os.path import isfile, join
from os import listdir
import platform
from timeit import default_timer as timer

#Parameters for running
PASSES = 1 
HEAP_RUNS = 1

#Path variables
CLASSPATH_jRAPL="/scratch/Project/jRAPL"
CLASSPATH_jRAPL_java13="/scratch/Project/jRAPL_13"
CLASSPATH_DACAPO="/scratch/Project/Dacapo_jar:/scratch/Project/Dacapo_jar/harness:/scratch/Project/Dacapo_jar/dacapo-9.12-MR1-bach.jar"
CLASSPATH_DACAPO_NEW="/scratch/Project/dacapo-evaluation-git+309e1fa.jar"
CLASSPATH_HAZELCAST="/scratch/Project/jet-gc-benchmark/target/hazelcast-jet-4.2.jar:/scratch/Project/jet-gc-benchmark/target/jet-gc-benchmark-1.0-SNAPSHOT-jar-with-dependencies.jar:/scratch/Project/jRAPL_jar/build/Energy.jar:/scratch/Project/jet-gc-benchmark/target/classes/"
FLAGS_HAZELCAST="--add-modules java.se --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.nio=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED"

#Java versions
JAVA16 = "java -Xlog:gc "
JAVA16_HOT = "/scratch/jdk-16/bin/java -Xlog:gc* "
JAVA15M1 = "/scratch/Project/openjdk-m1/build/linux-x86_64-server-release/images/jdk/bin/java -Xlog:gc* "
JAVA13 = "/scratch/jdk-13/bin/java -Xlog:gc "

#Specify here which bm+java you want to run
Which_BM = {
        #"DaCapo_j16", 
        #"DaCapo_j15M1", 
        #"DaCapo_j13", 
        #"DaCapo21_j16", 
        #"DaCapo21_j15M1", 
        #"DaCapo21_j13",
        #"HazelCast_j16",
        #"HazelCast_j15M1",
        "HazelCast_j13",
} 

#Specify GCs for each java version
GC13 = { "j13CMS": "-XX:+UseConcMarkSweepGC",
	 #"j13Ser": "-XX:+UseSerialGC",
	 #"j13P": "-XX:+UseParallelGC",
}

GCHCast16 = { 
	 'j16Z': '-XX:+UseZGC' ,
         #'j16Shen': "-XX:+UseShenandoahGC",
	 #'j16G1': '-XX:+UseG1GC',
}

GC15M1 = { 
	 'j16Z': '-XX:+UseZGC' 
}

GCHCast13 = { 
        "j13CMS": "-XX:+UseConcMarkSweepGC",
	#"j13Z": "-XX:+UnlockExperimentalVMOptions -XX:+UseZGC" ,
}

GC16 = { #'j16Ser': '-XX:+UseSerialGC',
	 #'j16P': '-XX:+UseParallelGC',
	 'j16G1': '-XX:+UseG1GC',
	 #'j16Z': '-XX:+UseZGC' ,
         #'j16Shen': "-XX:+UseShenandoahGC",
}

NUM_THREADS= {
	 'n1' : '-XX:ParallelGCThreads=1',
	 'n2' : '-XX:ParallelGCThreads=2',
	 'n4' : '-XX:ParallelGCThreads=4'
}

#Specify bms
BM_DaCapo = {
      #"EnergyCheckUtils":              	EnergyCheckUtils,
      #"h2_small_t4":             	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness h2 -size small -n 50 -t 4 -c MyCallback",
      #"h2_large_t4":             	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness h2 -size large -n 30 -t 4 -c MyCallback",
      #"h2_huge_t4":              	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness h2 -size huge -n 10 -t 4 -c MyCallback",
      #"tradesoap_huge_n25":     	"-cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness tradebeans -size huge -n 1 -t 4 -c MyCallback" concurrency bug -- skip
      #"tradebeans_huge_t4":      	"-cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness tradebeans -size huge -n 25 -t 4 -c MyCallback",
      "avrora_large":            	" avrora -size large -n 1 -c ",#17
      #"fop_default":             	" fop -n 1 -c ",#50
      #"jython_large":            	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness jython -size large -n 20 -c MyCallback",
      #"luindex_default":         	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness luindex -n 30 -c MyCallback",
      #"lusearch_large":          	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness lusearch -size large -n 20 -c MyCallback",
      #"pmd_large":               	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness pmd -size large -n 30 -c MyCallback",
      #"sunflow_large":           	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness sunflow -size large -n 20 -c MyCallback",
      #"xalan_large":             	" -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness xalan -size large -n 20 -c MyCallback"

}
BM_Hazelcast = {
      "hazelcast":             	" org.example.StreamingRound3 [10k, 20k, 40k ... 100k]"
      #"hazelcast":             	" " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST + " org.example.StreamingRound3 [10k, 20k, 40k ... 100k]"
      }
BM_DaCapo2021 = {
      #"zxing_def":             	" -jar " + CLASSPATH_DACAPO_NEW + " zxing",
      #"tradesoap_small":             	" -jar " + CLASSPATH_DACAPO_NEW + " tradesoap -size small",#only young
      #"tradesoap_large":             	" -jar " + CLASSPATH_DACAPO_NEW + " tradesoap -size large",#only young
      #"tradesoap_huge":             	" -jar " + CLASSPATH_DACAPO_NEW + " tradesoap -size huge",#only young
      #"tradesoap_def":             	" -jar " + CLASSPATH_DACAPO_NEW + " tradesoap",#only young generation
      #"tomcat_small":             	" -jar " + CLASSPATH_DACAPO_NEW + " tomcat -size small",#fails with validation
      #"tomcat_large":             	" -jar " + CLASSPATH_DACAPO_NEW + " tomcat -size large",#fails with validation
      #"tomcat_def":             	" -jar " + CLASSPATH_DACAPO_NEW + " tomcat",#fails with validations
      #"kafka_def":             	" -jar " + CLASSPATH_DACAPO_NEW + " kafka",#broken, does not run
      #"graphchi_large":             	" -jar " + CLASSPATH_DACAPO_NEW + " graphchi -size large",#big data needed
      #"graphchi_huge":             	" -jar " + CLASSPATH_DACAPO_NEW + " graphchi -size huge",#big data needed
      #"graphchi_def":             	" -jar " + CLASSPATH_DACAPO_NEW + " graphchi",#is it latency oriented?
      "jme_def":             	" jme",#For some reason there is System.gc calls inside of this bm
      #"h2o_def":             	" -jar " + CLASSPATH_DACAPO_NEW + " h2o",#latest java 11 supported
      #"biojava_def":             	" -jar " + CLASSPATH_DACAPO_NEW + " biojava",#only young
      #"h2_small":             	" -jar " + CLASSPATH_DACAPO_NEW + " h2 -size small -t 4",
      #"h2_large":             	" -jar " + CLASSPATH_DACAPO_NEW + " h2 -size large -t 4",
      #"h2_huge":             	" -jar " + CLASSPATH_DACAPO_NEW + " h2 -size huge -t 4",
      #"h2_def":             	" -jar " + CLASSPATH_DACAPO_NEW + " h2 -t 4",
      }

BM_DaCapo_java13 = {
      #"EnergyCheckUtils":              	EnergyCheckUtils,
      #"h2_large_t4":             	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness h2 -size large -n 30 -t 4 -c MyCallback_java13",
      #"avrora_large":            	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness avrora -size large -n 17 -c MyCallback_java13",
      #"h2_small_t4":             	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness h2 -size small -n 50 -t 4 -c MyCallback_java13",
      #"h2_huge_t4":              	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness h2 -size huge -n 8 -t 4 -c MyCallback_java13",
      #"tradesoap_huge_n25":     	"-cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness tradebeans -size huge -n 1 -t 4 -c MyCallback" concurrency bug -- skip
      #"tradebeans_huge_t4":      	"-cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness tradebeans -size huge -n 25 -t 4 -c MyCallback",
      #"fop_default":             	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness fop -n 1 -c MyCallback_java13",#50
      #"jython_large":            	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness jython -size large -n 20 -c MyCallback_java13",
      #"luindex_default":         	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness luindex -n 30 -c MyCallback_java13",
      #"lusearch_large":          	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness lusearch -size large -n 20 -c MyCallback_java13",
      #"pmd_large":               	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness pmd -size large -n 30 -c MyCallback_java13",
      #"sunflow_large":           	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness sunflow -size large -n 20 -c MyCallback_java13",
      #"xalan_large":             	" -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness xalan -size large -n 20 -c MyCallback_java13" 
}

#The maximum heap size for each application is set to 3X of its respective minimum heap size 
HEAP_SIZES = {
	"h2_small_t4": "210m",
	"h2_large_t4": "750m", 
	"h2_huge_t4": "2g", 
	"avrora_large": "27m",
	"fop_default": "75m", 
	"jython_large": "75m", 
	"luindex_default": "21m", 
	"lusearch_large": "21m", 
	"pmd_large": "150m", 
	"sunflow_large": "60m", 
	"xalan_large": "35m", 
	"jme_def": "10m",
	"zxing_def": "10m",
	"tradesoap_small": "21m",
	"tradesoap_large": "27m", 
	"tradesoap_huge": "27m", 
	"tradesoap_def": "27m", 
	"graphchi_def": "700m", 
	"biojava_def": "525m", 
	"hazelcast": "4g" 
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

#We need to decide which space between heap sizes we want. In theory we want to have 
#twice less GC cycles with the next heap size. 
def heap_size_array(BM_tag):
    start_HS = 1
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

def execute_bm(BM_tag, BM_conf, GC, JAVA, Callback, CLASSPATH):
    #print("Benchmarking " + BM_tag)
    for i in range(0, PASSES):
        for (GC_tag, GC_conf) in GC.items():
            #print(GC[GC_tag])
            if (GC_conf == '-XX:+UseParallelGC'):
                for (THR_tag, THR_conf) in NUM_THREADS.items():
                    HS = heap_size_array(BM_tag)
                    for (HS_tag, HS_conf) in HS.items():
                        start = timer()
                        result_path = os.path.join(os.getcwd(), "results", BM_tag, GC_tag + HS_tag, THR_tag)
                        os.system("sudo mkdir -p " + result_path)
                        os.system("sudo chmod 777 " + result_path)
                        binary_hot = " ".join(["sudo numactl --cpunodebind=0 --membind=0", JAVA, HS_conf, GC_conf, THR_conf, CLASSPATH, BM_conf, Callback])
                        print(binary_hot)
                        collect_data(binary_hot, result_path)
                        end = timer()
                        minutes = round((end - start) / 60.0, 3)
                        #print("Pass " + str(i) + " took " + str(minutes) + " minutes")
            else: 
                HS = heap_size_array(BM_tag)
                for (HS_tag, HS_conf) in HS.items():
                    start = timer()
                    result_path = os.path.join(os.getcwd(), "results_t", BM_tag, GC_tag + HS_tag)
                    os.system("sudo mkdir -p " + result_path)
                    os.system("sudo chmod 777 " + result_path)
                    binary_hot = " ".join(["sudo numactl --cpunodebind=0 --membind=0 ", JAVA, HS_conf, GC_conf, CLASSPATH, BM_conf, Callback])
                    print(binary_hot)
                    collect_data(binary_hot, result_path)
                    end = timer()
                    minutes = round((end - start) / 60.0, 3)
                    #print("Pass " + str(i) + " took " + str(minutes) + " minutes")        


def main():
    print("Starting to collect data with " + str(PASSES) + " passes")
    for BM in Which_BM:
        print(BM)
        if BM == "DaCapo_j16": 
            for (BM_tag, BM_conf) in BM_DaCapo.items():
                execute_bm(BM_tag, BM_conf, GC16, JAVA16_HOT, "MyCallback", "-XX:+DisableExplicitGC -cp " + CLASSPATH_jRAPL + ":" + CLASSPATH_DACAPO + " Harness")
        elif BM == "DaCapo_j13":
            for (BM_tag, BM_conf) in BM_DaCapo.items():
                execute_bm(BM_tag, BM_conf, GC13, JAVA13, "MyCallback_java13", " -cp " + CLASSPATH_jRAPL_java13 + ":" + CLASSPATH_DACAPO + " Harness")
        elif BM == "DaCapo_j15M1":
            for (BM_tag, BM_conf) in BM_DaCapo.items():
                print("DC java15")
        elif BM == "DaCapo21_j16":
            for (BM_tag, BM_conf) in BM_DaCapo2021.items():
                execute_bm(BM_tag, BM_conf, GC16, JAVA16_HOT, "", " -jar " + CLASSPATH_DACAPO_NEW)
        elif BM == "DaCapo21_j15M1":
            for (BM_tag, BM_conf) in BM_DaCapo2021.items():
                execute_bm(BM_tag, BM_conf, GC15M1, JAVA15M1, "", " -jar " + CLASSPATH_DACAPO_NEW)
        elif BM == "DaCapo21_j13":
            for (BM_tag, BM_conf) in BM_DaCapo2021.items():
                execute_bm(BM_tag, BM_conf, GC13, JAVA13, "", " -jar " + CLASSPATH_DACAPO_NEW)
        elif BM ==  "HazelCast_j16":    
            for (BM_tag, BM_conf) in BM_Hazelcast.items():
                execute_bm(BM_tag, BM_conf, GCHCast16, JAVA16_HOT, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST)
        elif BM ==  "HazelCast_j15M1":    
            for (BM_tag, BM_conf) in BM_Hazelcast.items():
                execute_bm(BM_tag, BM_conf, GC15M1, JAVA15M1, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST)
        elif BM ==  "HazelCast_j13":    
            for (BM_tag, BM_conf) in BM_Hazelcast.items():
                execute_bm(BM_tag, BM_conf, GCHCast13, JAVA13, "", " " + FLAGS_HAZELCAST + " -cp " + CLASSPATH_HAZELCAST)

if __name__ == "__main__": main()
