# gui_input_handler.py
# Defines the InputHandler class for parsing and validating user input for graph edges.

class InputHandler:
    def parse_edges_input(self, edges_text, num_nodes):
        if not edges_text:
            return None
        try:
            # Parse edges by removing whitespace and splitting on "),('"
            edges = edges_text.replace(" ", "").split("),(")
            edges[0] = edges[0].lstrip("(")  # Remove leading parenthesis from first edge
            edges[-1] = edges[-1].rstrip(")")  # Remove trailing parenthesis from last edge
            edge_list = []
            for edge in edges:
                parts = edge.split(",")
                if len(parts) != 3 and len(parts) != 2:
                    raise ValueError("Each edge must be in the format (u,v) or (u,v,weight)")
                u, v = int(parts[0]), int(parts[1])
                # Validate node indices against the number of nodes
                if not (0 <= u < num_nodes and 0 <= v < num_nodes):
                    raise ValueError(f"Node indices must be between 0 and {num_nodes - 1}")
                if len(parts) == 3:
                    weight = int(parts[2])
                    if weight <= 0:
                        raise ValueError("Edge weights must be positive integers")
                    edge_list.append((u, v, weight))
                else:
                    edge_list.append((u, v))
            return edge_list
        except ValueError as e:
            # Re-raise specific validation errors or raise a generic format error
            if str(e).startswith("Node indices") or str(e).startswith("Edge weights"):
                raise
            raise ValueError("Invalid edge format. Use (u,v) or (u,v,weight), e.g., (1,2,19),(2,3,15)")