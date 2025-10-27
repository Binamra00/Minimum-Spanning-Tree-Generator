# gui_reset_handler.py
# Defines the ResetHandler subclass for managing the application reset functionality.

class ResetHandler:
    def __init__(self, parent):
        self.parent = parent  # Reference to MSTWindow instance

    def clear_application(self):
        """Reset the application to its initial state, showing the welcome screen."""
        if self.parent.is_animation_running:
            return

        # If no graph exists yet, just return and keep the app as-is
        graph = self.parent.gm.get_graph()
        if graph is None:
            return

        # Stop any running animation
        self.parent.timer.stop()
        self.parent.is_animation_running = False

        # Clear the graph and reset state variables
        graph.clear()
        self.parent.weight_manager.mst = None
        self.parent.weight_manager.total_graph_weight = 0
        self.parent.large_graph = False
        self.parent.algorithm_runner.animation_steps = []
        self.parent.algorithm_runner.current_step = 0
        self.parent.algorithm_runner.mst_edges = None
        self.parent.algorithm_runner.metrics = None
        self.parent.visualizer.highlighted_edges = []
        self.parent.visualizer.pos = None

        # Clear input fields
        self.parent.nodes_input.clear()
        self.parent.edges_input.clear()

        # Clear the table and show the welcome message
        self.parent.table_manager.clear_table()
        self.parent.visualizer.show_welcome_message()

        # Re-enable all buttons
        self.parent.gen_button.setEnabled(True)
        self.parent.weight_button.setEnabled(True)
        self.parent.clear_button.setEnabled(True)