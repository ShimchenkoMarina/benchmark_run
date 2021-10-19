# How to run, in 3 steps <br />
1. python3 collect_data.py <br />
2. bash analyze_results.sh <br />
3. python3.7 analyze.py <br />
4. python3 gather_data_into_csv.py <br />
5. cd EnergyVsTimePlots <br />
6. python3 Example.py <br />
#Where to look for output <br />
1. >> results <br />
2. >> raw_dir <br />
3. >> prosessed_results <br />
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



