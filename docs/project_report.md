# Project Report

## Introduction
This project applies classical DAA techniques to book recommendation.

## Problem
Recommend books related to a selected book using a weighted similarity graph.

## Graph Model
Book = vertex. Similarity relationship = edge. Weight = 100 - similarity.

## Similarity
Same genre +40, same author +30, rating closeness up to +20, common tags up to +10.

## Algorithms
BFS: level traversal, O(V+E).
DFS: depth traversal, O(V+E).
Dijkstra: weighted shortest path, O((V+E) log V).
Merge Sort: recommendation ranking, O(n log n).
Priority Queue: efficient Top-K retrieval.

## Flow
Select book -> build/use graph -> traverse/find paths -> rank candidates -> Top 5 recommendations.

## Advantages
Simple, explainable, offline and focused on algorithms.

## Limitations
Static dataset and manually selected similarity rules.

## Conclusion
The system demonstrates practical use of graph traversal, shortest path, sorting and priority queues in a recommendation problem.
