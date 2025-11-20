MST Visualization Project README
===============================

Overview
--------
This project is a Python-based desktop application for visualizing Minimum Spanning Trees (MSTs) using Kruskal's and Prim's algorithms. It features a GUI built with PyQt5, allowing users to generate graphs, assign weights, run MST algorithms, and view results with animations.

Requirements
------------
- Python 3.6 or higher
- Required libraries:
  - PyQt5
  - networkx
  - matplotlib
  - numpy
  - scipy

Installation
------------
1. Clone or download the project repository.
2. Install the required libraries using pip:
   pip install PyQt5 networkx matplotlib numpy
3. Ensure all project files are in the same directory (`src/`):
- `mst_project.py`
- `gui.py`
- `gui_graph_handler.py`
- `gui_algorithm_runner.py`
- `gui_weight_manager.py`
- `gui_reset_handler.py`
- `gui_graph_visualizer.py`
- `gui_table_manager.py`
- `gui_input_handler.py`
- `graph_manager.py`
- `mst_algorithms.py`
- `mst_animation.py`
- `combined_metrics_chart.py`

Running the Application
-----------------------
1. Navigate to the project directory:
   cd path/to/project/src
2. Run the main script:
   python mst_project.py
3. The GUI will open, allowing you to:
   - Generate a random or custom graph.
   - Assign weights to edges.
   - Run Kruskal's or Prim's algorithm with animation.
   - View results in a comparison table.
   - Reset the application using the "Clear" button.

Documentation
-------------
- Code Documentation: See Code Documentation.html
- Data and Control Flow: See Data and Control Flow.html
- User Interaction Flow: See User Interaction Flow.html and User Instructions.html
- Project Report: See Project Report.html

For more details, refer to the documentation files.
