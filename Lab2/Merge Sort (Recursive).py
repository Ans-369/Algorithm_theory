def merge_sort_recursive(arr):
    return merge_sort_recursive_with_counters(arr)


def merge_sort_recursive_with_counters(arr):
    comparisons = 0
    assignments = 0
    recursive_calls = 1

    print(f"Розділяємо масив: {arr}")
    if len(arr) <= 1:
        return arr, comparisons, assignments, recursive_calls

    mid = len(arr) // 2
    assignments += 1

    left_half, c1, a1, r1 = merge_sort_recursive_with_counters(arr[:mid])
    right_half, c2, a2, r2 = merge_sort_recursive_with_counters(arr[mid:])

    comparisons += c1 + c2
    assignments += a1 + a2
    recursive_calls += r1 + r2

    print(f"Зливаємо {left_half} та {right_half}")
    merged_arr, c_merge, a_merge = merge_recursive(left_half, right_half)
    comparisons += c_merge
    assignments += a_merge

    print(f"Злиття завершено. Результат: {merged_arr}")
    return merged_arr, comparisons, assignments, recursive_calls


def merge_recursive(left, right):
    merged_arr = []
    comparisons = 0
    assignments = 0
    i, j = 0, 0
    assignments += 2

    while i < len(left) and j < len(right):
        comparisons += 1
        is_less_eq = left[i] <= right[j]
        print(f"Порівняння: {left[i]} <= {right[j]} -> {is_less_eq}. Додаємо {left[i] if is_less_eq else right[j]}")
        if is_less_eq:
            merged_arr.append(left[i])
            i += 1
        else:
            merged_arr.append(right[j])
            j += 1
        assignments += 1

    while i < len(left):
        merged_arr.append(left[i])
        i += 1
        assignments += 1

    while j < len(right):
        merged_arr.append(right[j])
        j += 1
        assignments += 1

    return merged_arr, comparisons, assignments


print("\n--- РЕКУРСИВНА ВЕРСІЯ ---")
my_list = [38, 15, 50, 99, 41, 52, 47, 65, 95]
sorted_list, total_comparisons, total_assignments, total_recursive_calls = merge_sort_recursive(my_list)
print("-" * 50)
print(f"Фінальний відсортований список: {sorted_list}")
print(f"Загальна кількість порівнянь: {total_comparisons}")
print(f"Загальна кількість присвоювань: {total_assignments}")
print(f"Загальна кількість рекурсивних викликів: {total_recursive_calls}")
