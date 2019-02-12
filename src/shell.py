# shell.py
# run different algorithms for the whole datasets

#!/usr/bin/python
import os
import sys
import subprocess

def read_file_list():
    # select the datasets
    filelist = []
    for file in os.listdir('../DATA/'):
        if os.path.splitext(file)[1] == ".tsp":
            filelist.append(file)
    # print("filelist is: ", filelist)
    return filelist

def generate_comprehensive_table(method, max_time):
    #
    # set the initial parameters
    # max_time = 60
    # method = 'Approx'
    print('generate the comprehensive table of the method %s with max_time %s'%(method, max_time))

    filelist = read_file_list()
    # restore the results from the files
    res_time = {}
    res_cost = {}
    # Branch and Bound without seeds
    if method == 'BnB' or method == 'Approx':
        for file in filelist:
            command = 'python3 main.py -inst ../DATA/' + str(file) + ' -alg ' + str(method) + ' -time ' + str(max_time)
            a = subprocess.getoutput(command)
            # print("a is", a)
            a_time = float(a.split(',')[0])
            a_cost = int(a.split(',')[1])
            print("%s, %.2f, %d"%(file, a_time, a_cost))
    elif method == 'LS1' or method == 'LS2':
        for file in filelist:
            temp_time = []
            temp_cost = []
            range_temp = range(5,55,5)
            for i in range_temp:
                command = 'python3 main.py -inst ../DATA/' + str(file) + ' -alg ' + str(method) + ' -time ' + str(max_time) + ' -seed ' + str(i)
                a = subprocess.getoutput(command)
                a_time = a.split(',')[0]
                a_cost = a.split(',')[1]
                temp_time.append(float(a_time))
                temp_cost.append(int(a_cost))
            res_time[file] = temp_time
            res_cost[file] = temp_cost

    else:
        print("Error: input method must be correct")
        exit(1)

        # output the average time and average cost
        for file in filelist:
            avg_time = sum(res_time[file])/len(res_time[file])
            avg_cost = sum(res_cost[file])/len(res_cost[file])
            print("%s, %.2f, %d"%(file, avg_time, avg_cost))
            # print(res_time[file], '\n', res_cost)

if __name__ == "__main__":
    num_args = len(sys.argv)
    # Approx 60
    # BnB 40
    if num_args == 3:
        method = sys.argv[1]
        max_time = sys.argv[2]
        generate_comprehensive_table(method, max_time)
    else:
        print("Error: input arguments must be like:\npython3 shell.py LS2 40")
        exit(1)

