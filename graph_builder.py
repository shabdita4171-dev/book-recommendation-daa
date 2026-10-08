import pandas as pd
import networkx as nx
THRESHOLD=35

def calculate_similarity(a,b):
    score=0; reasons=[]
    if a["genre"].lower()==b["genre"].lower(): score+=40; reasons.append("same genre")
    if a["author"].lower()==b["author"].lower(): score+=30; reasons.append("same author")
    rg=max(0,20-abs(float(a["rating"])-float(b["rating"]))*20)
    score+=rg
    if rg>=15: reasons.append("similar rating")
    common=set(str(a["tags"]).lower().split()) & set(str(b["tags"]).lower().split())
    score+=min(10,len(common)*2.5)
    if common: reasons.append(f"{len(common)} common tags")
    return round(min(score,100),2),reasons

def build_graph(df,threshold=THRESHOLD):
    graph={int(r.id):{} for r in df.itertuples()}; details={}
    rows=df.to_dict("records")
    for i in range(len(rows)):
        for j in range(i+1,len(rows)):
            sim,reasons=calculate_similarity(rows[i],rows[j])
            if sim>=threshold:
                a,b=int(rows[i]["id"]),int(rows[j]["id"]); w=round(100-sim,2)
                graph[a][b]=w; graph[b][a]=w; details[(a,b)]={"similarity":sim,"reasons":reasons}; details[(b,a)]=details[(a,b)]
    return graph,details

def networkx_graph(graph):
    g=nx.Graph()
    for u,nb in graph.items():
        g.add_node(u)
        for v,w in nb.items():
            if u<v: g.add_edge(u,v,weight=w,similarity=round(100-w,2))
    return g
