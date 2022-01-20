# How to run, in 3 steps <br />
1. sudo python3 collect_data.py <br />
2. sudo bash analyze_results.sh <br />
3. sudo bash analyze_results_raw_to_processed.sh <br />
4. sudo bash analyze_results_likwid.sh <br />
5. python3.7 analyze.py <br />
6. python3 gather_data_into_csv.py <br />
7. cd EnergyVsTimePlots <br />
8. python3 Clustering.py <br />
#Where to look for output <br />
1. >> results <br />
2. >> raw_dir <br />
3. >> prosessed_results <br />
#All the pathes are in a separate file: pathes.txt <br />
#How many times the same benchmark runs <br />
There are 3 parameters, that needed to be spesified when running collect_data.py
-r - how many times to repeat each experiment
-s - how many heap sizes to test
-n - use NUMA (1) or not (0)
#Different Garbage Colectors (GC) in collect_data.py <br />
Uncomment the ones you want in the GC*  
#Benchmarks in collect_data.py <br />
Uncomment the ones you want in the BM* <br />



