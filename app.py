import streamlit as st
import pandas as pd
from graph_builder import build_graph
from algorithms import bfs,dfs,dijkstra,benchmark_algorithms
from recommendation import recommendation_rows
from visualization import draw_graph

st.set_page_config(page_title="DAA Book Recommendation",page_icon="📚",layout="wide")
@st.cache_data
def load_books(): return pd.read_csv("data/books.csv")
@st.cache_data
def make_graph(csv_text): return build_graph(pd.read_csv(pd.io.common.StringIO(csv_text)))
df=load_books(); graph,details=make_graph(df.to_csv(index=False))
books={int(r["id"]):r.to_dict() for _,r in df.iterrows()}
titles={i:f'{b["title"]} ({b["author"]})' for i,b in books.items()}

st.title("📚 Graph-Based Book Recommendation System")
st.caption("DAA Project • Graphs • BFS • DFS • Dijkstra • Merge Sort • Priority Queue")
with st.sidebar:
    st.header("Project Controls")
    selected=st.selectbox("Select a book",list(books),format_func=lambda x:titles[x])
    st.divider(); st.write("**Graph model**"); st.write("Vertex = Book"); st.write("Edge = Similarity"); st.write("Weight = 100 − Similarity")

tabs=st.tabs(["Dashboard","Book Details","BFS","DFS","Dijkstra","Recommendations","Algorithm Comparison"])
with tabs[0]:
    c=st.columns(4); c[0].metric("Books / Vertices",len(books)); c[1].metric("Graph Edges",sum(map(len,graph.values()))//2); c[2].metric("Genres",df.genre.nunique()); c[3].metric("Algorithms",5)
    fig=draw_graph(graph,books,focus=selected)
    if fig: st.pyplot(fig,use_container_width=True)
    st.info("Deterministic similarity rules are used. No machine learning is used.")
with tabs[1]:
    b=books[selected]; st.subheader(b["title"]); a,c=st.columns(2)
    a.write(f"**Author:** {b['author']}"); a.write(f"**Genre:** {b['genre']}"); a.write(f"**Rating:** {b['rating']}")
    c.write(f"**Year:** {b['year']}"); c.write(f"**Tags:** {b['tags']}")
    rows=[{"Book":books[v]["title"],"Similarity":round(100-w,2),"Distance":w} for v,w in graph.get(selected,{}).items()]
    st.dataframe(pd.DataFrame(rows).sort_values("Similarity",ascending=False),use_container_width=True)
with tabs[2]:
    st.subheader("Breadth First Search")
    if st.button("Run BFS"):
        order,levels=bfs(graph,selected)
        st.dataframe(pd.DataFrame([{"Order":i+1,"Book":books[x]["title"],"Level":levels[x]} for i,x in enumerate(order)]),use_container_width=True)
    st.code("Queue-based traversal\nTime: O(V + E)\nSpace: O(V)")
with tabs[3]:
    st.subheader("Depth First Search")
    if st.button("Run DFS"):
        order=dfs(graph,selected)
        st.dataframe(pd.DataFrame([{"Order":i+1,"Book":books[x]["title"]} for i,x in enumerate(order)]),use_container_width=True)
    st.code("Depth-first traversal\nTime: O(V + E)\nSpace: O(V)")
with tabs[4]:
    st.subheader("Dijkstra Shortest Path")
    dest=st.selectbox("Destination book",[x for x in books if x!=selected],format_func=lambda x:titles[x])
    if st.button("Run Dijkstra"):
        dist,prev,path=dijkstra(graph,selected,dest)
        if path:
            st.success(f"Path cost: {dist[dest]:.2f}")
            st.write(" → ".join(books[x]["title"] for x in path))
            fig=draw_graph(graph,books,focus=selected,path=path)
            if fig: st.pyplot(fig,use_container_width=True)
        else: st.warning("No connected path exists.")
    st.code("Manually implemented Dijkstra + priority queue\nTime: O((V + E) log V)\nSpace: O(V)")
with tabs[5]:
    st.subheader("Top 5 Recommendations")
    recs=recommendation_rows(selected,books,graph,5)
    if not recs: st.warning("No sufficiently similar books found.")
    for i,r in enumerate(recs,1):
        with st.container(border=True):
            st.markdown(f"### {i}. {r['title']}")
            st.write(f"**Author:** {r['author']} • **Genre:** {r['genre']} • **Rating:** {r['rating']}")
            st.progress(min(100,int(r["similarity"])),text=f"Similarity: {r['similarity']}%")
            st.caption(r["reason"])
    st.info("Recommendations are ranked with manually implemented Merge Sort and retrieved with a Priority Queue.")
with tabs[6]:
    st.subheader("Algorithm Comparison")
    st.dataframe(pd.DataFrame(benchmark_algorithms(graph,selected)),use_container_width=True)
    st.markdown("""| Algorithm | Purpose | Time | Space |
|---|---|---|---|
| BFS | Level traversal | O(V + E) | O(V) |
| DFS | Deep traversal | O(V + E) | O(V) |
| Dijkstra | Weighted shortest path | O((V + E) log V) | O(V) |
| Merge Sort | Ranking | O(n log n) | O(n) |
| Priority Queue | Top-K | O(n log k) | O(k) |""")

