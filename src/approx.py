# approx.py
# approximation using MST

import random
import time
import heapq
import numpy as np

def computeMST(graph, seed):
    ans = 0
    V_set = set([])
    V=[]
    for i in range (len(graph)):
        V.append([])

    root = 0
    V_set.add(root)
    heap  = []
    i = 0
    while (i < len(graph)):
        edges = graph[root]

        for edge in edges:
            tar = edge[2]
            if tar not in V_set:
                heapq.heappush(heap, edge)
        while(True):
            edges = heapq.heappop(heap)
            root1 = edges[2]
            if root1 not in V_set:
                root = root1
            else:
                if len(V_set)== len(graph):
                    break
                else:
                    continue
            V_set.add(root1)
            V[edges[1]].append((edges[0],edges[1], edges[2]))
            V[edges[2]].append((edges[0],edges[2], edges[1]))
            ans += edges[0]
            break
        i += 1
    V=np.array(V)
    for v in V:
        np.random.shuffle(v)
    return ans, V

def dfs(graph, root):
    visited = []
    def dfs_walk(node):
        visited.append(node)
        for succ in graph[node]:
            if not succ[2] in visited:
                dfs_walk(succ[2])
    dfs_walk(root)
    return visited

def approx(dis, seed):
    n=len(dis)
    V=[[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if j==i:
                continue
            V[i].append((dis[i][j],i,j))
    ans,mst=computeMST(V, seed)
    ans = float('Inf')
    for i in range(n):
        l=dfs(mst, i)
        l.append(i)
        ll=0
        for i in range(1,len(l)):
            ll += dis[l[i]][l[i-1]]
        if ll<ans:
            route=l
        ans=min(ans,ll)
    return ans ,route

def approximation(graph, duration, seed=30):
    random.seed(seed)
    start = time.time()
    duration = float(duration)
    ans = float('Inf')
    for i in range(50):
        tans,troute = approx(graph, seed)
        if time.time() > start + duration:
            break
        if tans < ans:
            ans=tans
            route=troute

    sol = [[time.time()-start, int(ans)]]
    return route, ans, sol
