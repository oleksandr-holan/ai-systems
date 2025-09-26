from collections import deque


def is_valid_state(state):
    """
    Перевіряє, чи є заданий стан допустимим.
    state = (farmer_pos, wolf_pos, goat_pos, cabbage_pos)
    0 = початковий берег, 1 = протилежний берег
    """
    farmer_pos, wolf_pos, goat_pos, cabbage_pos = state

    # Перевіряємо обидва береги
    # Для початкового берега (всі об'єкти з позицією 0)
    if (wolf_pos == goat_pos and farmer_pos != wolf_pos and wolf_pos == 0) or (
        goat_pos == cabbage_pos and farmer_pos != goat_pos and goat_pos == 0
    ):
        return False

    # Для протилежного берега (всі об'єкти з позицією 1)
    if (wolf_pos == goat_pos and farmer_pos != wolf_pos and wolf_pos == 1) or (
        goat_pos == cabbage_pos and farmer_pos != goat_pos and goat_pos == 1
    ):
        return False

    return True


def get_next_states(current_state):
    """
    Генерує всі можливі наступні допустимі стани з поточного стану.
    """
    farmer_pos, wolf_pos, goat_pos, cabbage_pos = current_state
    next_states = []

    # Можливі переміщення човном (що фермер везе)
    # 0: фермер сам
    # 1: фермер і вовк
    # 2: фермер і коза
    # 3: фермер і капуста

    # Спробуємо всі 4 варіанти перевезення
    for move in range(4):
        new_farmer_pos = (
            1 - farmer_pos
        )  # Фермер завжди переправляється на протилежний берег

        new_wolf_pos = wolf_pos
        new_goat_pos = goat_pos
        new_cabbage_pos = cabbage_pos

        if move == 0:  # Фермер сам
            pass
        elif move == 1:  # Фермер і вовк
            if wolf_pos == farmer_pos:  # Вовк має бути на тому ж березі, що й фермер
                new_wolf_pos = 1 - wolf_pos
            else:
                continue  # Неможливо перевезти вовка, якщо його немає на цьому березі
        elif move == 2:  # Фермер і коза
            if goat_pos == farmer_pos:  # Коза має бути на тому ж березі, що й фермер
                new_goat_pos = 1 - goat_pos
            else:
                continue  # Неможливо перевезти козу, якщо її немає на цьому березі
        elif move == 3:  # Фермер і капуста
            if (
                cabbage_pos == farmer_pos
            ):  # Капуста має бути на тому ж березі, що й фермер
                new_cabbage_pos = 1 - cabbage_pos
            else:
                continue  # Неможливо перевезти капусту, якщо її немає на цьому березі

        new_state = (new_farmer_pos, new_wolf_pos, new_goat_pos, new_cabbage_pos)

        # Перевіряємо, чи є новий стан допустимим
        if is_valid_state(new_state):
            next_states.append(new_state)

    return next_states


def solve_river_crossing():
    """
    Вирішує задачу "Переправа через річку" за допомогою BFS.
    """
    initial_state = (0, 0, 0, 0)  # (Фермер, Вовк, Коза, Капуста) - всі на березі 0
    target_state = (1, 1, 1, 1)  # Всі на березі 1

    # Черга для BFS: зберігає (state, path_to_state)
    queue = deque([(initial_state, [initial_state])])

    # Множина для зберігання відвіданих станів, щоб уникнути циклів
    visited = {initial_state}

    while queue:
        current_state, path = queue.popleft()

        if current_state == target_state:
            return path  # Знайдено рішення

        for next_state in get_next_states(current_state):
            if next_state not in visited:
                visited.add(next_state)
                new_path = path + [next_state]
                queue.append((next_state, new_path))

    return None  # Рішення не знайдено


def describe_state(state):
    """
    Допоміжна функція для зрозумілого опису стану.
    """
    farmer_pos, wolf_pos, goat_pos, cabbage_pos = state
    bank_names = {0: "Лівий берег", 1: "Правий берег"}

    desc = f"Фермер: {bank_names[farmer_pos]}, Вовк: {bank_names[wolf_pos]}, Коза: {bank_names[goat_pos]}, Капуста: {bank_names[cabbage_pos]}"
    return desc


if __name__ == "__main__":
    solution_path = solve_river_crossing()

    if solution_path:
        print("Знайдено рішення для задачі Переправа через річку:")
        for i, state in enumerate(solution_path):
            print(f"Крок {i}: {describe_state(state)}")
    else:
        print("Рішення не знайдено.")
