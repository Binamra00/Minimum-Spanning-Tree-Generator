# mst_project.py
# Main entry point for the Minimum Spanning Tree (MST) visualization project.
# This script sets up the application, initializes core components, and launches the GUI.

import sys # Module for accessing system-specific parameters and functions
from PyQt5.QtWidgets import QApplication # PyQt5 module for creating the application and managing GUI events
from graph_manager import GraphManager # Custom class for generating and managing graphs
from mst_algorithms import MSTAlgorithms # Custom class for computing MSTs using Kruskal's and Prim's algorithms
from gui import MSTWindow # Custom GUI class for the main application window

def main():
    """Initialize and run the MST visualization application."""
    app = QApplication(sys.argv)  # Create a Qt application instance to manage the GUI event loop.
    gm = GraphManager()  # Initialize the GraphManager to manage graph creation and weight assignment.
    window = MSTWindow(gm, MSTAlgorithms)  # Create the main GUI window, passing GraphManager and MSTAlgorithms class.
    window.show()  # Display the GUI window to the user.
    sys.exit(app.exec_())  # Start the application event loop and exit when the window is closed.

if __name__ == "__main__":
    # Check if the script is run directly (not imported as a module) and call the main function.
    main()