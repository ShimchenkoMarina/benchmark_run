#New project - heap sizes
# How to run, in 3 steps <br />
1. sudo python3 collect_data.py <br />
2. sudo bash analyze_results.sh <br />
 <br />
 <br />
3. python3 gather_data_into_csv.py <br />
7. cd EnergyVsTimePlots <br />
8. python3.8 Clustering.py  - builds heatmaps and puts together all_data_energy and all_data_perf<br /> 
<br />

#Where to look for output <br />
1. >> results <br />
2. >> raw_dir <br />
3. >> prosessed_results <br />

#All the pathes are in a separate file: pathes.txt <br />
#How many times the same benchmark runs <br />
There are 3 parameters, that needed to be spesified when running collect_data.py
-r - how many times to repeat each experiment

#Benchmarks in collect_data.py <br />
Uncomment the ones you want in the BM* <br />



