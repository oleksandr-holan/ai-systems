import numpy as np
import random

ASSETS = ["Apple", "Google", "Tesla", "Gold", "Bonds"]
N_ASSETS = len(ASSETS)

EXPECTED_RETURNS = np.array([0.25, 0.20, 0.45, 0.05, 0.03])

COVARIANCE_MATRIX = np.array(
    [
        [0.10, 0.03, 0.04, -0.01, 0.00],  # Apple
        [0.03, 0.09, 0.05, -0.01, 0.00],  # Google
        [0.04, 0.05, 0.25, 0.02, -0.01],  # Tesla
        [-0.01, -0.01, 0.02, 0.02, 0.01],  # Gold
        [0.00, 0.00, -0.01, 0.01, 0.005],  # Bonds
    ]
)

RISK_FREE_RATE = 0.02

POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.1
ELITISM_COUNT = 2


def create_individual():
    """Створює випадковий портфель (генотип), сума ваг = 1."""
    weights = np.random.random(N_ASSETS)
    return weights / np.sum(weights)


def calculate_fitness(weights):
    """Розрахунок коефіцієнта Шарпа."""
    portfolio_return = np.sum(weights * EXPECTED_RETURNS)

    portfolio_volatility = np.sqrt(
        np.dot(weights.T, np.dot(COVARIANCE_MATRIX, weights))
    )

    if portfolio_volatility == 0:
        return 0
    sharpe_ratio = (portfolio_return - RISK_FREE_RATE) / portfolio_volatility
    return sharpe_ratio


def selection(population, fitness_scores):
    """Турнірний відбір."""
    tournament_size = 3
    selected_indices = random.sample(range(len(population)), tournament_size)
    best_idx = selected_indices[0]
    for idx in selected_indices[1:]:
        if fitness_scores[idx] > fitness_scores[best_idx]:
            best_idx = idx
    return population[best_idx]


def crossover(parent1, parent2):
    """Арифметичний кросовер (зважене середнє)."""
    alpha = random.random()
    child = alpha * parent1 + (1 - alpha) * parent2
    return child


def mutation(individual):
    """Мутація: невелика зміна випадкових ваг та ре-нормалізація."""
    if random.random() < MUTATION_RATE:
        idx = random.randint(0, N_ASSETS - 1)
        change = np.random.normal(0, 0.1)
        individual[idx] += change
        individual = np.clip(individual, 0, 1)  # Щоб не було від'ємних ваг
        individual = individual / np.sum(individual)
    return individual


def run_evolution():
    population = [create_individual() for _ in range(POPULATION_SIZE)]

    for gen in range(GENERATIONS):
        fitness_scores = [calculate_fitness(ind) for ind in population]

        best_score = max(fitness_scores)
        best_individual = population[np.argmax(fitness_scores)]

        if gen % 20 == 0 or gen == GENERATIONS - 1:
            print(f"Generation {gen}: Best Sharpe Ratio = {best_score:.4f}")

        new_population = []

        sorted_indices = np.argsort(fitness_scores)[::-1]
        for i in range(ELITISM_COUNT):
            new_population.append(population[sorted_indices[i]])

        while len(new_population) < POPULATION_SIZE:
            p1 = selection(population, fitness_scores)
            p2 = selection(population, fitness_scores)
            child = crossover(p1, p2)
            child = mutation(child)
            new_population.append(child)

        population = new_population

    return best_individual, best_score


best_weights, best_sharpe = run_evolution()

print("\n--- РЕЗУЛЬТАТИ ОПТИМІЗАЦІЇ ---")
print(f"Найкращий коефіцієнт Шарпа: {best_sharpe:.4f}")
print("Оптимальний розподіл активів:")
for asset, weight in zip(ASSETS, best_weights):
    print(f"  {asset}: {weight * 100:.2f}%")

final_ret = np.sum(best_weights * EXPECTED_RETURNS)
final_vol = np.sqrt(np.dot(best_weights.T, np.dot(COVARIANCE_MATRIX, best_weights)))
print(f"\nОчікувана прибутковість: {final_ret * 100:.2f}%")
print(f"Ризик (волатильність): {final_vol * 100:.2f}%")
