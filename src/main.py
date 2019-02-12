# main.py
# run different algorithms

from FileIo import *
from ls1 import *
from ls2 import *
from bnb import *
from approx import *
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-inst", "--file_name", help="File name")
    parser.add_argument("-alg", "--method", help="Method")
    parser.add_argument("-time", "--cut_off_time", help="Cut off time")
    parser.add_argument("-seed", "--random_seed", help="Seed")

    args = parser.parse_args()

    graph, name, edge_type, dimension = read_tsp_file(args.file_name)
    dis = distance_computing(graph, edge_type)

    start = time.time()
    if args.method == 'BnB':
        route, cost, sol = branch_and_bound(dis, args.cut_off_time)
    elif args.method == 'LS1':
        route, cost, sol = local_search_1(dis, args.cut_off_time, args.random_seed)
    elif args.method == 'LS2':
            route, cost, sol = local_search_2(dis, args.cut_off_time, args.random_seed)
    elif args.method == 'Approx':
        route, cost, sol = approximation(dis, args.cut_off_time, args.random_seed)

    elapsed = (time.time() - start)  #seconds

    print('%0.2f, %d'%(elapsed, int(cost)))
    output_sol(cost, route, name, args.method, args.cut_off_time, args.random_seed)
    output_trace(sol, name, args.method, args.cut_off_time, args.random_seed)

