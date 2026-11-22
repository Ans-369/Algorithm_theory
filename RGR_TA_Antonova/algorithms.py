import sys
from typing import Dict, List, Tuple

# Константи триколірного маркування вершин у алгоритмі DFS
WHITE = 0  # Вершина ще не відвідана
GRAY = 1   # Вершина перебуває в обробці (активна у стеку викликів)
BLACK = 2  # Вершина та всі її нащадки повністю оброблені


def topological_sort_dfs_recursive(
    adj_list: Dict[int, List[int]],
    v_count: int
) -> Tuple[bool, List[int], List[int], Dict[int, int], Dict[int, int]]:
    """
    Рекурсивне топологічне сортування орієнтованого графа методом обходу в глибину (DFS).
    Повертає кортеж:
      - is_dag (bool): True, якщо граф ациклічний; False, якщо виявлено цикл;
      - topo_order (List[int]): топологічно відсортований список вершин;
      - cycle_path (List[int]): список вершин знайденого циклу (якщо is_dag == False);
      - tin (Dict[int, int]): словник міток часу входу у вершини;
      - tout (Dict[int, int]): словник міток часу виходу з вершин.
    """
    # Збільшуємо ліміт глибини рекурсії для великих розріджених графів
    if sys.getrecursionlimit() < v_count + 500:
        sys.setrecursionlimit(v_count + 500)

    color = [WHITE] * v_count
    parent = [-1] * v_count
    tin: Dict[int, int] = {}
    tout: Dict[int, int] = {}
    topo_stack: List[int] = []
    cycle_path: List[int] = []
    timer = 0

    def dfs(u: int) -> bool:
        nonlocal timer
        color[u] = GRAY
        timer += 1
        tin[u] = timer

        for v in adj_list[u]:
            if color[v] == WHITE:
                parent[v] = u
                if not dfs(v):
                    return False
            elif color[v] == GRAY:
                # Виявлено зворотне ребро (u -> v) на активну вершину: відновлюємо цикл
                curr = u
                cycle = [v]
                while curr != v and curr != -1:
                    cycle.append(curr)
                    curr = parent[curr]
                cycle.append(v)
                cycle.reverse()
                cycle_path.extend(cycle)
                return False

        # Усі нащадки вершини u оброблені: фіксуємо час виходу та додаємо у стек
        color[u] = BLACK
        timer += 1
        tout[u] = timer
        topo_stack.append(u)
        return True

    # Обхід усіх компонент зв'язності графа
    for node in range(v_count):
        if color[node] == WHITE:
            if not dfs(node):
                return False, [], cycle_path, tin, tout

    # Інвертування стека формує порядок за спаданням часу виходу (reverse post-order)
    topo_stack.reverse()
    return True, topo_stack, [], tin, tout


def topological_sort_dfs_iterative(
    adj_list: Dict[int, List[int]],
    v_count: int
) -> Tuple[bool, List[int], List[int]]:
    """
    Ітеративна реалізація топологічного сортування методом DFS на базі явного стека викликів.
    Виключає ризик переповнення системного стека рекурсії на надвеликих графах.
    """
    color = [WHITE] * v_count
    parent = [-1] * v_count
    topo_stack: List[int] = []

    for start_node in range(v_count):
        if color[start_node] != WHITE:
            continue

        # Стек зберігає пари (поточна_вершина, індекс_наступного_сусіда)
        call_stack: List[Tuple[int, int]] = [(start_node, 0)]
        color[start_node] = GRAY

        while call_stack:
            u, edge_idx = call_stack[-1]
            neighbors = adj_list[u]

            if edge_idx < len(neighbors):
                call_stack[-1] = (u, edge_idx + 1)
                v = neighbors[edge_idx]
                if color[v] == WHITE:
                    color[v] = GRAY
                    parent[v] = u
                    call_stack.append((v, 0))
                elif color[v] == GRAY:
                    curr = u
                    cycle = [v]
                    while curr != v and curr != -1:
                        cycle.append(curr)
                        curr = parent[curr]
                    cycle.append(v)
                    cycle.reverse()
                    return False, [], cycle
            else:
                call_stack.pop()
                color[u] = BLACK
                topo_stack.append(u)

    topo_stack.reverse()
    return True, topo_stack, []


def topological_sort_dfs_with_trace(
    adj_list: Dict[int, List[int]],
    node_names: Dict[int, str]
) -> Tuple[bool, List[int]]:
    """
    Допоміжна версія алгоритму з покроковим виведенням протоколу обходу DFS.
    """
    v_count = len(node_names)
    color = [WHITE] * v_count
    tin: Dict[int, int] = {}
    tout: Dict[int, int] = {}
    topo_stack: List[int] = []
    timer = 0
    step = 0

    def log(depth: int, msg: str) -> None:
        nonlocal step
        step += 1
        indent = "  " * depth
        print(f"[Крок {step:>2}] {indent}{msg}")

    def dfs(u: int, depth: int) -> bool:
        nonlocal timer
        color[u] = GRAY
        timer += 1
        tin[u] = timer
        log(depth, f"Вхід у вершину {u} ('{node_names[u]}'): колір -> GRAY, tin = {tin[u]}")

        for v in adj_list[u]:
            edge_str = f"ребро {u} ('{node_names[u]}') -> {v} ('{node_names[v]}')"
            if color[v] == WHITE:
                log(depth + 1, f"Перехід по деревному {edge_str} (сусід WHITE)")
                if not dfs(v, depth + 1):
                    return False
            elif color[v] == GRAY:
                log(depth + 1, f"ПОМИЛКА! Зворотне {edge_str}: вершина {v} має статус GRAY (виявлено цикл!)")
                return False
            else:
                edge_type = "пряме" if tin[u] < tin[v] else "перехресне"
                log(depth + 1, f"Пропуск ({edge_type} {edge_str}): вершина {v} вже BLACK (tout = {tout[v]})")

        color[u] = BLACK
        timer += 1
        tout[u] = timer
        topo_stack.append(u)
        log(depth, f"Вихід із вершини {u} ('{node_names[u]}'): колір -> BLACK, tout = {tout[u]} | Стек: {topo_stack}")
        return True

    for node in range(v_count):
        if color[node] == WHITE:
            print(f"\n--- Запуск DFS із невідвіданої кореневої вершини {node} ('{node_names[node]}') ---")
            if not dfs(node, 0):
                return False, []

    topo_stack.reverse()
    return True, topo_stack


def verify_topological_order(adj_list: Dict[int, List[int]], topo_order: List[int]) -> bool:
    """
    Перевіряє коректність отриманого топологічного порядку:
    для кожної дуги (u -> v) позиція u має бути меншою за позицію v.
    """
    if len(topo_order) != len(adj_list):
        return False
    pos = {node: idx for idx, node in enumerate(topo_order)}
    for u, neighbors in adj_list.items():
        for v in neighbors:
            if pos[u] >= pos[v]:
                return False
    return True
