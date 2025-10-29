import numpy as np


class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size))

    def train(self, patterns):
        patterns_matrix = np.array(patterns)
        # W = (1/N) * Σ(p * p^T)
        self.weights = (1 / len(patterns)) * patterns_matrix.T @ patterns_matrix
        np.fill_diagonal(self.weights, 0)

    def predict(self, pattern, max_iter=20):
        current_pattern = np.array(pattern).copy()
        print("Початковий (спотворений) патерн:")
        self.print_pattern(current_pattern)
        for i in range(max_iter):
            print(f"\nІтерація {i + 1}:")
            random_neuron_index = np.random.randint(self.size)
            activation = self.weights[random_neuron_index, :] @ current_pattern  # Async
            current_pattern[random_neuron_index] = 1 if activation >= 0 else -1
            self.print_pattern(current_pattern)
        print("\nРезультат: відновлений патерн.")
        self.print_pattern(current_pattern)
        return current_pattern

    @staticmethod
    def print_pattern(pattern):
        side = int(np.sqrt(len(pattern)))
        if side * side != len(pattern):
            print(pattern)
            return
        for i in range(side):
            for j in range(side):
                print("#" if pattern[i * side + j] == 1 else " ", end=" ")
            print()


# 5x5
pattern_X = [
    1,
    -1,
    -1,
    -1,
    1,
    -1,
    1,
    -1,
    1,
    -1,
    -1,
    -1,
    1,
    -1,
    -1,
    -1,
    1,
    -1,
    1,
    -1,
    1,
    -1,
    -1,
    -1,
    1,
]

pattern_O = [
    -1,
    1,
    1,
    1,
    -1,
    1,
    -1,
    -1,
    -1,
    1,
    1,
    -1,
    -1,
    -1,
    1,
    1,
    -1,
    -1,
    -1,
    1,
    -1,
    1,
    1,
    1,
    -1,
]

pattern_T = [
    1,
    1,
    1,
    1,
    1,
    -1,
    -1,
    1,
    -1,
    -1,
    -1,
    -1,
    1,
    -1,
    -1,
    -1,
    -1,
    1,
    -1,
    -1,
    -1,
    -1,
    1,
    -1,
    -1,
]

# pattern_X = [
#     [1, -1, -1, -1, 1],
#     [-1, 1, -1, 1, -1],
#     [-1, -1, 1, -1, -1],
#     [-1, 1, -1, 1, -1],
#     [1, -1, -1, -1, 1],
# ]

# pattern_O = [
#     [-1, 1, 1, 1, -1],
#     [1, -1, -1, -1, 1],
#     [1, -1, -1, -1, 1],
#     [1, -1, -1, -1, 1],
#     [-1, 1, 1, 1, -1],
# ]

# pattern_T = [
#     [1, 1, 1, 1, 1],
#     [-1, -1, 1, -1, -1],
#     [-1, -1, 1, -1, -1],
#     [-1, -1, 1, -1, -1],
#     [-1, -1, 1, -1, -1],
# ]

network = HopfieldNetwork(size=25)
network.train([pattern_X, pattern_O, pattern_T])

print("Мережу навчено на патернах X, O, T.")
print("Патерн X:")
network.print_pattern(pattern_X)
print("\nПатерн O:")
network.print_pattern(pattern_O)
print("\nПатерн T:")
network.print_pattern(pattern_T)


distorted_X = list(pattern_X)
distorted_X[6] = 1
distorted_X[8] = -1
distorted_X[12] = -1

restored_pattern = network.predict(distorted_X, max_iter=20)
