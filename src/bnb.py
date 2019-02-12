# bnb.py
# branch and bound algorithm

import copy
import heapq
import numpy as np
from FileIo import *
import time

def branch_and_bound(dist_matrix, cutoff=600.0):
    if dist_matrix.shape[0] <= 20:
        return branch_and_bound_BeFS(dist_matrix, cutoff)
    else:
        return branch_and_bound_dfs(dist_matrix, cutoff)


def branch_and_bound_dfs(dist_matrix, cutoff=600.0):
    start_time = time.clock()
    n = dist_matrix.shape[0]
    np.fill_diagonal(dist_matrix, float('inf'))
    par_path = []
    lb = 0.0
    par_cost = 0.0
    start = 0
    heur = 0.0
    start_mat = np.copy(dist_matrix)
    row = [i for i in range(n)]
    col = [i for i in range(n)]
    paths = []
    best_cost = float('inf')
    sol = []
    ctf = float(cutoff)
    frontier = []

    path = [p for p in np.arange(1, n + 1)]
    best_cost = get_cost(path, dist_matrix)

    path = [p - 1 for p in path]
    path.remove(start)
    paths.append((best_cost, path))
    # (lb, cost, heuristic, vertex, push-order, row, column, matrix, partial_parth)
    frontier.append((lb, par_cost, heur, start, 0, row, col, start_mat, par_path))

    i = 0
    front_maxlen = 0
    order = 0
    while frontier:
        i += 1
        if (time.clock() - start_time >= ctf):
            break

        if (front_maxlen < len(frontier)):
            front_maxlen = len(frontier)

        # pop frontier
        exp_lb, exp_cost, exp_heur, exp_vert, _, row, col, exp_mat, exp_path = frontier.pop()

        # dead end
        if is_deadend(exp_mat):
            continue

        adj_path = copy.deepcopy(exp_path)
        # add the expanding point into path
        if not (exp_vert == start):
            adj_path.append(exp_vert)

        if len(adj_path) == n - 1:
            path_cost = exp_cost + dist_matrix[exp_vert][start]
            if path_cost < best_cost:
                paths.append((path_cost, adj_path))
                best_cost = path_cost
                sol.append([time.clock()-start_time, int(best_cost)])
            continue

        adjs = dist_matrix[exp_vert, col]
        for j in range(len(col)-1):

            adj_row = copy.deepcopy(row)
            adj_col = copy.deepcopy(col)
            exp_indx = adj_row.index(exp_vert)

            adj_mat = np.copy(exp_mat)
            if (not exp_vert == start) or (not len(adj_path) == n - 1):
                adjs[0] = -1
            exp_adj_max_indx = np.argmax(adjs)
            adj_vert = col[exp_adj_max_indx]
            adj_indx = adj_col.index(adj_vert)
            adjs[exp_adj_max_indx] = -1

            exp_adj_cost = dist_matrix[exp_vert][adj_vert]
            adj_cost = exp_cost + exp_adj_cost

            if not (exp_indx == len(adj_row) - 1):
                adj_mat[exp_indx: -1] = adj_mat[exp_indx + 1:]
            if not (adj_indx == len(adj_col) - 1):
                adj_mat[:, adj_indx: -1] = adj_mat[:, adj_indx + 1:]
            adj_mat = adj_mat[:-1, :-1]

            del adj_row[exp_indx]
            del adj_col[adj_indx]
            adj_heur = heurisitic_dy_rcm(adj_mat)
            adj_lb = exp_cost + adj_heur

            if adj_lb < best_cost:
                frontier.append((adj_lb, adj_cost, adj_heur, adj_vert, i, adj_row, adj_col, adj_mat, adj_path))
                order += 1

    paths_cp = []
    for p in paths:
        p_cp = [x+1 for x in p[1]]
        p_cp.insert(0, start+1)
        p_cp.append(start + 1)
        paths_cp.append((p[0], p_cp))

    heapq.heapify(paths_cp)

    return min(paths_cp)[1], min(paths_cp)[0], sol


