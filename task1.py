from collections import deque, defaultdict


class EdmondsKarp:
    def __init__(self):
        self.graph = defaultdict(list)
        self.capacity = defaultdict(lambda: defaultdict(int))
        self.flow = defaultdict(lambda: defaultdict(int))

    def add_edge(self, u, v, capacity):
        """
        Додає ребро u -> v з пропускною здатністю capacity.
        Також додаємо зворотне ребро для залишкової мережі.
        """
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.capacity[u][v] += capacity

    def bfs(self, source, sink, parent):
        """
        BFS шукає найкоротший збільшуючий шлях
        від source до sink у залишковій мережі.
        """
        visited = set()
        queue = deque()

        queue.append(source)
        visited.add(source)

        while queue:
            current = queue.popleft()

            for neighbor in self.graph[current]:
                residual_capacity = self.capacity[current][neighbor] - self.flow[current][neighbor]

                if neighbor not in visited and residual_capacity > 0:
                    visited.add(neighbor)
                    parent[neighbor] = current

                    if neighbor == sink:
                        return True

                    queue.append(neighbor)

        return False

    def max_flow(self, source, sink):
        """
        Основна реалізація алгоритму Едмондса-Карпа.
        """
        max_flow_value = 0
        steps = []

        while True:
            parent = {}
            found_path = self.bfs(source, sink, parent)

            if not found_path:
                break

            # Знаходимо мінімальну пропускну здатність на знайденому шляху
            path_flow = float("inf")
            current = sink
            path = []

            while current != source:
                previous = parent[current]
                path_flow = min(
                    path_flow,
                    self.capacity[previous][current] - self.flow[previous][current]
                )
                path.append((previous, current))
                current = previous

            path.reverse()

            # Оновлюємо потоки
            current = sink
            while current != source:
                previous = parent[current]
                self.flow[previous][current] += path_flow
                self.flow[current][previous] -= path_flow
                current = previous

            max_flow_value += path_flow
            steps.append((path, path_flow, max_flow_value))

        return max_flow_value, steps


def build_logistics_network():
    ek = EdmondsKarp()

    source = "Джерело"
    sink = "Стік"

    terminals = ["Термінал 1", "Термінал 2"]

    stores = [f"Магазин {i}" for i in range(1, 15)]

    edges = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),

        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),

        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),

        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),

        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),

        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]

    # Додаємо основні ребра
    for u, v, capacity in edges:
        ek.add_edge(u, v, capacity)

    # Додаємо ребра від джерела до терміналів.
    # Їхня пропускна здатність дорівнює сумі вихідних можливостей термінала.
    ek.add_edge(source, "Термінал 1", 60)
    ek.add_edge(source, "Термінал 2", 55)

    # Додаємо ребра від магазинів до стоку.
    # Пропускна здатність дорівнює сумі вхідних можливостей магазину.
    store_capacities = {
        "Магазин 1": 15,
        "Магазин 2": 10,
        "Магазин 3": 20,
        "Магазин 4": 15,
        "Магазин 5": 10,
        "Магазин 6": 25,
        "Магазин 7": 20,
        "Магазин 8": 15,
        "Магазин 9": 10,
        "Магазин 10": 20,
        "Магазин 11": 10,
        "Магазин 12": 15,
        "Магазин 13": 5,
        "Магазин 14": 10,
    }

    for store, capacity in store_capacities.items():
        ek.add_edge(store, sink, capacity)

    return ek, source, sink, edges


def print_results():
    ek, source, sink, edges = build_logistics_network()

    max_flow_value, steps = ek.max_flow(source, sink)

    print("=" * 70)
    print("МАКСИМАЛЬНИЙ ПОТІК У ЛОГІСТИЧНІЙ МЕРЕЖІ")
    print("=" * 70)
    print(f"Максимальний потік: {max_flow_value} одиниць")
    print()

    print("ПОКРОКОВИЙ РОЗРАХУНОК:")
    print("-" * 70)

    for i, (path, path_flow, total_flow) in enumerate(steps, start=1):
        path_nodes = [path[0][0]] + [v for _, v in path]
        print(f"Крок {i}:")
        print(" -> ".join(path_nodes))
        print(f"Доданий потік: {path_flow}")
        print(f"Поточний сумарний потік: {total_flow}")
        print()

    print("=" * 70)
    print("ФАКТИЧНІ ПОТОКИ ПО РЕБРАХ:")
    print("=" * 70)

    for u, v, capacity in edges:
        actual_flow = ek.flow[u][v]
        print(f"{u:12} -> {v:12} | Потік: {actual_flow:3} / {capacity}")

    print()

    print("=" * 70)
    print("ПІДСУМОК ПО ТЕРМІНАЛАХ:")
    print("=" * 70)
    print(f"Термінал 1 відправив: {ek.flow[source]['Термінал 1']} одиниць")
    print(f"Термінал 2 відправив: {ek.flow[source]['Термінал 2']} одиниць")


if __name__ == "__main__":
    print_results()