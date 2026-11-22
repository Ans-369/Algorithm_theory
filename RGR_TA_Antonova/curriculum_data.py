import random
from typing import Dict, List, Tuple


def get_curriculum_graph() -> Tuple[Dict[int, List[int]], Dict[int, str]]:
    """
    Набір 1: Контрольний граф навчальних дисциплін бакалаврату ІТ (V = 8, E = 11).
    Дуга (u -> v) означає, що дисципліна u є пререквізитом для дисципліни v.
    """
    node_names = {
        0: "Дискретна математика",
        1: "Основи програмування",
        2: "Лінійна алгебра та аналітична геометрія",
        3: "Алгоритми та структури даних",
        4: "Об'єктно-орієнтоване програмування",
        5: "Теорія алгоритмів",
        6: "Бази даних",
        7: "Машинне навчання та аналіз даних"
    }
    edges = [
        (0, 3), (0, 6),
        (1, 3), (1, 4),
        (2, 7),
        (3, 5), (3, 6), (3, 7),
        (4, 6),
        (5, 7),
        (6, 7)
    ]
    adj_list = {i: [] for i in node_names}
    for u, v in edges:
        adj_list[u].append(v)
    return adj_list, node_names


def get_cyclic_curriculum_graph() -> Tuple[Dict[int, List[int]], Dict[int, str]]:
    """
    Набір 2: Некоректний навчальний план із циклічною залежністю (1 -> 2 -> 3 -> 1).
    """
    node_names = {
        0: "Вступ до комп'ютерних наук",
        1: "Архітектура комп'ютерів",
        2: "Операційні системи",
        3: "Системне програмування",
        4: "Розподілені системи"
    }
    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 1),  # Помилкова циклічна залежність
        (2, 4)
    ]
    adj_list = {i: [] for i in node_names}
    for u, v in edges:
        adj_list[u].append(v)
    return adj_list, node_names


def generate_random_dag(
    v_count: int,
    density: float,
    seed: int = 42
) -> Tuple[Dict[int, List[int]], int]:
    """
    Генерує випадковий орієнтований ациклічний граф (DAG) із V вершинами.
    Ациклічність гарантується спрямуванням усіх дуг строго зліва направо
    відносно випадкової перестановки вершин perm.
    """
    rng = random.Random(seed)
    perm = list(range(v_count))
    rng.shuffle(perm)
    adj_list: Dict[int, List[int]] = {i: [] for i in range(v_count)}
    edges_count = 0

    for i in range(v_count):
        u = perm[i]
        for j in range(i + 1, v_count):
            if rng.random() < density:
                v = perm[j]
                adj_list[u].append(v)
                edges_count += 1

    return adj_list, edges_count
