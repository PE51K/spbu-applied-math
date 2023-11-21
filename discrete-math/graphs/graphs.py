import numpy as np
from typing import Dict, List, Iterable
from itertools import chain, combinations
import unittest
from collections import deque


class Graph:
    def __init__(self, num_vertices: int, edges: np.array = None, original_indices: Iterable = None) -> None:
        if num_vertices <= 0:
            raise ValueError("Number of vertices must be a positive integer")
        self.num_vertices = num_vertices
        if edges is None:
            self.edges = np.zeros((num_vertices, num_vertices), dtype=int)
        else:
            if edges.shape != (num_vertices, num_vertices):
                raise ValueError("Edges matrix shape does not match the number of vertices")
            self.edges = edges

        if original_indices is None:
            self.original_indices = np.arange(num_vertices)
        else:
            self.original_indices = original_indices

    def add_edge(self, vertex1: int, vertex2: int) -> None:
        if 0 <= vertex1 < len(self.edges) and 0 <= vertex2 < len(self.edges):
            self.edges[vertex1, vertex2] = 1
            self.edges[vertex2, vertex1] = 1
        else:
            raise ValueError("Invalid vertex indices")

    def remove_edge(self, vertex1: int, vertex2: int) -> None:
        if 0 <= vertex1 < len(self.edges) and 0 <= vertex2 < len(self.edges):
            self.edges[vertex1, vertex2] = 0
            self.edges[vertex2, vertex1] = 0
        else:
            raise ValueError("Invalid vertex indices")

    def get_subgraph(self, subgraph_vertices: Iterable) -> "Graph":
        subgraph_size = len(subgraph_vertices)
        subgraph_edges = np.zeros((subgraph_size, subgraph_size), dtype=int)

        for i in range(subgraph_size):
            for j in range(subgraph_size):
                subgraph_edges[i, j] = self.edges[subgraph_vertices[i], subgraph_vertices[j]]

        subgraph = Graph(
            subgraph_size, 
            subgraph_edges,
            [self.original_indices[i] for i in subgraph_vertices],
            )

        return subgraph

    def find_all_induced_subgraphs(self, vertices):
        all_subgraphs = []

        for r in range(1, len(vertices) + 1):
            for subset in combinations(vertices, r):
                subgraph = self.get_subgraph(subset)
                if is_valid_induced_subgraph(self, subgraph):
                    all_subgraphs.append(subgraph)

        return all_subgraphs

    def intersection(self, other_graph: "Graph") -> "Graph":
        new_edges = np.logical_and(self.edges, other_graph.edges)
        return Graph(new_edges.shape[0], new_edges)
    
    def union(self, other_graph: "Graph") -> "Graph":
        new_edges = np.logical_or(self.edges, other_graph.edges)
        return Graph(new_edges.shape[0], new_edges)

    def connection(self, other_graph: "Graph") -> "Graph":
        new_num_vertices = self.num_vertices + other_graph.num_vertices
        new_edges = np.zeros((new_num_vertices, new_num_vertices), dtype=int)
        new_edges[:self.num_vertices, :self.num_vertices] = self.edges
        new_edges[self.num_vertices:, self.num_vertices:] = other_graph.edges
        new_edges[:self.num_vertices, other_graph.num_vertices:] = 1
        new_edges[other_graph.num_vertices:, :self.num_vertices] = 1
        return Graph(new_num_vertices, new_edges)
    
    def complement(self) -> "Graph":
        new_edges = 1 - self.edges
        for i in range(len(new_edges)):
            new_edges[i, i] = 0
        return Graph(new_edges.shape[0], new_edges, self.original_indices)

    def delete_vertex(self, vertex):
        if not 0 <= vertex < len(self.edges):
            raise ValueError("Invalid vertex index")
        self.edges = np.delete(self.edges, vertex, 0)
        self.edges = np.delete(self.edges, vertex, 1)
        self.original_indices = np.delete(self.original_indices, vertex)
        self.num_vertices -= 1

    def get_adjacent_vertices(self, vertex: int) -> List:
        if 0 <= vertex < len(self.edges):
            adjacent_vertices = []
            for i in range(len(self.edges)):
                if self.edges[vertex, i] == 1:
                    adjacent_vertices.append(i)
            return adjacent_vertices
        else:
            raise ValueError("Invalid vertex index")

    def find_connected_components_dfs(self):
        visited = set()
        components = []
        traversal_order = []  # Список для хранения порядка обхода

        def dfs(node, component):
            visited.add(node)
            component.append(node)
            traversal_order.append(node)

            for neighbor in self.get_adjacent_vertices(node):
                if neighbor not in visited:
                    dfs(neighbor, component)

        for vertex in range(len(self.edges)):
            if vertex not in visited:
                component = []
                dfs(vertex, component)
                components.append(component)

        return components, traversal_order

    from collections import deque

    def find_connected_components_bfs(self):
        visited = set()
        components = []
        traversal_order = []  # Список для хранения порядка обхода

        for vertex in range(len(self.edges)):
            if vertex not in visited:
                component = []
                queue = deque([vertex])

                while queue:
                    node = queue.popleft()
                    visited.add(node)
                    component.append(node)
                    traversal_order.append(node)

                    for neighbor in self.get_adjacent_vertices(node):
                        if neighbor not in visited:
                            queue.append(neighbor)

                components.append(component)

        return components, traversal_order


    def __str__(self) -> str:
        return 'Матрица смежности:\n' + str(self.edges) + '\n' + 'Номера вершин:\n' + str(self.original_indices)


