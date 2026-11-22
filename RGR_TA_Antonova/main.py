import time
from algorithms import (
    topological_sort_dfs_recursive,
    topological_sort_dfs_iterative,
    topological_sort_dfs_with_trace,
    verify_topological_order
)
from curriculum_data import (
    get_curriculum_graph,
    get_cyclic_curriculum_graph,
    generate_random_dag
)


def run_curriculum_demo() -> None:
    print("=" * 96)
    print(" ЕТАП 1: ТРАСУВАННЯ ТА АПРОБАЦІЯ НА НАВЧАЛЬНОМУ ПЛАНІ СПЕЦІАЛЬНОСТІ (V = 8, E = 11)")
    print("=" * 96)
    adj_list, names = get_curriculum_graph()
    is_dag, topo_order = topological_sort_dfs_with_trace(adj_list, names)

    print("\n" + "-" * 96)
    print(f"Граф ациклічний (DAG): {is_dag}")
    print(f"Топологічний вектор індексів: {topo_order}")
    print("Рекомендована послідовність вивчення навчальних дисциплін:")
    for step_num, node_id in enumerate(topo_order, 1):
        print(f"  {step_num}. [{node_id}] {names[node_id]}")
    is_valid = verify_topological_order(adj_list, topo_order)
    print(f"Автоматична перевірка інваріанта пререквізитів (pos[u] < pos[v]): {'УСПІШНО' if is_valid else 'ПОМИЛКА'}")
    print("-" * 96)


def run_cyclic_test() -> None:
    print("\n" + "=" * 96)
    print(" ЕТАП 2: ТЕСТУВАННЯ НА НЕКОРЕКТНОМУ НАВЧАЛЬНОМУ ПЛАНІ З ЦИКЛОМ (V = 5, E = 5)")
    print("=" * 96)
    adj_c, names_c = get_cyclic_curriculum_graph()
    ok_c, _, cycle_c, _, _ = topological_sort_dfs_recursive(adj_c, len(names_c))
    print(f"Граф ациклічний (is_dag): {ok_c}")
    if not ok_c:
        cycle_desc = " -> ".join(f"[{u}] {names_c[u]}" for u in cycle_c)
        print(f"Виявлено суперечність (цикл у навчальному плані): {cycle_desc}")


def run_benchmarks() -> None:
    print("\n" + "=" * 96)
    print(" ЕТАП 3: ДОСЛІДЖЕННЯ ШВИДКОДІЇ ТА ЛІНІЙНОЇ СКЛАДНОСТІ Θ(V + E)")
    print("=" * 96)
    sizes = [500, 1000, 1500, 2000, 3000, 4000, 5000]

    for label, density in [("РОЗРІДЖЕНИХ (щільність 5%)", 0.05), ("ЩІЛЬНИХ (щільність 30%)", 0.30)]:
        print(f"\n>>> Тестування на {label} ациклічних графах:")
        print(f"{'Вершини (V)':<13} | {'Ребра (E)':<11} | {'V + E':<11} | {'Рек. DFS (с)':<15} | {'Ітер. DFS (с)':<15} | {'Статус'}")
        print("-" * 96)
        for v in sizes:
            adj_r, e_cnt = generate_random_dag(v, density, seed=42)

            t0 = time.perf_counter()
            ok1, ord1, _, _, _ = topological_sort_dfs_recursive(adj_r, v)
            t_rec = time.perf_counter() - t0

            t0 = time.perf_counter()
            ok2, ord2, _ = topological_sort_dfs_iterative(adj_r, v)
            t_iter = time.perf_counter() - t0

            status = "Ok" if (ok1 and ok2 and ord1 == ord2 and verify_topological_order(adj_r, ord1)) else "Fail"
            print(f"{v:<13} | {e_cnt:<11} | {v + e_cnt:<11} | {t_rec:<15.6f} | {t_iter:<15.6f} | {status}")


if __name__ == "__main__":
    run_curriculum_demo()
    run_cyclic_test()
    run_benchmarks()
