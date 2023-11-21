import numpy as np
from typing import List, Set


class Graph:
    def __init__(self, edges: np.array, vertex_names = None) -> None:
        if edges.shape[0] != edges.shape[1]:
            raise ValueError("Edges matrix shape does not match the number of vertices")

        if vertex_names is None:
            vertex_names = np.arange(edges.shape[0])

        if vertex_names.shape[0] != edges.shape[0]:
            raise ValueError("Vertex numbers shape does not match the number of vertices")

        self.edges = edges
        self.num_vertices = edges.shape[0]
        self.vertex_names = vertex_names

    def get_vertex_index(self, vertex_name) -> int:
        if vertex_name not in self.vertex_names:
            raise ValueError("No such vertex")
        return np.where(self.vertex_names == vertex_name)[0][0]

    def get_vertex_name(self, vertex_index):
        return self.vertex_names[vertex_index]

    def add_edge(self, vertex_1_name: int, vertex_2_name: int) -> None:
        vertex_1_index = self.get_vertex_index(vertex_1_name)
        vertex_2_index = self.get_vertex_index(vertex_2_name)
        
        self.edges[vertex_1_index, vertex_2_index] = 1
        self.edges[vertex_2_index, vertex_1_index] = 1

    def remove_edge(self, vertex_1_name: int, vertex_2_name: int) -> None:
        vertex_1_index = self.get_vertex_index(vertex_1_name)
        vertex_2_index = self.get_vertex_index(vertex_2_name)

        self.edges[vertex_1_index, vertex_2_index] = 0
        self.edges[vertex_2_index, vertex_1_index] = 0

    def delete_vertex(self, vertex_name):
        vertex_index = self.get_vertex_index(vertex_name)

        self.edges = np.delete(self.edges, vertex_index, 0)
        self.edges = np.delete(self.edges, vertex_index, 1)
        self.vertex_names = np.delete(self.vertex_names, vertex_index)
        self.num_vertices -= 1

    def __str__(self) -> str:
        return 'Имена вершин:\n' + str(self.vertex_names) + '\n' + 'Матрица смежности:\n' + str(self.edges)


def is_connected_vertexes(G: Graph, vertex_1_name, vertex_2_name) -> bool:
    vertex_1_index = G.get_vertex_index(vertex_1_name)
    vertex_2_index = G.get_vertex_index(vertex_2_name)
    return G.edges[vertex_1_index, vertex_2_index] == 1


def  get_subgraph(G: Graph, sungraph_vertex_names) -> Graph:
    subraph = G
    for vertex in np.setdiff1d(G.vertex_names, sungraph_vertex_names):
        subraph.delete_vertex(vertex)
    return subraph


def vertex_degree(G: Graph, vertex_name):
    vertex = G.get_vertex_index(vertex_name)
    degree = np.sum(G.edges[vertex, :])
    return degree


def find_neighbors(G: Graph, vertex_name):
    vertex = G.get_vertex_index(vertex_name)
    neighbors_row = G.edges[vertex, :]
    neighbors_indices = np.where(neighbors_row == 1)[0]
    neighbors_names = G.get_vertex_name(neighbors_indices)
    return neighbors_names


def find_neighbors_plus_vertex(G: Graph, vertex_name):
    neighbors = find_neighbors(G, vertex_name)
    return np.concatenate([neighbors, np.array([vertex_name])])


def find_neighbors_of_neighbors_minus_vertex(G: Graph, vertex_name):
    neighbors_of_neighbors = np.array([])
    neighbors = find_neighbors(G, vertex_name)
    for neighbor in neighbors:
        neighbors_of_neighbor = find_neighbors(G, neighbor)
        neighbors_of_neighbors = np.concatenate([neighbors_of_neighbors, neighbors_of_neighbor])
    return np.setdiff1d(neighbors_of_neighbors, np.array([vertex_name]))


def is_dominating(G: Graph, vertex_A_name, vertex_B_name) -> bool:
    neighbors_A = set(find_neighbors_plus_vertex(G, vertex_A_name))
    neighbors_B = set(find_neighbors_plus_vertex(G, vertex_B_name))
    return neighbors_A.issubset(neighbors_B)


