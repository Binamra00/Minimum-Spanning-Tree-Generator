# gui_table_manager.py
# Defines the TableManager class for managing the comparison table in the GUI.
# Displays MST results, runtime, weights, and graph edges.

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem # PyQt5 widgets for creating and managing tables
from PyQt5.QtCore import Qt # PyQt5 core module for alignment and item flags

class TableManager:
    def __init__(self, bottom_layout):
        # Initialize the table with 7 rows and 3 columns (added Total Nodes row)
        self.table = QTableWidget()
        self.table.setRowCount(7)  # Rows: Header, MST Edges, Runtime, Total Weight, MST Weight, Total Nodes, Graph
        self.table.setColumnCount(3)  # Columns: Metric, Kruskal’s, Prim’s
        self.table.setHorizontalHeaderLabels(["", "Kruskal’s", "Prim’s"])
        self.table.verticalHeader().setVisible(False)  # Hide vertical header labels
        # Disable editing on the table
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        # Set metric names in the first column
        self.table.setItem(1, 0, QTableWidgetItem("MST Edges"))
        self.table.setItem(2, 0, QTableWidgetItem("Runtime (ms)"))  # Updated to milliseconds
        self.table.setItem(3, 0, QTableWidgetItem("Total Weight"))
        self.table.setItem(4, 0, QTableWidgetItem("MST Weight"))
        self.table.setItem(5, 0, QTableWidgetItem("Total Nodes"))
        self.table.setItem(6, 0, QTableWidgetItem("Graph"))
        # Make Metric column items read-only and left-justify
        for row in range(1, self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Remove editable flag
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # Merge the "Kruskal’s" and "Prim’s" columns in the "Total Nodes" and "Graph" rows
        self.table.setSpan(5, 1, 1, 2)  # Span row 5 (Total Nodes), column 1 across 2 columns
        self.table.setSpan(6, 1, 1, 2)  # Span row 6 (Graph), column 1 across 2 columns
        # Adjust column widths for better readability
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, header.Fixed)
        self.table.setColumnWidth(0, 120)  # Fixed width for Metric column
        header.setSectionResizeMode(1, header.Stretch)
        header.setSectionResizeMode(2, header.Stretch)
        # Set header row height to 10px (reduced from 14px to make space)
        self.table.verticalHeader().setSectionResizeMode(0, header.Fixed)
        self.table.verticalHeader().resizeSection(0, 10)
        # Apply custom styling for padding
        self.table.setStyleSheet("""
            QHeaderView::section {
                padding: 2px;
            }
            QTableWidget::item {
                padding-left: 2px;
            }
        """)
        # Stretch content rows to fill table height
        vertical_header = self.table.verticalHeader()
        for row in range(1, self.table.rowCount()):
            vertical_header.setSectionResizeMode(row, vertical_header.Stretch)
        bottom_layout.addWidget(self.table, stretch=65)

    def clear_table(self):
        # Clear all cells except the Metric column (column 0)
        for row in range(1, self.table.rowCount()):
            for col in range(1, self.table.columnCount()):
                self.table.setItem(row, col, None)
        # Reset metric names in the first column
        self.table.setItem(1, 0, QTableWidgetItem("MST Edges"))
        self.table.setItem(2, 0, QTableWidgetItem("Runtime (ms)"))  # Updated to milliseconds
        self.table.setItem(3, 0, QTableWidgetItem("Total Weight"))
        self.table.setItem(4, 0, QTableWidgetItem("MST Weight"))
        self.table.setItem(5, 0, QTableWidgetItem("Total Nodes"))
        self.table.setItem(6, 0, QTableWidgetItem("Graph"))
        # Reapply left alignment and read-only for Metric column
        for row in range(1, self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Remove editable flag
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def update_table(self, algo, mst_edges, metrics, calculate_mst_weight):
        col = 1 if algo == "Kruskal’s" else 2  # Select column based on algorithm
        # MST Edges
        item = QTableWidgetItem(str(mst_edges))
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
        self.table.setItem(1, col, item)
        # Runtime
        item = QTableWidgetItem(f"{metrics['runtime']:.6f}")
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
        self.table.setItem(2, col, item)
        # MST Weight
        mst_weight = calculate_mst_weight(mst_edges)
        item = QTableWidgetItem(str(mst_weight))
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
        self.table.setItem(4, col, item)

    def update_graph_row(self, graph, has_weights):
        # Handle special cases for empty or unweighted graphs
        if not graph or graph.number_of_nodes() == 0:
            item = QTableWidgetItem("No graph")
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(6, 1, item)  # Update row 6 (Graph)
            return
        if graph.number_of_edges() == 0:
            item = QTableWidgetItem("No edges")
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(6, 1, item)  # Update row 6 (Graph)
            return
        if not has_weights:
            edges = [(u, v) for u, v in graph.edges()]
            item = QTableWidgetItem(str(edges))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(6, 1, item)  # Update row 6 (Graph)
            return
        edges = [(u, v, graph[u][v]['weight']) for u, v in graph.edges()]
        item = QTableWidgetItem(str(edges))
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.table.setItem(6, 1, item)  # Update row 6 (Graph)

    def update_total_weight(self, total_weight):
        # Update total weight for both Kruskal’s and Prim’s columns
        item1 = QTableWidgetItem(str(total_weight))
        item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)  # Make read-only
        self.table.setItem(3, 1, item1)
        item2 = QTableWidgetItem(str(total_weight))
        item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)  # Make read-only
        self.table.setItem(3, 2, item2)

    def update_total_nodes(self, graph):
        # Update the Total Nodes row with the number of nodes in the graph
        if not graph or graph.number_of_nodes() == 0:
            item = QTableWidgetItem("0")
        else:
            item = QTableWidgetItem(str(graph.number_of_nodes()))
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.table.setItem(5, 1, item)  # Update row 5 (Total Nodes)