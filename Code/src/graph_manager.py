# graph_manager.py
# Defines the GraphManager class for generating and managing graphs.
# Handles random graph generation, user-specified edges, and weight assignment.

import networkx as nx # Library for creating and manipulating complex networks/graphs
import random # Module for generating random numbers and making random selections

class GraphManager:
    def __init__(self):
        self.graph = None  # Initialize graph as None

    def generate_random_graph(self, num_nodes_range=(1, 100), user_nodes=None, user_edges=None):
        # Determine the number of nodes to use
        if user_nodes is not None:
            num_nodes = user_nodes
        else:
            num_nodes = random.randint(num_nodes_range[0], num_nodes_range[1])

        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(num_nodes))  # Add nodes labeled 0 to num_nodes-1

        if user_edges:
            # Add user-specified edges with weights and validate
            for u, v, w in user_edges:
                if not (0 <= u < num_nodes and 0 <= v < num_nodes):
                    raise ValueError(f"Nodes {u} or {v} are out of range for {num_nodes} nodes (0 to {num_nodes-1})")
                if w <= 0:
                    raise ValueError(f"Weight {w} must be positive")
                self.graph.add_edge(u, v, weight=w)
        else:
            # Ensure the graph is connected by creating a chain structure
            for i in range(1, num_nodes):
                self.graph.add_edge(i-1, i)

            # Add extra random edges to increase connectivity (50% more than V-1)
            extra_edges = int(num_nodes * 0.5)
            for _ in range(extra_edges):
                u, v = random.sample(range(num_nodes), 2)  # Select two distinct nodes
                if not self.graph.has_edge(u, v):
                    self.graph.add_edge(u, v)

    def assign_random_weights(self, weight_range=(1, 100)):
        if not self.graph:
            raise ValueError("Generate a graph first!")
        # Assign random weights to all edges, overwriting any existing weights
        for u, v in self.graph.edges():
            weight = random.randint(weight_range[0], weight_range[1])
            self.graph[u][v]['weight'] = weight

    def is_connected(self):
        # Check if the graph is connected using networkx
        return nx.is_connected(self.graph) if self.graph else False

    def get_graph(self):
        return self.graph

    def has_weights(self):
        # Verify that all edges have a 'weight' attribute
        return all('weight' in self.graph[u][v] for u, v in self.graph.edges())