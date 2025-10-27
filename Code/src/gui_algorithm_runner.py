# gui_algorithm_runner.py
# Defines the AlgorithmRunner class for managing MST algorithm execution and animation.
# Coordinates with MSTAnimation to run algorithms and animate the results in the GUI.

from PyQt5.QtWidgets import QMessageBox # PyQt5 module for displaying message boxes in the GUI
from mst_animation import MSTAnimation # Custom animation wrapper for MST algorithm visualization

class AlgorithmRunner:
    def __init__(self, parent):
        # Initialize with reference to the main GUI window
        self.parent = parent  # Reference to MSTWindow instance
        self.animation_steps = []  # Store animation steps for playback
        self.current_step = 0  # Track current step in animation
        self.mst_edges = None  # Store final MST edges
        self.metrics = None  # Store performance metrics
        self.starting_node = None  # Track starting node for visualization
        self.visited_vertices = []  # Track visited vertices for highlighting
        self.sub_step = 0  # Track sub-step (0 for vertices, 1 for edges)

    def run_algorithm(self):
        # Execute the selected MST algorithm and prepare for animation
        if self.parent.is_animation_running:
            return  # Exit if animation is already running

        # Validate graph existence
        if not self.parent.gm.get_graph():
            QMessageBox.warning(self.parent, "Error", "Please generate a graph first!")
            return
        # Validate weights existence
        if not self.parent.gm.has_weights():
            QMessageBox.warning(self.parent, "Error", "Please either input the weights manually or hit the 'Assign Weights' button, then run the algorithm.")
            return

        self.parent.is_animation_running = True  # Mark animation as running
        self.parent.set_controls_enabled(False)  # Disable controls during animation

        # Initialize MST computation and animation objects
        self.parent.weight_manager.mst = self.parent.mst_class(self.parent.gm.get_graph())
        animator = MSTAnimation(self.parent.weight_manager.mst)  # Wrap MST for animation
        algo = self.parent.algo_combo.currentText()  # Get selected algorithm
        # Select appropriate animation generator
        gen = animator.kruskal_mst_with_animation() if algo == "Kruskal’s" else animator.prim_mst_with_animation()

        # Reset animation state
        self.animation_steps = []
        self.current_step = 0
        self.sub_step = 0
        self.starting_node = None
        self.visited_vertices = []
        self.parent.visualizer.highlighted_edges = []

        # Process the generator to collect steps and results
        steps, (mst_edges, error) = self.run_algorithm_generator(gen, algo)
        if error:
            QMessageBox.warning(self.parent, "Error", error)  # Show error if present
            self.parent.is_animation_running = False
            self.parent.set_controls_enabled(True)
            return

        self.animation_steps = steps  # Store animation steps
        self.mst_edges = mst_edges  # Store MST edges
        self.metrics = self.parent.weight_manager.mst.get_metrics()  # Get metrics from computation

        # Start animation if steps exist
        if self.animation_steps:
            if self.parent.large_graph:
                self.parent.timer.start(0)  # Instant animation for large graphs
            else:
                self.parent.timer.start(250)  # 0.25-second delay for small graphs
        else:
            # Update table immediately if no animation steps
            self.parent.table_manager.update_table(algo, self.mst_edges, self.metrics, self.parent.weight_manager.calculate_mst_weight)
            self.parent.is_animation_running = False
            self.parent.set_controls_enabled(True)

    def animate_step(self):
        # Animate the current step in the MST construction
        if self.current_step < len(self.animation_steps):
            # Process the current animation step
            step_type, step_data = self.animation_steps[self.current_step]

            if self.sub_step == 0:
                # First sub-step: Highlight vertices
                if step_type == 'vertex':
                    if step_data not in self.visited_vertices:
                        self.visited_vertices.append(step_data)  # Add vertex to visited list
                # Plot graph with updated vertices
                self.parent.visualizer.plot_graph(
                    self.parent.gm.get_graph(),
                    self.parent.is_animation_running,
                    self.parent.large_graph,
                    self.starting_node,
                    self.visited_vertices
                )
                self.sub_step = 1  # Move to edge sub-step
            else:
                # Second sub-step: Highlight edges
                if step_type == 'edge':
                    self.parent.visualizer.highlighted_edges.append(step_data)  # Add edge to highlighted list
                # Plot graph with updated edges
                self.parent.visualizer.plot_graph(
                    self.parent.gm.get_graph(),
                    self.parent.is_animation_running,
                    self.parent.large_graph,
                    self.starting_node,
                    self.visited_vertices
                )
                self.sub_step = 0  # Reset sub-step
                self.current_step += 1  # Move to next step
        else:
            # Animation complete, finalize visualization
            self.visited_vertices = [self.starting_node] if self.starting_node is not None else []  # Keep only starting node
            self.parent.visualizer.plot_graph(
                self.parent.gm.get_graph(),
                self.parent.is_animation_running,
                self.parent.large_graph,
                self.starting_node,
                self.visited_vertices
            )
            self.parent.timer.stop()  # Stop animation timer
            algo = self.parent.algo_combo.currentText()
            # Update table with final results
            self.parent.table_manager.update_table(algo, self.mst_edges, self.metrics, self.parent.weight_manager.calculate_mst_weight)
            self.parent.is_animation_running = False
            self.parent.set_controls_enabled(True)  # Re-enable controls

    def run_algorithm_generator(self, algorithm_gen, algo):
        # Process the MST animation generator to collect steps and final result
        steps = []  # Store animation steps
        first_edge_processed = False  # Track first edge for Kruskal’s starting node
        try:
            while True:
                item = next(algorithm_gen)  # Get next animation step
                if isinstance(item, tuple) and len(item) == 2:
                    step_type, step_data = item
                    if step_type == 'edge' and isinstance(step_data, tuple) and len(step_data) == 2:
                        # Set starting node for Kruskal’s from first edge
                        if algo == "Kruskal’s" and not first_edge_processed:
                            self.starting_node = step_data[0]  # First node of first edge
                            first_edge_processed = True
                        steps.append(item)  # Add edge step
                    elif step_type == 'vertex':
                        steps.append(item)  # Add vertex step
                    elif step_type == 'final':
                        # Set starting node for Prim’s if steps exist
                        if algo == "Prim’s" and steps:
                            self.starting_node = 0  # Prim’s starts at node 0
                        return steps, step_data  # Return steps and final result
        except StopIteration as e:
            # Handle unexpected termination
            if algo == "Prim’s" and steps:
                self.starting_node = 0  # Ensure Prim’s starting node is set
            return steps, e.value if hasattr(e, 'value') and e.value is not None else ([], "Unexpected termination")