def is_valid_induced_subgraph(original_graph, subgraph):
        for i in range(len(subgraph.edges)):
            for j in range(i, len(subgraph.edges)):
                if subgraph.edges[i, j] == 1 and original_graph.edges[subgraph.original_indices[i], subgraph.original_indices[j]] == 0:
                    return False
        return True


class TestGraphs(unittest.TestCase):
    def test_generate_subgraphs(self):
        test_graph = Graph(
            5, 
            np.array([
                [0, 1, 1, 0, 0],
                [1, 0, 0, 1, 0],
                [1, 0, 0, 0, 1],
                [0, 1, 0, 0, 1],
                [0, 0, 1, 1, 0]
                ])
        )
        subgraphs = test_graph.find_all_induced_subgraphs([0, 1])
        subgraph = test_graph.get_subgraph([0, 1, 2, 4])
        for subgraph in subgraphs:
            self.assertTrue(is_valid_induced_subgraph(test_graph, subgraph))

    def test_union(self):
        graph1 = Graph(4, np.array([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]))
        graph2 = Graph(4, np.array([[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]))
        result = graph1.union(graph2)
        expected_edges = np.array([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]])
        self.assertTrue(np.array_equal(result.edges, expected_edges))

    def test_connection(self):
        graph1 = Graph(3)
        graph1.add_edge(0, 1)
        graph1.add_edge(1, 2)

        graph2 = Graph(2)
        graph2.add_edge(1, 0)

        union_graph = graph1.connection(graph2)
        print(union_graph)

    def test_intersection(self):
        graph1 = Graph(4, np.array([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]))
        graph2 = Graph(4, np.array([[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]))
        result = graph1.intersection(graph2)
        expected_edges = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        self.assertTrue(np.array_equal(result.edges, expected_edges))

    def test_complement(self):
        graph = Graph(4, np.array([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]))
        complement = graph.complement()
        expected_edges = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]])
        self.assertTrue(np.array_equal(complement.edges, expected_edges))

    def test_remove_edges(self):
        graph = Graph(4, np.array([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]))
        graph.remove_edge(0, 1)
        self.assertEqual(graph.edges[0, 1], 0)
        self.assertEqual(graph.edges[1, 0], 0)

    def test_remove_vertex(self):
        graph = Graph(4, np.array([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]))
        graph.delete_vertex(0)
        self.assertEqual(len(graph.edges), 3)

    def test_connected_components_dfs(self):
        graph = Graph(6, np.array([[0, 1, 0, 0, 0, 0],
                                   [1, 0, 1, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 1, 1],
                                   [0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 0, 0]]))

        components, traversal_order = graph.find_connected_components_dfs()

        self.assertEqual(len(components), 2) 
        self.assertIn([0, 1, 2], components) 
        self.assertIn([3, 4, 5], components) 
        self.assertEqual(traversal_order, [0, 1, 2, 3, 4, 5])

    def test_connected_components_bfs(self):
        graph = Graph(6, np.array([[0, 1, 0, 0, 0, 0],
                                   [1, 0, 1, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 1, 1],
                                   [0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 0, 0]]))

        components, traversal_order = graph.find_connected_components_bfs()
        

        self.assertEqual(len(components), 2) 
        self.assertIn([0, 1, 2], components) 
        self.assertIn([3, 4, 5], components) 
        self.assertEqual(traversal_order, [0, 1, 2, 3, 4, 5])

        
if __name__ == "__main__":
    unittest.main()
