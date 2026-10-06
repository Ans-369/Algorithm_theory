def merge_sort_iterative(a):
    n = len(a)
    comparisons = 0
    assignments = 0
    i = 1
    step = 1
    print("--- ІТЕРАТИВНА ВЕРСІЯ ---")
    print(f"Початковий масив: {a}")

    while i < n:
        j = 0
        while j < n - i:
            left = j
            mid = j + i
            right = min(j + 2 * i, n)

            print("-" * 50)
            print(
                f"Крок {step}. Об'єднуємо підмасиви: {a[left:mid]} і {a[mid:right]} | (індекси: [{left}:{mid}] та [{mid}:{right}])")

            c, a_count = merge(a, left, mid, right)
            comparisons += c
            assignments += a_count

            print(f"Масив після об'єднання: {a}")

            j += 2 * i
            step += 1
        i *= 2

    return a, comparisons, assignments


def merge(a, left, mid, right):
    comparisons = 0
    assignments = 0
    n1 = mid - left
    n2 = right - mid

    L = a[left:mid]
    R = a[mid:right]
    assignments += n1 + n2

    it1, it2, k = 0, 0, left
    assignments += 3

    while it1 < n1 and it2 < n2:
        comparisons += 1
        print(f"Порівняння: {L[it1]} < {R[it2]}")
        if L[it1] < R[it2]:
            a[k] = L[it1]
            it1 += 1
        else:
            a[k] = R[it2]
            it2 += 1
        assignments += 2
        k += 1
        assignments += 1

    while it1 < n1:
        a[k] = L[it1]
        it1 += 1
        k += 1
        assignments += 2

    while it2 < n2:
        a[k] = R[it2]
        it2 += 1
        k += 1
        assignments += 2

    return comparisons, assignments


my_list = [38, 15, 50, 99, 41, 52, 47, 65, 95]
sorted_list, comps, assigs = merge_sort_iterative(my_list.copy())
print("-" * 50)
print(f"Фінальний відсортований список: {sorted_list}")
print(f"Загальна кількість порівнянь: {comps}")
print(f"Загальна кількість присвоювань: {assigs}")
