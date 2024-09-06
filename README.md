Cache Simulation and Performance Analysis
This project involves simulating cache memory performance, plotting graphs for miss rate and hit rate based on different cache parameters such as cache size, block size, and associativity.


To run the codes we have to install numpy prettytables and matplotlib


Files and Functions'

Code 1: Driver Code for Cache Simulation
This part of the project processes input trace files and calculates cache statistics. The key steps include:

Reading multiple trace files.
Extracting relevant information (cache size, block size, associativity) from the traces.
Performing cache-related computations (hit rate, miss rate).
Files used:

gcc.trace
gzip.trace
mcf.trace
swim.trace
twolf.trace


Code 2: Graph Plotting
This part of the project generates plots based on the cache simulation data:

For each trace file, graphs are generated based on different cache parameters:
Cache Size vs Miss Rate
Block Size vs Miss Rate
Associativity vs Hit Rate
Key Features:

The x-axis is scaled using powers of 2 to represent various cache sizes and associativity values.
A legend helps differentiate between the graphs for different trace files.

