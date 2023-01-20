# How to run, in 3 steps <br />
1. sudo python3 collect_data.py <br />
2. sudo bash analyze_results.sh <br />
3. python3 gather_data_into_csv.py <br />
4. cd EnergyVsTimePlots <br />
5. python3 Clustering.py  - builds heatmaps and puts together all_data_energy and all_data_perf<br /> 
<br />
#All the pathes are in a separate file: path_file.txt <br />
<br />
#How many times the same benchmark runs <br />
There are 2 parameters, that needed to be spesified when running collect_data.py <br />
-r - how many times to repeat each experiment <br />
-s - how many heap sizes to test<br />