def branch_and_bound_BeFS (dist_matrix, cutoff=600.0):

    start_time = time.clock()
    n = dist_matrix.shape[0]
    np.fill_diagonal(dist_matrix, float('inf'))
    best_cost = float('inf')
    paths = []
    start = 0
    start_mat = np.copy(dist_matrix)
    par_path = []
    sol = []
    ctf = float(cutoff)
    frontier = []

    path = [p for p in np.arange(1, n+1)]
    best_cost = get_cost(path, dist_matrix)

    path = [p-1 for p in path]
    path.remove(start)
    paths.append((best_cost, path))
    # vertex labels of each row, with outgoing edges
    row_ls = [i for i in range(n)]
    # vertex labels of each column, with incoming edges
    col_ls = [i for i in range(n)]

    # frontier tuple (lb, cost, heuristic, vertex, push-order, row, column, matrix, partial_parth)
    heapq.heappush(frontier, (0.0, 0.0, 0.0, start, 0, row_ls, col_ls, start_mat, par_path))

    i = 0
    while frontier:
        i += 1
        if (time.clock() - start_time >= ctf):
            break

        # pop frontier
        exp_lb, exp_cost, exp_heur, exp_vert, _, row, col, exp_mat, exp_path = heapq.heappop(frontier)

        # dead end
        if is_deadend (exp_mat):
            continue

        adj_path = copy.deepcopy(exp_path)
        # add the expanding point into path
        if not (exp_vert == start):
            adj_path.append(exp_vert)

        if len(adj_path) == n - 1:
            path_cost = exp_cost + dist_matrix[exp_vert][start]
            if path_cost < best_cost:
                paths.append((path_cost, adj_path))
                best_cost = path_cost
                sol.append([time.clock()-start_time, int(best_cost)])
            continue

        adj_row = copy.deepcopy(row)
        adj_col = copy.deepcopy(col)
        exp_indx = adj_row.index(exp_vert)

        # include the shortest edge (exp_vert, adj_vert)
        adj_mat = np.copy(exp_mat)
        adjs = adj_mat[exp_indx]
        # not include edge to start vertex until having all other vertices in path
        if (not exp_vert == start) or (not len(adj_path) == n - 1):
            adjs[0] = float('inf')
        exp_adj_min_indx = np.argmin(adjs)
        adj_vert = col[exp_adj_min_indx]
        adj_indx = adj_col.index(adj_vert)

        exp_adj_cost = dist_matrix[exp_vert][adj_vert]
        adj_cost = exp_cost + exp_adj_cost

        if not (exp_indx == len(adj_row) - 1):
            adj_mat[exp_indx: -1] = adj_mat[exp_indx + 1:]
        if not (adj_indx == len(adj_col) - 1):
            adj_mat[:, adj_indx: -1] = adj_mat[:, adj_indx + 1:]
        adj_mat = adj_mat[:-1, :-1]
        del adj_row[exp_indx]
        del adj_col[adj_indx]

        adj_heur = heurisitic_dy_rcm(adj_mat)
        adj_lb = exp_cost + adj_heur

        if adj_lb < best_cost:
            heapq.heappush(frontier, (adj_lb, adj_cost, adj_heur, adj_vert, i, adj_row, adj_col, adj_mat, adj_path))

        # exclude the shortest edge (exp_vert, adj_vert)
        excld_mat = exp_mat
        excld_mat[exp_indx][adj_indx] = float('inf')

        # no more edges from the expanding vertex
        if is_deadend (excld_mat):
            continue

        excld_heur = heurisitic_dy_rcm(excld_mat)
        excld_lb = exp_cost + excld_heur
        if not excld_lb >= best_cost:
            heapq.heappush(frontier, (excld_lb, exp_cost, exp_heur, exp_vert, i, row, col, excld_mat, exp_path))

    paths_cp = []
    for p in paths:
        p_cp = [x+1 for x in p[1]]
        p_cp.insert(0, start+1)
        p_cp.append(start + 1)
        paths_cp.append((p[0], p_cp))

    heapq.heapify(paths_cp)

    return min(paths_cp)[1], min(paths_cp)[0], sol


def is_deadend (adj_mat):
    mask = (adj_mat[:, 1:] == float('inf'))
    col_test = np.all(mask, axis=0).sum()
    if col_test > 0:
        return True
    else:
        row_test = np.all(mask, axis=1).sum()
        if row_test > 0 and mask.shape[1] > 1:
            return True
        else:
            return False


def heurisitic_dy_rcm(mat):

    # min of each row
    mat = np.copy(mat)
    row_min = np.min(mat, axis=1)
    reduction = np.sum(row_min)
    row_min = row_min[:, np.newaxis]
    mat -= row_min

    # min of each column
    col_min = np.min(mat, axis=0)
    reduction += np.sum(col_min)
    heur = reduction

    return heur

def get_cost(route, graph):
    cost = 0
    route_cost = [graph[route[i]-1][route[i+1]-1] for i in range(len(route)-1)]
    cost = sum(route_cost)
    return cost

# if __name__ == "__main__":
#     # Boston.tsp 60 LS1 20
#     # ulysses16.tsp - 15pt
#     # Cincinnati.tsp - 10pt
#     # Atlanta.tsp  - 20 pt
#     # Champaign.tsp
#     graph, name, edge_type, dimension = read_tsp_file("../DATA/ulysses16.tsp")
#
#     dis = distance_computing(graph, edge_type)
#     # branch_and_bound(dis)
#     # branch_and_bound_dfs(dis)
#
#     cut_off_time = 600
#     # route, cost, solut = branch_and_bound(dis, cut_off_time)
#     route, cost, solut = branch_and_bound_BeFS(dis, cut_off_time)
#     print route
#     print cost
#     print solut
