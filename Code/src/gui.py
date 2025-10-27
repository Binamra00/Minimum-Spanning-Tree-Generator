# gui.py
# Defines the MSTWindow superclass, the main GUI for the MST visualization project.
# Sets up the window, widgets, and layout, and delegates functionality to subclasses.

from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QComboBox, QMessageBox, QLineEdit, QLabel, QHBoxLayout  # PyQt5 widgets for GUI components and layouts
from PyQt5.QtCore import Qt, QTimer # PyQt5 core module for alignment, flags, and timer functionality
from gui_graph_visualizer import GraphVisualizer # Custom class for rendering graph visualizations
from gui_table_manager import TableManager # Custom class for managing the comparison table
from gui_input_handler import InputHandler # Custom class for parsing user input
from gui_graph_handler import GraphHandler # Custom class for generating and managing graphs
from gui_algorithm_runner import AlgorithmRunner # Custom class for running MST algorithms and animations
from gui_weight_manager import WeightManager # Custom class for assigning and calculating weights
from gui_reset_handler import ResetHandler # Custom class for resetting the application state

class MSTWindow(QMainWindow):
    def __init__(self, graph_manager, mst_algorithms):
        super().__init__()
        self.setWindowTitle("MST Project")
        self.setGeometry(100, 100, 1000, 600)

        # Dependencies
        self.gm = graph_manager
        self.mst_class = mst_algorithms

        # Animation state (shared across subclasses)
        self.is_animation_running = False
        self.timer = QTimer(self)

        # Flag to track if the graph has more than 27 nodes
        self.large_graph = False

        # GUI layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Initialize components
        self.visualizer = GraphVisualizer(self.main_layout)
        self.bottom_layout = QHBoxLayout()
        self.main_layout.addLayout(self.bottom_layout, stretch=30)
        self.table_manager = TableManager(self.bottom_layout)
        self.input_handler = InputHandler()

        # Left section: Controls (inputs, dropdown, buttons) - 35% width
        self.controls_widget = QWidget()
        self.controls_layout = QVBoxLayout(self.controls_widget)
        self.controls_layout.setAlignment(Qt.AlignCenter)

        # Input fields
        self.nodes_label = QLabel("Number of Nodes (1-500, optional):")
        self.controls_layout.addWidget(self.nodes_label)
        self.nodes_input = QLineEdit()
        self.nodes_input.setPlaceholderText("e.g., 5")
        self.controls_layout.addWidget(self.nodes_input)

        self.edges_label = QLabel("Edges with Weights (optional, e.g., (1,2,19),(2,3,15)):")
        self.controls_layout.addWidget(self.edges_label)
        self.edges_input = QLineEdit()
        self.edges_input.setPlaceholderText("e.g., (1,2,19),(2,3,15)")
        self.controls_layout.addWidget(self.edges_input)

        # Buttons and dropdown
        self.gen_button = QPushButton("Generate Graph")
        self.weight_button = QPushButton("Assign Weights")
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["Kruskal’s", "Prim’s"])
        self.run_button = QPushButton("Run Algorithm")
        self.clear_button = QPushButton("Clear")

        # Initialize subclasses and connect buttons
        self.graph_handler = GraphHandler(self)
        self.algorithm_runner = AlgorithmRunner(self)
        self.weight_manager = WeightManager(self)
        self.reset_handler = ResetHandler(self)

        # Connect buttons to subclass methods
        self.gen_button.clicked.connect(self.graph_handler.generate_graph)
        self.weight_button.clicked.connect(self.weight_manager.assign_weights)
        self.run_button.clicked.connect(self.algorithm_runner.run_algorithm)
        self.clear_button.clicked.connect(self.reset_handler.clear_application)
        self.timer.timeout.connect(self.algorithm_runner.animate_step)

        # Add widgets to layout
        self.controls_layout.addWidget(self.gen_button)
        self.controls_layout.addWidget(self.weight_button)
        self.controls_layout.addWidget(self.algo_combo)
        self.controls_layout.addWidget(self.run_button)
        self.controls_layout.addWidget(self.clear_button)
        self.bottom_layout.addWidget(self.controls_widget, stretch=35)

        self.visualizer.show_welcome_message()

    def set_controls_enabled(self, enabled):
        # Enable or disable all interactive controls during animation
        self.gen_button.setEnabled(enabled)
        self.weight_button.setEnabled(enabled)
        self.algo_combo.setEnabled(enabled)  # Disable/enable the dropdown
        self.run_button.setEnabled(enabled)  # Disable/enable the Run Algorithm button
        self.clear_button.setEnabled(enabled)