def is_connected(G: Graph) -> bool:
    if G.num_vertices == 0:
        return True

    def dfs(start, visited):
        visited[start] = True
        for neighbor in range(G.num_vertices):
            if G.edges[start, neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor, visited)

    num_vertices = G.num_vertices
    visited = [False] * num_vertices
    dfs(0, visited)
    
    return all(visited)


def find_smallest_connected_component(G: Graph) -> Graph:
    def dfs(start, visited, component):
        visited[start] = True
        component.append(start)
        for neighbor in range(G.num_vertices):
            if G.edges[start, neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor, visited, component)

    num_vertices = G.num_vertices
    visited = [False] * num_vertices
    smallest_component = None

    for vertex in range(num_vertices):
        if not visited[vertex]:
            current_component = []
            dfs(vertex, visited, current_component)
            if smallest_component is None or len(current_component) < len(smallest_component):
                smallest_component = current_component

    smallest_component_names = G.get_vertex_name(smallest_component)
    return get_subgraph(G, smallest_component_names)


def find_minimal_degree_vertices(G: Graph):
    degrees = np.sum(G.edges, axis=1)
    min_degree = np.min(degrees)
    minimal_degree_vertices = np.where(degrees == min_degree)[0]
    minimal_degree_vertices_names = G.get_vertex_name(minimal_degree_vertices)
    return minimal_degree_vertices_names


def find_maximal_degree_neighbor(G: Graph, vertex_name):
    neighbors = find_neighbors(G, vertex_name)
    neighbors_indices = np.array([G.get_vertex_index(neighbor) for neighbor in neighbors])

    degrees = np.sum(G.edges, axis=1)
    max_degree_neighbor = None
    max_degree = -1

    for neighbor_index in neighbors_indices:
        if degrees[neighbor_index] > max_degree:
            max_degree_neighbor_index = neighbor_index
            max_degree = degrees[neighbor_index]

    return G.get_vertex_name(max_degree_neighbor_index)


def  find_min_degree_A_with_max_degree_B_neighbor(G: Graph) -> (int, int):
    minimal_degree_vertices = find_minimal_degree_vertices(G)
    
    A_with_max_B_degree, maxB_degree, maxB = -1, -1, -1
    for A in minimal_degree_vertices:
        B = find_maximal_degree_neighbor(G, A)
        B_degree = vertex_degree(G, B)
        if B_degree >= maxB_degree:
            A_with_max_B_degree = A
            maxB_degree = B_degree
            maxB = B
            
    return A_with_max_B_degree, maxB


def graph_a_minus_graph_b(A: Graph, B: Graph) -> Graph:
    for vertex_name in B.vertex_names:
        A.delete_vertex(vertex_name)
    return A


def drop_vertexes(G: Graph, vertexes) -> Graph:
    result = Graph(G.edges, G.vertex_names)
    for vertex in vertexes:
        result.delete_vertex(vertex)
    return result


def sort_vertexes_by_degree(G: Graph, vertexes):
    vertexes_degree = np.array([vertex_degree(G, vertex) for vertex in vertexes])
    vertexes = vertexes[np.argsort(vertexes_degree)]
    return vertexes


def ms1(G: Graph, S):
    S = sort_vertexes_by_degree(G, S)
    print('New ms1 cycle, G: \n' + str(G) + '\nS: ' + str(S) + '\n')
    s1_index = G.get_vertex_index(S[0])
    s2_index = G.get_vertex_index(S[1])
    if G.edges[s1_index, s2_index] == 1:
        if vertex_degree(G, S[0]) <= 3:
            print('Case 8' + '\n')
            return robson(G)
    raise ValueError("Invalid input")


