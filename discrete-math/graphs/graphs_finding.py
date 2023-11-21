import numpy as np

def is_independent_set(graph, node_set):
    for i in node_set:
        for j in node_set:
            if i != j and graph[i, j] == 1:
                return False
    return True


def brute_force_maximum_independent_set(graph):
    n = len(graph)
    max_independent_set = set()

    for i in range(2**n):
        current_set = {j for j in range(n) if (i >> j) & 1}
        if is_independent_set(graph, current_set) and len(current_set) > len(max_independent_set):
            max_independent_set = current_set

    return max_independent_set


def main():
    edges = np.array([
            [0, 0, 1, 1, 1, 0, 1, 1, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 1],
            [1, 1, 0, 1, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 0],
            [1, 0, 1, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 1, 0]
        ])

    print("Максимальное независимое множество:", brute_force_maximum_independent_set(edges))


if __name__ == "__main__":
    main()
