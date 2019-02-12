#!/usr/bin/python
import os
import sys
import subprocess
import matplotlib
import numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_QRTD(file_name, method, opt_value, figure_name):
    fontsize = 20
    for percent in np.arange(0.2, 1.0, 0.2):
        temp_time = []
        temp_p = []
        # for max_time in np.arange(0.00, 0.0020, 0.0002):
        for max_time in np.arange(0.00, 2.00, 0.20):
            success = 0
            fail = 0
            for iteration in range(0, 20, 1):
                i = iteration * 5 + 5
                command = 'python3 main.py -inst ../DATA/' + str(file_name) + ' -alg ' + str(method) + ' -time ' + str(max_time) + ' -seed ' + str(i)
                a = subprocess.getoutput(command)
                a_time = a.split(',')[0]
                a_cost = a.split(',')[1]
                rel_qual = float(int(a_cost) / int(opt_value))
                # print(rel_qual)
                if rel_qual < 1 + percent * 0.01:
                    success = success + 1
                else:
                    fail = fail + 1
            print('success is %d fail is %d'%(success, fail))
            p_solve = success / (success + fail)
            temp_time.append(max_time)
            temp_p.append(p_solve)
        percent = round(percent, 2)
        temp_label = '$q$ = ' + str(percent) + '%'
        print("temp_p is: ", temp_p)
        plt.plot(temp_time, temp_p, label = temp_label)
    plt.title('$P_{solve}$ vs Time(s)', fontsize = fontsize)
    leg = plt.legend(loc='best', shadow = True, fancybox = True)
    xlabel = 'Time(s)'
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
        file_name = 'Boston.tsp'
        method = 'LS2'
        opt_value = 893536
        # file_name = 'Cincinnati.tsp'
        # method = 'LS2'
        # opt_value = 277952
        # file_name = 'Berlin.tsp'
        # method = 'LS2'
        # opt_value = 7542
        figure_name = file_name.split('.')[0] + '_' + method + '_QRTD'
        plot_QRTD(file_name, method, opt_value, figure_name)

    if num_args == 4:
        file_name = sys.argv[1]
        method = sys.argv[2]
        opt_value = sys.argv[3]

