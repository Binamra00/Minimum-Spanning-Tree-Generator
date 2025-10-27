# mst_animation.py
# Defines the MSTAnimation class for generating animation steps for MST algorithms.
# Wraps the pure computation from MSTAlgorithms to provide visualization steps without affecting runtime metrics.

class MSTAnimation:
    def __init__(self, mst_algorithms_instance):
        # Initialize with an instance of MSTAlgorithms
        self.mst = mst_algorithms_instance  # Reference to the MST computation object

    def kruskal_mst_with_animation(self):
        # Generate animation steps for Kruskal's MST algorithm
        # Run the pure computation first
        mst_edges, error = self.mst.kruskal_mst()
        if error:
            yield ('final', ([], error))  # Yield empty result with error if computation failed
            return

        # Generate animation steps based on the computed MST
        visited_vertices = set()  # Track visited vertices for vertex highlighting
        for u, v, weight in mst_edges:
            if u not in visited_vertices:
                visited_vertices.add(u)  # Add new vertex to visited set
                yield ('vertex', u)  # Yield vertex for animation
            if v not in visited_vertices:
                visited_vertices.add(v)  # Add new vertex to visited set
                yield ('vertex', v)  # Yield vertex for animation
            yield ('edge', (u, v))  # Yield edge for animation

        yield ('final', (mst_edges, None))  # Yield final MST edges with no error

    def prim_mst_with_animation(self):
        # Generate animation steps for Prim's MST algorithm
        # Run the pure computation first
        mst_edges, error = self.mst.prim_mst()
        if error:
            yield ('final', ([], error))  # Yield empty result with error if computation failed
            return

        # Generate animation steps based on the computed MST
        visited_vertices = set()  # Track visited vertices for vertex highlighting
        start_node = 0  # Prim's starts at node 0 (consistent with mst_algorithms.py)
        visited_vertices.add(start_node)
        yield ('vertex', start_node)  # Yield starting vertex for animation

        for parent, u, weight in mst_edges:
            if u not in visited_vertices:
                visited_vertices.add(u)  # Add new vertex to visited set
                yield ('vertex', u)  # Yield vertex for animation
            yield ('edge', (parent, u))  # Yield edge for animation

        yield ('final', (mst_edges, None))  # Yield final MST edges with no error