def ms2(G: Graph, S):
    S = sort_vertexes_by_degree(G, S)
    print('New ms2 cycle, G: \n' + str(G) + '\nS: ' + str(S) + '\n')
    index = 0
    last_pair = None
    for vertex1, vertex2 in zip(S, np.concatenate([S[1:], np.array([S[0]])])):
        vertex_1_index = G.get_vertex_index(vertex1)
        vertex_2_index = G.get_vertex_index(vertex2)
        if G.edges[vertex_1_index, vertex_2_index] == 1:
            last_pair = np.array([vertex1, vertex2])
            index += 1
    if index == 3:
        print('Case 17' + '\n')
        return np.array([])
    if index == 1:
        print('Case 19' + '\n')
        return np.concatenate([
            np.setdiff1d(S, last_pair),
            ms1(
                drop_vertexes(
                    G,
                    np.setdiff1d(S, last_pair)
                ),
                last_pair
            )
        ])
    else:
        raise ValueError("Invalid input")
        

def robson(G: Graph):
    print('New robson cycle, G: \n' + str(G) + '\n')

    if not is_connected(G):
        C: Graph = find_smallest_connected_component(G)
        # (1)
        print('Case 1' + '\n')
        return robson(graph_a_minus_graph_b(G, C))

    if G.num_vertices <= 1:
        # (2)
        print('Case 2' + '\n')
        return G.vertex_names

    A, B = find_min_degree_A_with_max_degree_B_neighbor(G)
    # print(A, B)
    if vertex_degree(G, A) == 1:
        # (3)
        print('Case 3' + '\n')
        return np.concatenate([np.array([A]), robson(drop_vertexes(G, find_neighbors_plus_vertex(G, A)))])

    if vertex_degree(G, A) == 2:
        B_dot = np.setdiff1d(find_neighbors(G, A), np.array([B]))[0]
        if is_connected_vertexes(G, B, B_dot):
            # (4)
            print('Case 4' + '\n')
            return np.concatenate([np.array([A]), robson(drop_vertexes(G, find_neighbors_plus_vertex(G, A)))])
        # (5)
        print('Case 5' + '\n')
        res1 = np.concatenate([
            np.array([B, B_dot]), 
            robson(
                drop_vertexes(
                    drop_vertexes(
                        G, 
                        find_neighbors_plus_vertex(G, B)
                    ), 
                    find_neighbors_plus_vertex(
                        drop_vertexes(
                            G, 
                            find_neighbors_plus_vertex(G, B)
                        ), 
                        B_dot
                    )
                )
            )
        ])
        res2 = np.concatenate([
            np.array([A]),
            ms2(
                drop_vertexes(G, find_neighbors_plus_vertex(G, A)), 
                find_neighbors_of_neighbors_minus_vertex(G, A)
            )
        ])
        if len(res1) >= len(res2):
            return res1
        else:
            return res2
    
    if vertex_degree(G, A) == 3:
        # (6)
        print('Case 6' + '\n')
        res1 = ms2(
            drop_vertexes(G, np.array([A])),
            find_neighbors(G, A)
        )
        res2 = np.concatenate([
            np.array([A]),
            robson(drop_vertexes(G, find_neighbors_plus_vertex(G, A)))
        ])
        if len(res1) >= len(res2):
            return res1
        else:
            return res2
    
    raise ValueError('Invalide Input')


def main() -> None:
    # edges = np.array([
    #         [0, 0, 1, 1, 1, 0, 1, 1, 0],
    #         [0, 0, 1, 0, 0, 1, 0, 0, 1],
    #         [1, 1, 0, 1, 1, 0, 0, 0, 0],
    #         [1, 0, 1, 0, 1, 0, 1, 0, 0],
    #         [1, 0, 1, 1, 0, 0, 1, 0, 0],
    #         [0, 1, 0, 0, 0, 0, 0, 1, 0],
    #         [1, 0, 0, 1, 1, 0, 0, 0, 0],
    #         [1, 0, 0, 0, 0, 1, 0, 0, 1],
    #         [0, 1, 0, 0, 0, 0, 0, 1, 0]
    #     ])

    edges = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ])

    my_graph = Graph(edges, np.array([1, 2, 3]))    

    print(robson(my_graph))


if __name__ == '__main__':
    main()
