## combined_metrics_chart.py
# Benchmarks Kruskal’s and Prim’s MST algorithms on dense random graphs, measuring runtime and space complexity.
# Generates charts comparing performance across varying graph sizes using NetworkX graphs.
# Optimized Prim’s with in_heap for runtime efficiency; outputs averaged metrics over multiple runs.

import matplotlib.pyplot as plt  # For plotting runtime and space complexity charts
import networkx as nx  # For graph generation and manipulation
import numpy as np  # For averaging metrics
import time  # For runtime measurement
import sys  # For space complexity calculation
from heapq import heappush, heappop  # For Prim’s priority queue

nodes = [5, 50, 100, 200, 300, 400, 500]  # Graph sizes to test
num_runs = 100  # Number of runs for averaging
kruskal_runtimes_avg = []  # Store average Kruskal’s runtimes
prim_runtimes_avg = []  # Store average Prim’s runtimes
kruskal_space_avg = []  # Store average Kruskal’s space usage
prim_space_avg = []  # Store average Prim’s space usage

# Kruskal’s MST Algorithm
# Computes the Minimum Spanning Tree using edge sorting and Union-Find.
# Input: NetworkX graph with weighted edges
# Output: MST as list of (u, v, weight) tuples, parent and rank arrays for space tracking
# Time Complexity: O(E log E), where E is the number of edges
def kruskal_mst(graph):
    edges = sorted([(u, v, data['weight']) for u, v, data in graph.edges(data=True)], key=lambda x: x[2])  # Sort edges by weight
    parent = list(range(graph.number_of_nodes()))  # Initialize Union-Find parent array
    rank = [0] * graph.number_of_nodes()  # Rank array for balanced trees

    def find(parent, i):  # Find root with path compression
        if parent[i] != i:
            parent[i] = find(parent, parent[i])  # Recursively compress path
        return parent[i]

    def union(parent, rank, x, y):  # Unite sets with rank optimization
        px, py = find(parent, x), find(parent, y)  # Get roots
        if px == py:
            return  # Already in same set
        if rank[px] < rank[py]:
            px, py = py, px  # Ensure px has higher or equal rank
        parent[py] = px  # Attach smaller tree
        if rank[px] == rank[py]:
            rank[px] += 1  # Increment rank if equal height

    mst = []  # Store MST edges
    for u, v, weight in edges:  # Process sorted edges
        if find(parent, u) != find(parent, v):  # Check for cycle
            union(parent, rank, u, v)  # Merge sets
            mst.append((u, v, weight))  # Add edge to MST
    return mst, parent, rank  # Return MST and structures for space measurement

# Prim’s MST Algorithm
# Computes the Minimum Spanning Tree using a priority queue with in_heap optimization.
# Input: NetworkX graph with weighted edges
# Output: MST as list of (u, v, weight) tuples, space complexity in KB
# Time Complexity: O(E + V log V), where E is edges and V is nodes
def prim_mst(graph):
    # Check for empty graph; return empty MST and zero space if no nodes exist
    if not graph.nodes():
        return [], 0

    # Get the number of nodes in the graph for indexing
    num_nodes = graph.number_of_nodes()
    # Initialize adjacency list: each node maps to a list of (neighbor, weight) tuples
    adj_list = [[] for _ in range(num_nodes)]
    # Build adjacency list from graph edges; undirected graph, so add edges both ways
    for u, v, data in graph.edges(data=True):
        adj_list[u].append((v, data['weight']))  # Add edge u -> v with weight
        adj_list[v].append((u, data['weight']))  # Add edge v -> u with same weight

    # Choose starting node as 0 (arbitrary choice for connected graph)
    start_node = 0
    # Track visited nodes to avoid cycles in the MST
    visited = set()
    # Initialize priority queue (min-heap) with a dummy edge: (weight, node, parent)
    # Start with weight 0, node 0, and no parent (None)
    heap = [(0, start_node, None)]
    # Track nodes currently in the heap and their minimum weights for optimization
    in_heap = {start_node: 0}  # Key: node, Value: current minimum weight in heap
    # Store MST edges as list of (parent, child, weight) tuples
    mst = []
    # Track peak number of unique nodes in the heap (size of in_heap)
    max_unique_nodes = 0

    # Process the heap until empty, building the MST
    while heap:
        # Update peak number of unique nodes (size of in_heap)
        max_unique_nodes = max(max_unique_nodes, len(in_heap))
        # Pop the edge with minimum weight: (weight, node, parent)
        weight, u, parent = heappop(heap)
        # Skip if node u has already been visited (avoids cycles)
        if u in visited:
            continue
        # Mark node u as visited
        visited.add(u)
        # Remove node u from in_heap since it’s now processed
        del in_heap[u]
        # If this isn’t the starting node (parent is not None), add edge to MST
        if parent is not None:
            mst.append((parent, u, weight))
        # Explore neighbors of node u
        for v, w in adj_list[u]:
            # Process only unvisited neighbors to avoid cycles
            if v not in visited:
                # Add to heap if v isn’t in heap or if this edge is lighter than v’s current min weight
                if v not in in_heap or w < in_heap[v]:
                    heappush(heap, (w, v, u))  # Add edge (weight, child, parent) to heap
                    in_heap[v] = w  # Update v’s minimum weight in in_heap

    # Calculate space complexity based on peak number of unique nodes (in_heap size)
    heap_entry_size = 80  # Bytes for each heap entry: (weight, u, parent) tuple
    spc_bytes = max_unique_nodes * heap_entry_size  # Total bytes based on unique nodes
    spc_kb = spc_bytes / 1024  # Convert bytes to KB

    # Return the MST and its space complexity in KB
    return mst, spc_kb

