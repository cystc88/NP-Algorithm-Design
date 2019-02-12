# ls2.py
# local search using iterated local search

import random
import time
import numpy as np
from FileIo import *

def local_search_2(graph, duration, seed):
    random.seed(seed)
    start = time.time()
    duration = float(duration)
    n = graph.shape[0]
    max_iterations = 500

    #Route Initialization
    initial_route = get_random_route(n, seed)
    # print('==', initial_route)
    initial_cost = get_cost(initial_route, graph)
    sol = [[time.time()-start, int(initial_cost)]]

    # Local search from the initial solution
    global_best_route, global_best_cost = local_search(initial_route, initial_cost, graph, start, duration, initial_route, initial_cost, sol)

    # Do the iteration local search
    for step in range(0, max_iterations):
        # perturb the best route
        perturbed_route = perturbation(global_best_route, seed, graph)
        perturbed_cost = get_cost(perturbed_route, graph)
        # local search from the perturbation result
        temp_best_route, temp_best_cost = local_search(perturbed_route, perturbed_cost, graph, start, duration, global_best_route, global_best_cost, sol)
        if temp_best_cost < global_best_cost:
            global_best_cost = temp_best_cost
            global_best_route = temp_best_route
    return global_best_route, global_best_cost, sol

def local_search(best_route, best_cost, graph, start, duration, global_best_route, global_best_cost, sol):
    count = 0
    max_no_improve = 10
    while count < max_no_improve:
        for i in range(1, len( best_route) - 2):
            for j in range(i + 1, len(best_route)):
                if j - i == 1 or (i == 1 and j == len(best_route) - 1):
                    continue
                # generate the new route by permutation of the route i -> j to j -> i
                new_route = best_route[:]
                new_route[i:j] = best_route[j-1:i-1:-1]
                city1 = best_route[i-1]
                city2 = best_route[i]
                city3 = best_route[j-1]
                city4 = best_route[j]
                new_cost = best_cost - graph[city1-1, city2-1] - graph[city3-1, city4-1] + graph[city1-1, city3-1] + graph[city2-1, city4-1]
                if new_cost < best_cost:
                    count = 0
                    best_cost = new_cost
                    best_route = new_route
                    if new_cost < global_best_cost:
                        global_best_cost = new_cost
                        global_best_route = new_route
                        sol.append([time.time()-start, int(global_best_cost)])
                count += 1
            if time.time() > start + duration:
                break

    return best_route, best_cost

def perturbation(best_route, seed, graph):
    accept = 5000
    size = len(best_route)
    gap = int(size/4+1)
    pos1 = random.randint(1, gap)
    pos2 = pos1 + random.randint(1, gap)
    pos3 = pos2 + random.randint(1, gap)
    new_route = [best_route[0]] \
                + best_route[1:pos1] \
                + best_route[pos3:size-1] \
                + best_route[pos2:pos3] \
                + best_route[pos1:pos2] \
                + [best_route[size-1]]
    # n = len(best_route) - 1
    # new_route = get_random_route(n, seed)
    old_cost = get_cost(best_route, graph)
    new_cost = get_cost(new_route, graph)
    if accept_rule(old_cost, new_cost, accept):
        return new_route
    return best_route

def get_random_route(n, seed):
    route = list(range(1,n+1))
    random.shuffle(route)
    route.append(route[0])
    return route

def get_cost(route, graph):
    cost = 0
    route_cost = [graph[route[i]-1][route[i+1]-1] for i in range(len(route)-1)]
    cost = sum(route_cost)
    return cost

def accept_rule(old_cost, new_cost, accept):
    return True if new_cost >= (old_cost - accept)  or new_cost <= (old_cost + accept) else False





