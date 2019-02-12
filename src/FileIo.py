# FileIo.py
# Read data and compute distance, output .sol and .trace

import sys
import time
import os
import math
import numpy as np
from scipy.spatial import distance

def read_tsp_file(text_file = "Berlin.tsp"):
    with open(text_file, 'r') as f:

        X = []
        name = 'name'
        dimension = 0
        edge_type = 'default'

        line = f.readline().strip(' ').strip('\n')
        while line:
            if line.split(': ')[0] == 'NAME':
                name = line.split(': ')[1].split('.')[0]
            elif line.split(': ')[0] == 'DIMENSION':
                dimension = line.split(': ')[1]
            elif line.split(': ')[0] == 'EDGE_WEIGHT_TYPE':
                edge_type = line.split(': ')[1]
            elif line.split(' ')[0] == 'NODE_COORD_SECTION':
                # print('\n=====reach the start point====')
                break
            line = f.readline().strip(' ').strip('\n')

        # print("Name is: ", name,
        #                 "\nDimension is: ", dimension,
        #                 "\nedge type is: ", edge_type)

        line = f.readline().strip(' ').strip('\n')
        while line.split(' ')[0] != 'EOF':
            temp_data = line.split(" ")
            latitude = float(temp_data[1])
            longtitude = float(temp_data[2])
            temp = []
            temp.append(latitude)
            temp.append(longtitude)
            X.append(temp)
            line = f.readline().strip(' ').strip('\n')

        X = np.array(X)
        return X, name, edge_type, dimension

def output_sol(quality, X, name, alg, time, seed = None):
    if not os.path.exists('../output'):
        os.mkdir('../output')
    if seed == None:
        output = '../output/' + str(name) + '_' + str(alg) + '_' + str(time) + '.sol'
    else:
        output = '../output/' + str(name) + '_' + str(alg) + '_' + str(time) + '_' + str(seed) + '.sol'
    with open(output,'w') as file:
        file.write('%d\n'%(quality))
        write_str = ", ".join(str(i) for i in X)
        file.write(write_str)
        file.write('\n')
    file.close()

def output_trace(X, name, alg, time, seed = None):
    if not os.path.exists('../output'):
        os.mkdir('../output')
    if seed == None:
        output = '../output/' + str(name) + '_' + str(alg) + '_' + str(time) + '.trace'
    else:
        output = '../output/' + str(name) + '_' + str(alg) + '_' + str(time) + '_' + str(seed) + '.trace'
    with open(output,'w') as file:
        for arr in X:
            write_str = '%.2f, %d\n'%(arr[0], arr[1])
            file.write(write_str)
    file.close()


def distance_computing(nodes, edge_type):
    N = nodes.shape[0]
    dis = np.zeros((N,N))
    if edge_type == 'EUC_2D':
        dis = distance.cdist(nodes, nodes, 'euclidean')
    elif edge_type == 'GEO':
        RRR = 6378.388
        radians = coordiate_convert(nodes)
        for i in range(N):
            for j in range(i+1, N):
                q1 = np.cos(radians[i][1] - radians[j][1])
                q2 = np.cos(radians[i][0] - radians[j][0])
                q3 = np.cos(radians[i][0] + radians[j][0])
                dis[i][j] = (int)(RRR * np.arccos(0.5*((1.0 + q1)* q2 - (1.0 - q1) * q3) ) + 1.0)
                dis[j][i] = dis[i][j]
    return dis

def coordiate_convert(nodes):
    PI = 3.141592
    # temp = nodes + 0.5 
    deg = nodes.astype(np.int64)
    # print('deg is: \n', deg)
    min_val = nodes - deg
    # print('min_val is: \n', min_val)
    radians = PI * (deg + 5.0 * min_val / 3.0) / 180.0
    # print('radians are: \n', radians)
    return radians


def test_code():
    X, name, edge_type, dimension = read_tsp_file()

    print("=====test for EUC_2D====\n",
            X, edge_type, dimension,
            "\n=========")
    print('Distance is: \n', distance_computing(X, edge_type))

    Y, name, edge_type, dimension = read_tsp_file('ulysses16.tsp')
    print("=====test for GEO====\n",
        Y, edge_type, dimension,
        "\n=========")
    print('Distance is: \n', distance_computing(Y, edge_type))

    quality = 0.000
    X =[1, 2, 3, 4]

    output_sol(quality, X, name, 'alg', 400)
    output_trace(Y, name, 'alg', 400, 20)

