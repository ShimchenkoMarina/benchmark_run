# How to run, in 3 steps
1. python3 collect_data.py
2. bash analyze_results.sh
3. python3.7 analyze.py
#Where to look for output
1. output >> results
2. output >> raw_dir
3. output >> prosessed_results
#Change paths to java and Dacapo_jar, jRAPL
open collect_data.py
first 30 lines
#How many times the same benchmark runs
open collect_data.py
line 9
#Different Garbage Colectors (GC) in collect_data.py
Uncomment the ones you want in the GC13 and GC16
#Benchmarks in collect_data.py
Uncomment the ones you want in the BM13 and BM16



