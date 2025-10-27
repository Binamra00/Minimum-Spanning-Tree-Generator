# gui_graph_handler.py
# Defines the GraphHandler subclass for managing graph generation and layout computation.

import networkx as nx # Library for creating and manipulating complex networks/graphs
import numpy as np # Library for numerical operations and array manipulations
import random # Module for generating random numbers and making random selections
from PyQt5.QtWidgets import QMessageBox # PyQt5 module for displaying message boxes in the GUI

class GraphHandler:
    def __init__(self, parent):
        self.parent = parent  # Reference to MSTWindow instance

    def generate_graph(self):
        if self.parent.is_animation_running:
            return

        self.parent.table_manager.clear_table()
        self.parent.visualizer.highlighted_edges = []

        nodes_text = self.parent.nodes_input.text().strip()
        user_nodes = None
        if nodes_text:
            try:
                user_nodes = int(nodes_text)
                if not (1 <= user_nodes <= 500):
                    raise ValueError("Number of nodes must be between 1 and 500")
            except ValueError as e:
                if str(e).startswith("Number of nodes"):
                    QMessageBox.warning(self.parent, "Error", str(e))
                else:
                    QMessageBox.warning(self.parent, "Error", "Number of nodes must be a valid integer")
                return

        self.parent.large_graph = user_nodes is not None and user_nodes > 27

        edges_text = self.parent.edges_input.text().strip()
        user_edges = None
        if edges_text:
            if user_nodes is None:
                QMessageBox.warning(self.parent, "Error", "Please specify the number of nodes before entering edges")
                return
            try:
                user_edges = self.parent.input_handler.parse_edges_input(edges_text, user_nodes)
            except ValueError as e:
                QMessageBox.warning(self.parent, "Error", str(e))
                return

        try:
            # Generate a random graph with 5 to 27 edges if user_edges is None
            self.parent.gm.generate_random_graph((5, 27), user_nodes=user_nodes, user_edges=user_edges)
            G = self.parent.gm.get_graph()
            num_nodes = G.number_of_nodes()
            # Adjust k for spring_layout to improve node distribution
            k = 0.5 / (num_nodes ** 0.5)  # Scales with the number of nodes for better spread
            if self.parent.large_graph:
                # Use random initial positions for large graphs to avoid edge clustering
                init_pos = {node: (random.uniform(0, 1), random.uniform(0, 1)) for node in G.nodes()}
                self.parent.visualizer.pos = nx.spring_layout(G, k=k, iterations=75, pos=init_pos)
                # Post-process positions to reduce edge clustering and fill the center
                pos_array = np.array(list(self.parent.visualizer.pos.values()))
                if len(pos_array) > 0:
                    x_min, x_max = pos_array[:, 0].min(), pos_array[:, 0].max()
                    y_min, y_max = pos_array[:, 1].min(), pos_array[:, 1].max()
                    if x_max > x_min and y_max > y_min:
                        pos_array[:, 0] = (pos_array[:, 0] - x_min) / (x_max - x_min)
                        pos_array[:, 1] = (pos_array[:, 1] - y_min) / (y_max - y_min)
                        center = np.array([0.5, 0.5])
                        for i in range(len(pos_array)):
                            pos_array[i] = center + 0.8 * (pos_array[i] - center)  # Pull nodes toward the center
                        for i, node in enumerate(self.parent.visualizer.pos.keys()):
                            self.parent.visualizer.pos[node] = (pos_array[i, 0], pos_array[i, 1])
            else:
                # Use circular layout for small graphs and more iterations for better layout
                init_pos = nx.circular_layout(G)
                self.parent.visualizer.pos = nx.spring_layout(G, k=k, iterations=100, pos=init_pos)
                pos_array = np.array(list(self.parent.visualizer.pos.values()))
                if len(pos_array) > 0:
                    x_min, x_max = pos_array[:, 0].min(), pos_array[:, 0].max()
                    y_min, y_max = pos_array[:, 1].min(), pos_array[:, 1].max()
                    if x_max > x_min and y_max > y_min:
                        pos_array[:, 0] = (pos_array[:, 0] - x_min) / (x_max - x_min)
                        pos_array[:, 1] = (pos_array[:, 1] - y_min) / (y_max - y_min)
                        pos_array[:, 1] = pos_array[:, 1] ** 0.7  # Stretch y-coordinates for better top spacing
                        for i, node in enumerate(self.parent.visualizer.pos.keys()):
                            self.parent.visualizer.pos[node] = (pos_array[i, 0], pos_array[i, 1])
            self.parent.weight_manager.mst = None
            # Update the Total Nodes row with the number of nodes in the graph
            self.parent.table_manager.update_total_nodes(G)
            if self.parent.gm.has_weights():
                self.parent.weight_manager.mst = self.parent.mst_class(self.parent.gm.get_graph())
                self.parent.weight_manager.total_graph_weight = self.parent.weight_manager.calculate_total_graph_weight()
                self.parent.table_manager.update_total_weight(self.parent.weight_manager.total_graph_weight)
            self.parent.table_manager.update_graph_row(G, self.parent.gm.has_weights())
            self.parent.visualizer.plot_graph(G, self.parent.is_animation_running, self.parent.large_graph)
        except ValueError as e:
            QMessageBox.warning(self.parent, "Error", str(e))