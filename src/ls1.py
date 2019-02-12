# ls1.py
# local search using simulted annealing 

import random 
import time
import numpy as np
from FileIo import *

def local_search_1(graph, duration, seed):
	random.seed(seed)
	start = time.time() 
	duration = float(duration)
	n = graph.shape[0]
	global_best_route = best_route = get_random_route(n, seed)
	global_best_cost = best_cost = get_cost(best_route, graph)
	# p = 0.3
	T = 1000.0
	a = 0.98
	sol = [[time.time()-start, int(global_best_cost)]]
	num_max_equal = 10
	num_equal = 0

	improve = True
	while improve:
		improve = False
		for i in range(1, len(best_route)-2):
			for j in range(i+1, len(best_route)):
				if j-i == 1: continue
				if i == 1 and j == len(best_route)-1: continue
				new_route = best_route[:]
				new_route[i:j] = best_route[j-1:i-1:-1]
				city1 = best_route[i-1]
				city2 = best_route[i]
				city3 = best_route[j-1]
				city4 = best_route[j]
				new_cost = best_cost - graph[city1-1, city2-1] - graph[city3-1, city4-1] + graph[city1-1, city3-1] + graph[city2-1, city4-1]
				# print("cost", new_cost - best_cost)
				if new_cost < best_cost:
					if new_cost < global_best_cost:
						global_best_cost = new_cost
						global_best_route = new_route
						sol.append([time.time()-start, int(global_best_cost)])
					best_cost = new_cost
					best_route = new_route
					improve = True
				elif random.random() < math.exp((best_cost-new_cost)/T):
					if best_cost == new_cost:
						num_equal = num_equal+1
					else:
						num_equal = 0
					best_cost = new_cost
					best_route = new_route

					improve = True

		T = a * T

		if time.time() > start + duration or num_equal > num_max_equal:
			break 
				
	return global_best_route, global_best_cost, sol

def get_random_route(n, seed):
	route = list(range(1, n+1))
	random.Random(seed).shuffle(route)
	route.append(route[0])
	return route

def get_cost(route, graph):
	cost = 0
	route_cost = [graph[route[i]-1][route[i+1]-1] for i in range(len(route)-1)]
	cost = sum(route_cost)

	return cost

# if __name__ == "__main__":
# 	graph = np.array([[3, 2, 1, 5, 2, 6], 
# 					 [2, 2, 6, 3, 0, 4], 
# 					 [1, 6, 3, 8, 7, 6], 
# 					 [5, 3, 8, 4, 2, 1],
# 					 [2, 0, 7, 2, 1, 3], 
# 					 [6, 4, 6, 1, 3, 5]])
# 	route, cost, sol = local_search_1(graph, 60, 200000)
# 	print(route)
# 	print(cost)