# Benchmarking Loop
# Runs Kruskal’s and Prim’s on random dense graphs, averages metrics, and stores results.
for V in nodes:  # Iterate over graph sizes
    kruskal_runtime_runs = []  # Store individual Kruskal runtimes
    prim_runtime_runs = []  # Store individual Prim runtimes
    kruskal_space_runs = []  # Store individual Kruskal space usages
    prim_space_runs = []  # Store individual Prim space usages

    for _ in range(num_runs):  # Repeat for averaging
        # Ensure E doesn’t exceed max possible edges for a simple graph
        max_edges = V * (V - 1) // 2
        E = min(V * V, max_edges)
        G = nx.gnm_random_graph(V, E)  # Generate random graph
        # Ensure the graph is connected
        while not nx.is_connected(G):
            G = nx.gnm_random_graph(V, E, seed=42)  # Retry with seed for consistency
        for (u, v) in G.edges():
            G[u][v]['weight'] = np.random.randint(1, 101)  # Assign random weights

        start_time = time.time()  # Start timer
        mst, parent, rank = kruskal_mst(G)  # Run Kruskal’s
        kruskal_time = (time.time() - start_time) * 1000  # Calculate runtime in ms
        kruskal_runtime_runs.append(kruskal_time)  # Store runtime
        kruskal_space = (sys.getsizeof(parent) + sys.getsizeof(rank)) / 1024  # Space in KB
        kruskal_space_runs.append(kruskal_space)  # Store space

        start_time = time.time()  # Start timer
        mst, prim_spc = prim_mst(G)  # Run Prim’s, get SPC directly
        prim_time = (time.time() - start_time) * 1000  # Calculate runtime in ms
        prim_runtime_runs.append(prim_time)  # Store runtime
        prim_space_runs.append(prim_spc)  # Use the SPC from prim_mst

    kruskal_runtimes_avg.append(np.mean(kruskal_runtime_runs))  # Average Kruskal runtime
    prim_runtimes_avg.append(np.mean(prim_runtime_runs))  # Average Prim runtime
    kruskal_space_avg.append(np.mean(kruskal_space_runs))  # Average Kruskal space
    prim_space_avg.append(np.mean(prim_space_runs))  # Average Prim space

# Output averaged metrics for each graph size
print(f"Averaged Metrics for each graph size (after {num_runs} runs):")
for V, kruskal_time, prim_time, kruskal_space, prim_space in zip(nodes, kruskal_runtimes_avg, prim_runtimes_avg,
                                                                 kruskal_space_avg, prim_space_avg):
    print(f"Nodes: {V}, Kruskal’s Runtime: {kruskal_time:.6f} ms, Prim’s Runtime: {prim_time:.6f} ms, "
          f"Kruskal’s SPC: {kruskal_space:.6f} KB, Prim’s SPC: {prim_space:.6f} KB")

# Plot Runtime Comparison
# Creates side-by-side plots of Kruskal’s and Prim’s runtimes vs. graph size.
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharey=True)  # Two subplots with shared y-axis
ax1.plot(nodes, kruskal_runtimes_avg, label="Kruskal’s", marker='o', color='blue')  # Plot Kruskal’s runtime
ax1.set_title("Kruskal’s Runtime vs. Input Size")  # Set title
ax1.set_xlabel("Number of Nodes")  # X-axis label
ax1.set_ylabel("Runtime (milliseconds)")  # Y-axis label
ax1.grid(True)  # Add grid
ax1.legend()  # Add legend

ax2.plot(nodes, prim_runtimes_avg, label="Prim’s", marker='o', color='green')  # Plot Prim’s runtime
ax2.set_title("Prim’s Runtime vs. Input Size")  # Set title
ax2.set_xlabel("Number of Nodes")  # X-axis label
ax2.grid(True)  # Add grid
ax2.legend()  # Add legend

plt.tight_layout()  # Adjust layout
plt.savefig("runtime_chart.png")  # Save runtime plot
plt.close()  # Close figure

# Plot Space Complexity Comparison
# Creates a single plot comparing Kruskal’s and Prim’s space complexity vs. graph size.
plt.figure(figsize=(8, 6))  # New figure for space plot
plt.plot(nodes, kruskal_space_avg, label="Kruskal’s (Disjoint Set)", marker='o')  # Plot Kruskal’s space
plt.plot(nodes, prim_space_avg, label="Prim’s (Priority Queue)", marker='o')  # Plot Prim’s space
plt.xlabel("Number of Nodes")  # X-axis label
plt.ylabel("Space Complexity (KB)")  # Y-axis label
plt.title("Space Complexity vs. Input Size")  # Set title
plt.legend()  # Add legend
plt.grid(True)  # Add grid
plt.savefig("space_complexity_chart.png")  # Save space plot
plt.close()  # Close figure