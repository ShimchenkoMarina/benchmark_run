# How to run, in 3 steps <br />
1. python3 collect_data.py <br />
2. bash analyze_results.sh <br />
3. python3.7 analyze.py <br />
#Where to look for output <br />
1. output >> results <br />
2. output >> raw_dir <br />
3. output >> prosessed_results <br />
#Change paths to java and Dacapo_jar, jRAPL <br />
open collect_data.py <br />
first 30 lines <br />
#How many times the same benchmark runs <br />
open collect_data.py <br />
change parameter PASSES <br />
#Different Garbage Colectors (GC) in collect_data.py <br />
Uncomment the ones you want in the GC*  
#Benchmarks in collect_data.py <br />
Uncomment the ones you want in the BM* <br />



