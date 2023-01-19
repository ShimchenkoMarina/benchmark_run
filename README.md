How to run, in 3 steps <br />
1. sudo python3 collect_data.py <br />
2. sudo bash analyze_results.sh <br />
3. python3 gather_data_into_csv.py <br />

Build plots <br />
4. cd EnergyVsTimePlots <br />
5. python3.8 Clustering.py  - builds heatmaps <br /> 
<br />

Where to look for output <br />
1. results <br />
2. raw_dir <br />
3. prosessed_results <br />

All the pathes are in a separate file:  <br />
pathes.txt <br />

How many times the same benchmark runs <br />
There -r parameter controls how many JVM invokation one has for a BM  <br />
Example: -r 10 <br />


