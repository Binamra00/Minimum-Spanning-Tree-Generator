# graph_visualizer.py
# Contains the GraphVisualizer class, which handles the visualization of the graph using Matplotlib.
# Renders nodes, edges, and weights, and supports animation by highlighting MST edges.

import matplotlib.pyplot as plt # Library for creating static, animated, and interactive visualizations
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # Backend for embedding Matplotlib in PyQt5
import networkx as nx # Library for creating and manipulating complex networks/graphs

class GraphVisualizer:
    """Class for visualizing the graph in the GUI using Matplotlib."""

    def __init__(self, main_layout):
        """
        Initialize the GraphVisualizer with a Matplotlib canvas.

        Args:
            main_layout (QVBoxLayout): The main layout to add the canvas to.
        """
        # Create a Matplotlib figure and axis (70% height of the window).
        self.figure, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas, stretch=70)

        # Initialize visualization state.
        self.pos = None  # Node positions (set by spring_layout in gui.py).
        self.highlighted_edges = []  # Edges to highlight during animation (MST edges).
        self.is_animation_running = False  # Flag to control edge label color during animation.

    def show_welcome_message(self):
        """Display a welcome message on the canvas when the application starts."""
        self.ax.clear()
        self.ax.axis('off')  # Hide axes for the welcome message.
        self.ax.text(0.5, 0.5, "Welcome!\nHit the 'Generate Graph' button to begin.",
                     fontsize=14, ha='center', va='center', wrap=True)
        self.canvas.draw()

    def plot_graph(self, graph, is_animation_running, large_graph=False, starting_node=None, visited_vertices=None):
        """
        Plot the graph on the canvas, including nodes, edges, and weights.

        Args:
            graph (networkx.Graph): The graph to plot.
            is_animation_running (bool): Whether an animation is currently running.
            large_graph (bool): Whether the graph has more than 27 nodes (affects rendering).
            starting_node (int, optional): The starting node to highlight in light green.
            visited_vertices (list, optional): List of vertices to highlight in light green during animation.
        """
        # Clear the previous plot.
        self.ax.clear()
        self.ax.axis('off')  # Hide axes for the graph.

        # Check if the graph is empty.
        if not graph or graph.number_of_nodes() == 0:
            self.ax.text(0.5, 0.5, "No graph to display.\nGenerate a graph to begin.",
                         fontsize=14, ha='center', va='center', wrap=True)
            self.canvas.draw()
            return

        # Use the fixed layout (self.pos should already be set in gui.py).
        if not self.pos:
            self.pos = nx.spring_layout(graph, k=1.2, iterations=100)

        # Scale positions to use 80% of the canvas width.
        pos_array = {node: list(pos) for node, pos in self.pos.items()}
        x_coords = [pos[0] for pos in pos_array.values()]
        y_coords = [pos[1] for pos in pos_array.values()]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)

        if x_max > x_min and y_max > y_min:
            # Normalize positions to [0, 1].
            for node in pos_array:
                pos_array[node][0] = (pos_array[node][0] - x_min) / (x_max - x_min)
                pos_array[node][1] = (pos_array[node][1] - y_min) / (y_max - y_min)
            # Scale to use 80% of the width and full height.
            for node in pos_array:
                pos_array[node][0] = pos_array[node][0] * 0.8 + 0.1  # Center within 80% of width.
                pos_array[node][1] = pos_array[node][1]  # Already scaled in gui.py.
            self.pos = pos_array

        # Draw all non-MST edges in black.
        non_mst_edges = [(u, v) for u, v in graph.edges() if
                         (u, v) not in self.highlighted_edges and (v, u) not in self.highlighted_edges]
        nx.draw_networkx_edges(graph, self.pos, ax=self.ax, edgelist=non_mst_edges, edge_color='black', alpha=0.6)

        # Draw MST edges in red (highlighted during animation).
        if self.highlighted_edges:
            nx.draw_networkx_edges(graph, self.pos, ax=self.ax, edgelist=self.highlighted_edges, edge_color='red',
                                   width=2,
                                   alpha=1.0)

        # Draw nodes: set colors based on starting node and visited vertices
        node_colors = []
        visited_vertices = visited_vertices or []  # Ensure visited_vertices is a list
        for node in graph.nodes():
            if node in visited_vertices:
                node_colors.append('lightgreen')  # Visited nodes in light green
            else:
                node_colors.append('darkblue' if large_graph else 'lightblue')  # Default color

        # Draw nodes with appropriate size and color
        if large_graph:
            nx.draw_networkx_nodes(graph, self.pos, ax=self.ax, node_color=node_colors,
                                   node_size=50)  # Smaller nodes for large graphs
        else:
            nx.draw_networkx_nodes(graph, self.pos, ax=self.ax, node_color=node_colors, node_size=300)
            nx.draw_networkx_labels(graph, self.pos, ax=self.ax)  # Show labels for small graphs

        # Draw edge labels only for small graphs.
        if not large_graph:
            label_color = 'black' if is_animation_running else '#8B0000'  # Black during animation, deep red otherwise.
            labels = nx.get_edge_attributes(graph, 'weight')
            for (u, v), weight in labels.items():
                x = (self.pos[u][0] + self.pos[v][0]) / 2  # Midpoint x for label position.
                y = (self.pos[u][1] + self.pos[v][1]) / 2  # Midpoint y for label position.
                self.ax.text(x, y, str(weight), fontsize=6, ha='center', va='center',
                             color=label_color,  # Set color dynamically.
                             bbox=dict(facecolor='none', edgecolor='none', alpha=0.0))

        # Set axis limits with minimal padding to use the full canvas.
        x_coords = [pos[0] for pos in self.pos.values()]
        y_coords = [pos[1] for pos in self.pos.values()]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_padding = (x_max - x_min) * 0.05  # 5% padding on each side.
        y_padding = (y_max - y_min) * 0.05  # 5% padding on each side.
        self.ax.set_xlim(x_min - x_padding, x_max + x_padding)
        self.ax.set_ylim(y_min - y_padding, y_max + y_padding)

        # Redraw the canvas.
        self.canvas.draw()