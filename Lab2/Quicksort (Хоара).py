def quicksort(a, l, r):
    comparisons = 0
    assignments = 0
    recursive_calls = 1

    print(f"Quicksort виклик: масив = {a}, l = {l}, r = {r}")

    if l < r:
        q, c1, a1 = partition(a, l, r)
        comparisons += c1
        assignments += a1

        c2, a2, r2 = quicksort(a, l, q)
        c3, a3, r3 = quicksort(a, q + 1, r)

        comparisons += c2 + c3
        assignments += a2 + a3
        recursive_calls += r2 + r3
    else:
        return 0, 0, 1

    return comparisons, assignments, recursive_calls


def partition(a, l, r):
    comparisons = 0
    assignments = 0
    pivot = a[l]
    assignments += 1
    i = l - 1
    j = r + 1
    assignments += 2

    print(f"Вибираємо опорний елемент (pivot): {pivot}")

    while True:
        i += 1
        assignments += 1
        while a[i] < pivot:
            comparisons += 1
            i += 1
            assignments += 1
        comparisons += 1

        j -= 1
        assignments += 1
        while a[j] > pivot:
            comparisons += 1
            j -= 1
            assignments += 1
        comparisons += 1

        comparisons += 1
        if i >= j:
            print(f"Індекси перетнулися. Поділ завершено. Повертаємо j={j}.")
            return j, comparisons, assignments

        a[i], a[j] = a[j], a[i]
        assignments += 3
        print(f"Поточні індекси: i = {i}, j = {j}. Обмінюємо a[{i}] ({a[j]}) і a[{j}] ({a[i]}). Масив: {a}")


print("\n--- Quicksort за схемою Хоара з трасуванням ---")
my_list = [38, 15, 50, 99, 41, 52, 47, 65, 95]
print(f"Оригінальний список: {my_list}")
total_comps, total_assigs, total_recs = quicksort(my_list, 0, len(my_list) - 1)
print("-" * 50)
print(f"Відсортований список: {my_list}")
print(f"Загальна кількість порівнянь: {total_comps}")
print(f"Загальна кількість присвоювань: {total_assigs}")
print(f"Загальна кількість рекурсивних викликів: {total_recs}")
