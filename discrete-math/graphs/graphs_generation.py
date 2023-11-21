import random
import numpy as np

def generate_random_graph(n, r):
    max_edges = n * (n - 1) // 2 
    num_edges = int(max_edges * r) 

    if num_edges > max_edges:
        raise ValueError("Слишком высокая реберная плотность")

    graph = np.zeros((n, n), dtype=int)

    edges_added = 0
    while edges_added < num_edges:
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        if u != v and graph[u, v] == 0:
            graph[u][v] = graph[v, u] = 1
            edges_added += 1

    return graph


def generate_turan_graph(n, r):
    l1 = np.ceil(n / r).astype(int)
    l2 = np.floor(n / r).astype(int)

    k1 = np.mod(n, r)
    k2 = r - k1

    graph = np.zeros((n, n), dtype=int)

    for i in range(r):
        start = i * l1
        end = start + l1 if i < k1 else start + l2

        for j in range(i + 1, r):
            start_j = j * l1
            end_j = start_j + l1 if j < k1 else start_j + l2

            for u in range(start, end):
                for v in range(start_j, end_j):
                    graph[u, v] = 1
                    graph[v, u] = 1

    return graph


def generate_moser_graph(m):
    return generate_turan_graph(3*m, m)


def find_neighbors(graph, vertex):
    vertex = int(vertex)
    return np.where(graph[vertex] == 1)[0]


def find_neighbors_plus_vertex(graph, vertex):
    neighbors = find_neighbors(graph, vertex)
    return np.concatenate([neighbors.reshape(-1, 1), np.array([vertex])], axis=0)


def find_all_maximum_independent_sets(graph):
    k = 0
    S = np.array([])
    Q_minus = np.array([])
    Q_plus = np.arange(graph.shape[0])

    while len(Q_plus) > 0:
        # M1 (шаг вперед)
        print(f'k = {k}, Q_plus = {Q_plus}, Q_minus = {Q_minus}, S = {S}')
        v = np.array([Q_plus[0]])
        X = v
        S = np.concatenate([S, v])
        Q_minus = np.setdiff1d(Q_minus, find_neighbors(graph, v))
        Q_plus = np.setdiff1d(Q_plus, find_neighbors_plus_vertex(graph, v))
        k += 1

        # M2 (проверка)
        for u in Q_minus:
            if len(np.intersect1d(find_neighbors(graph, u), Q_plus)) == 0:
                break
        if len(Q_plus) == 0:
            if len(Q_minus) == 0:
                yield S
            break
        else:
            continue

        # M3 (шаг назад)
        k -= 1
        S = np.setdiff1d(S, X)
        Q_minus = np.concatenate([Q_minus, X])
        Q_plus = np.setdiff1d(Q_plus, X)
        if k == 0 and len(Q_plus) == 0:
            break


def bron_kerbosch(graph, R=set(), P=None, X=None):
    if P is None:
        P = set(range(len(graph)))
    if X is None:
        X = set()

    if len(P) == 0 and len(X) == 0:
        print("Maximal clique:", R)
        return

    for v in list(P):
        neighbors = set(np.nonzero(graph[v])[0])
        bron_kerbosch(graph, R | {v}, P & neighbors, X & neighbors)
        P.remove(v)
        X.add(v)


def bron_kerbosch_independent_sets(graph, R=set(), P=None, X=None):
    if P is None:
        P = set(range(len(graph)))
    if X is None:
        X = set()

    if len(P) == 0 and len(X) == 0:
        print("Maximal independent set:", R)
        return

    for v in list(P):
        non_neighbors = set(range(len(graph))) - set(np.nonzero(graph[v])[0]) - {v}
        bron_kerbosch_independent_sets(graph, R | {v}, P & non_neighbors, X & non_neighbors)
        P.remove(v)
        X.add(v)


if __name__ == '__main__':
    # print(generate_random_graph(10, 1), '\n')
    # print(generate_turan_graph(9, 3), '\n')
    print(generate_moser_graph(2), '\n')

    # result = bron_kerbosch(generate_moser_graph(2))
    # print("Максимальные клики:", result)

    result = bron_kerbosch_independent_sets(generate_moser_graph(2))
    print("Максимальные независимые множества:", result)

