from collections import deque


def is_valid_state(state):
    farmer_pos, wolf_pos, goat_pos, cabbage_pos = state

    if (wolf_pos == goat_pos and farmer_pos != wolf_pos and wolf_pos == 0) or (
        goat_pos == cabbage_pos and farmer_pos != goat_pos and goat_pos == 0
    ):
        return False

    if (wolf_pos == goat_pos and farmer_pos != wolf_pos and wolf_pos == 1) or (
        goat_pos == cabbage_pos and farmer_pos != goat_pos and goat_pos == 1
    ):
        return False

    return True


def get_next_states(current_state):
    farmer_pos, wolf_pos, goat_pos, cabbage_pos = current_state
    next_states = []

    for move in range(4):
        new_farmer_pos = (
            1 - farmer_pos
        )

        new_wolf_pos = wolf_pos
        new_goat_pos = goat_pos
        new_cabbage_pos = cabbage_pos

        if move == 0:
            pass
        elif move == 1:  
            if wolf_pos == farmer_pos:  
                new_wolf_pos = 1 - wolf_pos
            else:
                continue  
        elif move == 2:  
            if goat_pos == farmer_pos:  
                new_goat_pos = 1 - goat_pos
            else:
                continue  
        elif move == 3:  
            if (
                cabbage_pos == farmer_pos
            ):  
                new_cabbage_pos = 1 - cabbage_pos
            else:
                continue  

        new_state = (new_farmer_pos, new_wolf_pos, new_goat_pos, new_cabbage_pos)

        if is_valid_state(new_state):
            next_states.append(new_state)

    return next_states


def solve_river_crossing():
    initial_state = (0, 0, 0, 0)  
    target_state = (1, 1, 1, 1)  

    queue = deque([(initial_state, [initial_state])])
    
    visited = {initial_state}

    while queue:
        current_state, path = queue.popleft()

        if current_state == target_state:
            return path  

        for next_state in get_next_states(current_state):
            if next_state not in visited:
                visited.add(next_state)
                new_path = path + [next_state]
                queue.append((next_state, new_path))

    return None  


def describe_state(state):
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
