from collections import deque
import heapq, math, random, time

def bfs(graph, start):
    visited={start}; order=[]; levels={start:0}; q=deque([start])
    while q:
        u=q.popleft(); order.append(u)
        for v in graph.get(u,{}):
            if v not in visited:
                visited.add(v); levels[v]=levels[u]+1; q.append(v)
    return order, levels

def dfs(graph, start):
    visited=set(); order=[]
    def visit(u):
        visited.add(u); order.append(u)
        for v in graph.get(u,{}):
            if v not in visited: visit(v)
    visit(start); return order

def dijkstra(graph, start, target=None):
    dist={u:math.inf for u in graph}; prev={u:None for u in graph}
    dist[start]=0; pq=[(0,start)]; done=set()
    while pq:
        d,u=heapq.heappop(pq)
        if u in done: continue
        done.add(u)
        if target is not None and u==target: break
        for v,w in graph.get(u,{}).items():
            nd=d+w
            if nd<dist[v]:
                dist[v]=nd; prev[v]=u; heapq.heappush(pq,(nd,v))
    path=[]
    if target is not None and dist.get(target,math.inf)<math.inf:
        cur=target
        while cur is not None: path.append(cur); cur=prev[cur]
        path.reverse()
    return dist,prev,path

def merge_sort(items,key=lambda x:x):
    if len(items)<=1: return items[:]
    m=len(items)//2; left=merge_sort(items[:m],key); right=merge_sort(items[m:],key)
    out=[]; i=j=0
    while i<len(left) and j<len(right):
        if key(left[i])>=key(right[j]): out.append(left[i]); i+=1
        else: out.append(right[j]); j+=1
    return out+left[i:]+right[j:]

def priority_top_k(items,k):
    return heapq.nlargest(k,items,key=lambda x:x["similarity"])

def recommend_books(book_id,graph,k=5):
    c=[{"id":v,"similarity":round(100-w,2),"distance":w} for v,w in graph.get(book_id,{}).items()]
    return merge_sort(c,key=lambda x:x["similarity"])[:k]

def benchmark_algorithms(graph,start):
    results=[]
    for name,fn in [("BFS",lambda:bfs(graph,start)),("DFS",lambda:dfs(graph,start))]:
        t=time.perf_counter(); fn(); results.append({"Algorithm":name,"Time (ms)":round((time.perf_counter()-t)*1000,4)})
    target=next((x for x in graph if x!=start),start)
    t=time.perf_counter(); dijkstra(graph,start,target)
    results.append({"Algorithm":"Dijkstra","Time (ms)":round((time.perf_counter()-t)*1000,4)})
    return results
