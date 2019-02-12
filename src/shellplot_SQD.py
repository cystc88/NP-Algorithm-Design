#!/usr/bin/python
import os
import sys
import subprocess
import matplotlib
import numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_SQD(file_name, method, opt_value, figure_name):
    fontsize = 20
    for max_time in np.arange(0.0005, 0.0025, 0.0005):
        temp_percent = []
        temp_p = []
        for percent in np.arange(0.0, 5, 0.5):
            success = 0
            fail = 0
            for iteration in range(0, 20, 1):
                seed = 5 + iteration * 5
                command = 'python3 main.py -inst ../DATA/' + str(file_name) + ' -alg ' + str(method) + ' -time ' + str(max_time) + ' -seed ' + str(seed)
                a = subprocess.getoutput(command)
                a_time = a.split(',')[0]
                a_cost = a.split(',')[1]
                rel_qual = float(int(a_cost) / int(opt_value))
                # print(rel_qual)
                # print(temp_percent)
                if rel_qual < 1 + percent * 0.01:
                    success = success + 1
                else:
                    fail = fail + 1
            p_solve = success / (success + fail)
            # print(success, fail)
            temp_percent.append(percent)
            temp_p.append(p_solve)
        max_time = round(max_time, 4)
        temp_label = str(max_time) + 's'
        print("max_time, temp_p is: ", max_time, temp_p)
        plt.plot(temp_percent, temp_p, label = temp_label)
    plt.title('$P_{solve}$ vs Relative solution quality (%)', fontsize = fontsize)
    leg = plt.legend(loc='best', shadow = True, fancybox = True)
    xlabel = 'Relative Solution Quality (%)'
    ylabel = '$P_{solve}$'
    plt.xlabel(xlabel, fontsize = fontsize)
    plt.ylabel(ylabel, fontsize = fontsize)
    if not os.path.exists('../graph'):
        os.mkdir('../graph')
    plt.savefig('../graph/' + str(figure_name), fontsize = fontsize)
    # plt.show()
    # plt.close()


if __name__ == "__main__":
    num_args = len(sys.argv)
    # 60 Approx

    if num_args == 1:
        # file_name = 'Boston.tsp'
        # method = 'LS1'
        # opt_value = 893536
        file_name = 'Cincinnati.tsp'
        method = 'LS1'
        opt_value = 277952
        figure_name = file_name.split('.')[0] + '_' + method + '_SQD'
        plot_SQD(file_name, method, opt_value, figure_name)

    if num_args == 4:
        file_name = sys.argv[1]
        method = sys.argv[2]
        opt_value = sys.argv[3]

