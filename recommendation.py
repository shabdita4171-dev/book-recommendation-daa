from algorithms import recommend_books, priority_top_k
def recommendation_rows(selected_id,books,graph,k=5):
    ranked=recommend_books(selected_id,graph,max(k,10)); rows=[]
    for x in ranked:
        b=books[x["id"]]
        rows.append({"id":x["id"],"title":b["title"],"author":b["author"],"genre":b["genre"],"rating":b["rating"],"similarity":x["similarity"],"reason":"Strong graph similarity based on shared book attributes"})
    return priority_top_k(rows,k)
