import matplotlib.pyplot as plt
import networkx as nx
def draw_graph(graph,books,focus=None,path=None,max_nodes=18):
    g=nx.Graph()
    nodes=([focus]+list(graph.get(focus,{})))[:max_nodes] if focus is not None else list(graph)[:max_nodes]
    for u in nodes:
        g.add_node(u)
        for v,w in graph.get(u,{}).items():
            if v in nodes: g.add_edge(u,v,weight=w)
    if not g: return None
    pos=nx.spring_layout(g,seed=7); fig,ax=plt.subplots(figsize=(11,7))
    nx.draw_networkx_nodes(g,pos,node_size=[900 if n==focus else 650 for n in g.nodes],ax=ax)
    widths=[1.8 if path and u in path and v in path and abs(path.index(u)-path.index(v))==1 else .8 for u,v in g.edges]
    nx.draw_networkx_edges(g,pos,width=widths,ax=ax)
    nx.draw_networkx_labels(g,pos,{n:books[n]["title"][:18] for n in g.nodes},font_size=7,ax=ax)
    ax.set_title("Book Similarity Graph"); ax.axis("off"); fig.tight_layout(); return fig
