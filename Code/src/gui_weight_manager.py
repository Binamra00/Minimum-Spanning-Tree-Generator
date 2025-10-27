# gui_weight_manager.py
# Defines the WeightManager subclass for managing weight assignment and calculations.

from PyQt5.QtWidgets import QMessageBox # PyQt5 module for displaying message boxes in the GUI

class WeightManager:
    def __init__(self, parent):
        self.parent = parent  # Reference to MSTWindow instance
        self.mst = None
        self.total_graph_weight = 0

    def calculate_total_graph_weight(self):
        G = self.parent.gm.get_graph()
        if not G or not self.parent.gm.has_weights():
            return 0
        # Sum the weights of all edges in the graph
        total_weight = sum(data['weight'] for u, v, data in G.edges(data=True))
        return total_weight

    def calculate_mst_weight(self, mst_edges):
        if not mst_edges:
            return 0
        # Sum the weights of the MST edges
        return sum(weight for u, v, weight in mst_edges)

    def assign_weights(self):
        if self.parent.is_animation_running:
            return

        try:
            self.parent.gm.assign_random_weights()
            self.mst = self.parent.mst_class(self.parent.gm.get_graph())
            self.total_graph_weight = self.calculate_total_graph_weight()
            self.parent.table_manager.clear_table()
            self.parent.table_manager.update_total_weight(self.total_graph_weight)
            self.parent.table_manager.update_graph_row(self.parent.gm.get_graph(), self.parent.gm.has_weights())
            # Add this line to repopulate the Total Nodes row
            self.parent.table_manager.update_total_nodes(self.parent.gm.get_graph())
            self.parent.visualizer.highlighted_edges = []
            self.parent.visualizer.plot_graph(self.parent.gm.get_graph(), self.parent.is_animation_running, self.parent.large_graph)
        except ValueError as e:
            QMessageBox.warning(self.parent, "Error", str(e))