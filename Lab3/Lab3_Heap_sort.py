comp = 0  # для рахування порівнянь
assign = 0  # для рахування присвоювань

def swap(arr, i, j):
    """Міняє місцями два елементи в масиві."""
    global assign
    arr[i], arr[j] = arr[j], arr[i]
    assign += 3  # Обмін через тимчасову змінну  = 3 присвоювання

def sink(arr, i, n):
    """
    Процедура 'занурення' елемента вниз по купі.
    """
    global comp
    k = i
    while True:
        j = 2 * k + 1
        if j >= n:
            break
        
        comp += 1
        # Знаходимо найбільший дочірній елемент
        if j + 1 < n and arr[j + 1] > arr[j]:
            j += 1
            
        comp += 1
        # Якщо батько більший або дорівнює найбільшому дочірньому - вихід
        if arr[k] >= arr[j]:
            break
            
        swap(arr, k, j)
        k = j

def heapsort(arr):
    """Алгоритм пірамідального сортування."""
    n = len(arr)
    print(f"Початковий масив: {arr}\n")
    
    #  Побудова максимальної купи
    print("--- Фаза 1: Побудова максимальної купи ---")
    for i in range(n // 2 - 1, -1, -1):
        print(f"Занурюємо елемент з індексу {i}: {arr[i]}")
        sink(arr, i, n)
    print(f"\nМасив після побудови купи: {arr}\n")
    
    #  Сортування
    print("--- Фаза 2: Сортування ---")
    for i in range(n - 1, 0, -1):
        print(f"Міняємо місцями корінь ({arr[0]}) та останній елемент ({arr[i]})")
        swap(arr, 0, i)
        n_current = i
        print(f"Розмір купи зменшився до {n_current}. Відновлюємо властивості купи.")
        sink(arr, 0, n_current)
        print(f"Масив на поточному кроці: {arr}\n")
        
    return arr

# Вхідні дані Варіанту 1
A = [38, 15, 50, 99, 41, 52, 47, 65, 95]
sorted_A = heapsort(A)

print(f"Відсортований масив: {sorted_A}")
print(f"Кількість порівнянь: {comp}")
print(f"Кількість присвоювань: {assign}")