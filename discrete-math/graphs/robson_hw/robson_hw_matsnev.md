## Обзор
Далее представлен разбор решения с моим графом, но сначала...

## Код вспомогательных функций
```python
import numpy as np


# Степень вершины (vertex) графа
def vertex_degree(graph, vertex):
    degree = np.sum(graph[vertex, :])
    return degree


# Соседи вершины (vertex) графа
def find_neighbors(graph, vertex):
    neighbors_row = graph[vertex, :]
    neighbor_indices = np.where(neighbors_row == 1)[1]
    return list(neighbor_indices)


# Соседи вершины (vertex) графа + вершина
def find_neighbors_plus_vertex(graph, vertex):
	return find_neighbors(graph, vertex) + [vertex]


# Соседи соседей вершин кроме начальной вершины
def find_neighbors_of_neighbors_minus_vertex(graph, vertex):


# Проверка на то, домирует ли вершина A (vertex_A) над вершиной B (vertex_B) в графе (graph)
def is_dominating(graph, vertex_A, vertex_B):
    neighbors_A = set(find_neighbors_plus_vertex(graph, vertex_A))
    neighbors_B = set(find_neighbors_plus_vertex(graph, vertex_B))
    return neighbors_A.issubset(neighbors_B)


# Проверка на то, является ли граф (graph) связным
def is_connected(graph):
    def dfs(start, visited):
        visited[start] = True
        for neighbor in range(len(graph)):
            if graph[start, neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor, visited)
                
    num_vertices = len(graph)
    visited = [False] * num_vertices
    dfs(0, visited)
    
    return all(visited)


# Получить подграф с вершинами (component) из графа (graph)
def extract_subgraph(graph, component):
    num_vertices = len(graph)
    subgraph = np.zeros((len(component), len(component)), dtype=int)

    for i in range(len(component)):
        for j in range(len(component)):
            subgraph[i][j] = graph[component[i], component[j]]

    return subgraph


# Найти самую маленькую компоненту связности в графе (graph)
def find_smallest_connected_component(graph):
    def dfs(start, visited, component):
        visited[start] = True
        component.append(start)
        for neighbor in range(len(graph)):
            if graph[start, neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor, visited, component)

    num_vertices = len(graph)
    visited = [False] * num_vertices
    smallest_component = None

    for vertex in range(num_vertices):
        if not visited[vertex]:
            current_component = []
            dfs(vertex, visited, current_component)
            if smallest_component is None or len(current_component) < len(smallest_component):
                smallest_component = current_component

    return extract_subgraph(graph, np.sort(smallest_component))


# Найти минимальную вершины с минимальной степенью в графе (graph)
def find_minimal_degree_vertices(graph):
    degrees = np.sum(graph, axis=1)
    min_degree = np.min(degrees)
    minimal_degree_vertices = np.where(degrees == min_degree)[0]
    return minimal_degree_vertices


# Найти вершину с максимальной степенью среди соседей вершины (vertex)
def find_maximal_degree_neighbor(graph, vertex):
    neighbors = find_neighbors(graph, vertex)
    degrees = np.sum(graph, axis=1)
    max_degree_neighbor = None
    max_degree = -1

    for neighbor in neighbors:
        if degrees[neighbor] > max_degree:
            max_degree_neighbor = neighbor
            max_degree = degrees[neighbor]

    return max_degree_neighbor


# Найти минимальную вершину графа с соседом с максимальной степенью
def  find_min_degree_A_with_max_degree_B_neighbor(graph):
    minimal_degree_vertices = find_minimal_degree_vertices(G)
    
    A_with_max_B_degree, maxB_degree, maxB = -1, -1, -1
    for A in minimal_degree_vertices:
        B = find_maximal_degree_neighbor(G, A)
        B_degree = vertex_degree(G, B)
        if B_degree > maxB_degree:
            A_with_max_B_degree = A
            maxB_degree = B_degree
            maxB = B
            
    return A_with_max_B_degree, maxB
```

## Проход по алгоритму

```python
G = np.matrix([
	[0, 0, 0, 0, 1, 0, 0, 1, 1],
	[0, 0, 0, 1, 0, 1, 0, 0, 0],
	[0, 0, 0, 1, 0, 1, 0, 0, 0],
	[0, 1, 1, 0, 0, 0, 1, 0, 0],
	[1, 0, 0, 0, 0, 0, 1, 1, 1],
	[0, 1, 1, 0, 0, 0, 0, 1, 0],
	[0, 0, 0, 1, 1, 0, 0, 1, 1],
	[1, 0, 0, 0, 1, 1, 1, 0, 1],
	[1, 0, 0, 0, 1, 0, 1, 1, 0],
])
```
### *Важно! В моём коде нумеровка вершин идёт не с 1, а с 0. Т.е. выход функции, к примеру [0, 1], означает для задания [1,2].*
1. is_connected(G) -> True (в (1) вариант не попадаем, но реализация find_smallest_connected_component у меня есть (см. код выше))
2. |G| = G.shape[0] = 9 not <= 1 (во (2) вариант тоже не попали)
- find_min_degree_A_with_max_degree_B_neighbor(G) -> (1, 3). В нашем задании получаем A = 2, B = 4 (см. предупреждение).
3. vertex_degree(G, 1) -> 2 != 1 (в (3) не попали)
- B' = find_neighbors(G, 1).remove(3) = 5. Т.е. соседи A, за исключением B - это только вершина 6 (+1, из-зи нумеровки в коде). 
4. Ребра между B = 4 и В' = 6 нет (в (4) не попали)
5. Значит мы попадаем в (5). 
   1. max1 = 2 + |ms(G − N (B) − N (B'))| = 2 + |ms({1, 5, 9})| = 3
   2. max2 = 1 + |ms^2(G − N(A), N^2(A))| = 1 + |ms^2(G - N(A), {3, 7, 8})| = 4
   3. max(max1, max2) = max2 -> {A} ∪ ms^2(G − N(A), N^2(A)) = {2, 3, 1, 7}

## Ответ: mu(G) = {2, 3, 1, 7}