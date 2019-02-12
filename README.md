# Algorithm-Design-Course
## Traveling-Salesperson-Problem
The Traveling Salesperson Problem (TSP) arises in numerous applications such as vehicle routing, circuit board drilling, VLSI design, robot control, X-ray crystallography, machine scheduling and computational biology. In this project, you will attempt to solve the TSP using different algorithms, evaluating their theoretical and experimental complexities on both real and random datasets.

The language we use here is python 3, with `scipy`, `numpy` and `matplotlib` installed. To build the environment, we could use the following command line `pip install scipy`, `pip install numpy` and `pip install matplotlib`.

To get the output of one specific dataset for one specific algorithm. Run in the terminal in the src directory with the command line:

`python3 -inst <filename> -alg [BNB | Approx | LS1 | LS2] -time <cutoff_in_seconds> [-seed <random_seed>]`

For example:

    `python3 main.py -inst ../DATA/Boston.tsp -alg LS2 -time 60 -seed 40`

To generate all the outputs (`.trace` and `.sol`) of all the data files (`.tsp`) and ouput the average time (seconds) and average solution cost in at least 10 times, run the shell.py with the following command line：

`python3 shell.py [BNB | Approx | LS1 | LS2] [cutoff_in_seconds]`

For example:

    `python3 shell.py LS2 60`

All the output files will be generated in the file `output` in the same directory with `src` and `DATA`.

For generating the relevant plots, we could use the `graph_plot.py` with the following command line:

`python3 graph_plot.py -f <tracefile> -o <optimal> -t <max time> -q <max quality> -m <method> -i <instance>`

For example:

`python3 graph_plot.py -f ../output/ -o 655454 -t 30 -q 0.5 -m LS1 -i Roanoke`

