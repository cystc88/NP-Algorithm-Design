# graph_plot.py 
# Generate SQD and QRTD graphs for local search 

import os, sys, getopt
import csv
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def plot_sqd(method, instance, trace, optimal, maxquality, times=[0.1, 0.5, 1, 5]):
    temp_quality = maxquality/100.0
    interval = temp_quality/100.0
    fig = plt.figure(2)
    plot = fig.add_subplot(111)
    x = np.arange(0,temp_quality + interval, interval)
    for t in times:
        y = []
        for val in x:
            sol_num = 0
            run_num = 0
            c = (val + 1) * optimal
            for file in os.listdir(trace):
                if file.endswith(".trace") and file.startswith(instance+"_"+method):
                    file_path = trace + os.path.sep + file
                    result = check_file(file_path, c, t)
                    run_num += 1
                    if result:
                        sol_num += 1
            y.append(sol_num/float(run_num))
        plot.plot(x*100, y, label=str(t)+"s")

    handles, labels = plot.get_legend_handles_labels()
    box = plot.get_position()
    plot.set_position([box.x0, box.y0, box.width*0.8, box.height])
    lgd = plot.legend(handles, labels, loc='center left', bbox_to_anchor=(1,0.5))
    plot.set_xlabel('Relative Solution Quality (%)')
    plot.set_ylabel('P(solve)')
    plot.set_title('Solution Quality Distributions (SQD)')

    filename = os.path.basename(trace)
    dir = os.getcwd() + '/SQD'
    if not os.path.exists(dir):
        os.makedirs(dir)
    fig.savefig(dir + os.path.sep + filename + instance + '_' + method + '_SQD.png', bbox_extra_artists=(lgd,), bbox_inches='tight')


# graph the QRTD
def plot_qrtd(method, instance, trace, optimal, maxtime, percents=[2, 4, 6, 8]):
    interval = maxtime/500.0
    fig = plt.figure(1)
    plot = fig.add_subplot(111)
    x = np.arange(0,maxtime+interval,interval)
    for p in percents:
        c = optimal + (optimal * p/100.0)
        y = []
        for val in x:
            sol_num = 0
            run_num = 0
            for file in os.listdir(trace):
                if file.endswith(".trace") and file.startswith(instance+"_"+method):
                    file_path = trace + os.path.sep + file
                    result = check_file(file_path, c, val)
                    run_num += 1
                    if result:
                        sol_num += 1
            y.append(sol_num/float(run_num))
        plot.semilogx(x,y,label=str(p)+"%")

    handles, labels = plot.get_legend_handles_labels()
    box = plot.get_position()
    plot.set_position([box.x0, box.y0, box.width*0.8, box.height])
    lgd = plot.legend(handles, labels, loc='center left', bbox_to_anchor=(1,0.5))
    plot.set_xlabel('Time (s)')
    plot.set_ylabel('P(solve)')
    plot.set_title('Qualified Run-time Distributions (QRTD)')

    filename = os.path.basename(trace)
    dir = os.getcwd() + '/QRTD'
    if not os.path.exists(dir):
        os.makedirs(dir)
    fig.savefig(dir + os.path.sep + filename + instance + '_' + method + '_QRTD.png', bbox_extra_artists=(lgd,), bbox_inches='tight')


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hf:o:t:q:m:i:")
    except getopt.GetoptError:
        print ("graph_plot.py -f <trace> -o <optimal> -t <max time> -q <max quality> -m <method> -i <instance>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-f':
            print ("trace: {}".format(arg))
            trace = arg
        elif opt == '-o':
            print ("optimal: {}".format(arg))
            optimal = float(arg)
        elif opt == '-t':
            print ("max time: {}".format(arg))
            maxtime = float(arg)
        elif opt == '-q':
            print ("max quality: {}".format(arg))
            maxquality = float(arg)
        elif opt == '-m': 
            print("method: {}".format(arg))
            method = arg
        elif opt == '-i':
            print("instance: {}".format(arg))
            instance = arg

    plot_qrtd(method, instance, trace, optimal, maxtime)
    plot_sqd(method, instance, trace, optimal, maxquality)

def check_file(file_path, c, t):
    f = open(file_path)
    csv_file = csv.reader(f)
    for time, cost in csv_file:
        if int(cost) <= c and float(time) <= t:
            return True
    return False

if __name__ == "__main__":
    main(sys.argv[1:])

    #python3 graph_plot.py -f ../output/ -o 655454 -t 30 -q 0.5 -m LS1 -i Roanoke
    #python3 graph_plot.py -f ../output/ -o 1654022 -t 1 -q 0.5 -m LS1 -i NYC
    #python3 graph_plot.py -f ../output/ -o 1176151 -t 100 -q 0.5 -m LS2 -i Toronto
    #python3 graph_plot.py -f ../output/ -o 893536 -t 1 -q 0.5 -m LS2 -i Boston

    #python3 graph_plot.py -f ../LS1_output/ -o 655454 -t 30 -q 0.5 -m LS1 -i Roanoke
    #python3 graph_plot.py -f ../LS1_output/ -o 1654022 -t 1 -q 0.5 -m LS1 -i NYC 
    #python3 graph_plot.py -f ../LS1_output/ -o 1176151 -t 100 -q 0.5 -m LS1 -i Toronto  
    #python3 graph_plot.py -f ../LS1_output/ -o 7542 -t 10 -q 0.5 -m LS1 -i berlin52
