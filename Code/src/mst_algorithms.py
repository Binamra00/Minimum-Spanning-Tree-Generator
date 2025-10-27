# mst_algorithms.py
# Defines the MSTAlgorithms class for computing Minimum Spanning Trees using Kruskal's and Prim's algorithms.
# Optimized for runtime efficiency with NetworkX graph input, focusing on edge comparisons and iterations as metrics.
# Includes Prim's with in_heap optimization for dense graphs and Kruskal's with rank-based Union-Find.

import time # Module for measuring execution time with high precision
from heapq import heappush, heappop # Heap queue functions for Prim's priority queue implementation

class MSTAlgorithms:
    def __init__(self, graph):
        self.num_nodes = graph.number_of_nodes()
        self.node_map = {node: i for i, node in enumerate(graph.nodes())}  # Map original nodes to 0-based indices
        self.edges_list = [(self.node_map[u], self.node_map[v], d['weight']) for u, v, d in graph.edges(data=True)]
        self.adj_list = [[] for _ in range(self.num_nodes)]
        for u, v, w in self.edges_list:
            self.adj_list[u].append((v, w))
            self.adj_list[v].append((u, w))
        self.reset_metrics()

    def reset_metrics(self):
        # Reset performance metrics before each algorithm run to ensure fresh measurements.
        self.runtime = 0  # Runtime in milliseconds
        self.edge_comparisons = 0  # Number of edge weight comparisons
        self.iterations = 0  # Number of iterations

    def get_metrics(self):
        # Return performance metrics from the last algorithm run as a dictionary.
        return {
            'runtime': self.runtime,  # Time taken in milliseconds
            'edge_comparisons': self.edge_comparisons,  # Total edge comparisons
            'iterations': self.iterations  # Total iterations
        }

    def find(self, parent, i):
        # Find the root of the set containing node i with path compression for near-O(1) lookups.
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])  # Recursively compress path to root
        return parent[i]

    def union(self, parent, rank, x, y):
        # Unite two sets using rank to maintain balanced trees, optimizing find operations.
        px, py = self.find(parent, x), self.find(parent, y)  # Get roots of x and y
        if px == py:
            return  # Already in same set, no union needed
        if rank[px] < rank[py]:
            px, py = py, px  # Ensure px has higher or equal rank
        parent[py] = px  # Attach smaller tree under larger
        if rank[px] == rank[py]:
            rank[px] += 1  # Increment rank if trees were equal height

    # Kruskal's MST Algorithm
    # Computes the Minimum Spanning Tree using edge sorting and Union-Find.
    # Input: Preprocessed graph data from self.edges_list
    # Output: List of MST edges as (u, v, weight) tuples, None (no error) or error message
    # Time Complexity: O(E log E) due to sorting, where E is the number of edges
    def kruskal_mst(self):
        self.reset_metrics()  # Clear previous metrics
        start_time = time.perf_counter()  # Start high-precision timer
        if self.num_nodes == 0:
            self.runtime = (time.perf_counter() - start_time) * 1000  # Record empty graph runtime
            return [], "Graph is empty"  # Early return for empty graph

        edges = sorted(self.edges_list, key=lambda x: x[2])  # Sort edges by weight (O(E log E))
        self.edge_comparisons += len(edges) * (len(edges).bit_length() - 1)  # Approximate sorting comparisons
        parent = list(range(self.num_nodes))  # Initialize Union-Find parent array
        rank = [0] * self.num_nodes  # Rank array for balanced trees
        mst_edges = []  # Store MST edges

        for u, v, weight in edges:  # Process each edge in sorted order
            self.iterations += 1  # Count iteration
            x = self.find(parent, u)  # Find root of u's set
            y = self.find(parent, v)  # Find root of v's set
            self.edge_comparisons += 1  # Count cycle check comparison
            if x != y:  # If no cycle, include edge
                mst_edges.append((u, v, weight))  # Add to MST
                self.union(parent, rank, x, y)  # Merge sets

        self.runtime = (time.perf_counter() - start_time) * 1000  # Calculate runtime in ms
        return mst_edges, None  # Return MST and no error

    # Prim's MST Algorithm
    # Computes the Minimum Spanning Tree using a priority queue with in_heap optimization.
    # Input: Preprocessed graph data from self.adj_list
    # Output: List of MST edges as (u, v, weight) tuples, None (no error) or error message
    # Time Complexity: O(E + V log V) with in_heap, where E is edges and V is nodes
    def prim_mst(self):
        # Reset performance metrics before running the algorithm
        self.reset_metrics()
        # Start high-precision timer for runtime measurement
        start_time = time.perf_counter()
        # Handle empty graph case
        if self.num_nodes == 0:
            self.runtime = (time.perf_counter() - start_time) * 1000  # Record runtime in milliseconds
            return [], "Graph is empty"  # Return empty edge list and error message

        # Track visited nodes to avoid cycles
        visited = set()
        # Initialize priority queue with a dummy edge: (weight, node, parent)
        # Start at node 0 with weight 0 and no parent
        heap = [(0, 0, None)]
        # Track nodes in heap with their current minimum weight to avoid duplicates and ensure lightest edges
        in_heap = {0: 0}  # Key: node, Value: current min weight in heap
        # Store MST edges as (parent, node, weight) tuples
        mst_edges = []

        # Process until heap is empty or all nodes are visited
        while heap:
            # Increment iteration counter for metrics
            self.iterations += 1
            # Pop the edge with minimum weight from the heap
            weight, u, parent = heappop(heap)
            # Count heap comparison for metrics
            self.edge_comparisons += 1
            # Skip if node is already in MST (could happen with outdated heap entries)
            if u in visited:
                continue
            # Mark node as visited, adding it to the MST
            visited.add(u)
            # Remove node from in_heap since it’s now processed
            del in_heap[u]
            # If not the dummy starting edge, add edge to MST
            if parent is not None:
                mst_edges.append((parent, u, weight))
            # Explore all neighbors of the current node
            for v, w in self.adj_list[u]:
                # Only consider unvisited nodes
                if v not in visited:
                    # If node isn’t in heap yet or we found a lighter edge, update it
                    if v not in in_heap or w < in_heap[v]:
                        heappush(heap, (w, v, u))  # Push new or lighter edge to heap
                        in_heap[v] = w  # Update min weight for v in heap
                        # Count comparison for metrics (checking or updating weight)
                        self.edge_comparisons += 1

        # Calculate runtime in milliseconds
        self.runtime = (time.perf_counter() - start_time) * 1000
        # Check if graph is unconnected (not all nodes visited)
        if len(visited) < self.num_nodes:
            return mst_edges, "Graph is unconnected—partial MST returned"
        # Return MST edges and no error for connected graph
        return mst_edges, None