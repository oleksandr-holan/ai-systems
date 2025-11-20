import random
import matplotlib.pyplot as plt
import numpy as np

NUM_AGENTS = 100
STEPS = 2000
CONFIDENCE_THRESHOLD = 0.3
CONVERGENCE_SPEED = 0.7

class Agent:
    def __init__(self, id):
        self.id = id
        self.opinion = random.random()

class SocialNetworkModel:
    def __init__(self, num_agents, threshold, speed):
        self.agents = [Agent(i) for i in range(num_agents)]
        self.threshold = threshold
        self.speed = speed
        self.history = []

    def step(self):
        current_opinions = [agent.opinion for agent in self.agents]
        self.history.append(current_opinions)

        agent_a = random.choice(self.agents)
        agent_b = random.choice(self.agents)
        
        if agent_a.id == agent_b.id:
            return

        diff = abs(agent_a.opinion - agent_b.opinion)
        
        if diff < self.threshold:
            new_opinion_a = agent_a.opinion + self.speed * (agent_b.opinion - agent_a.opinion)
            new_opinion_b = agent_b.opinion + self.speed * (agent_a.opinion - agent_b.opinion)
            
            agent_a.opinion = new_opinion_a
            agent_b.opinion = new_opinion_b

    def run(self, steps):
        print(f"Запуск симуляції: {steps} кроків...")
        for _ in range(steps):
            self.step()
        print("Симуляцію завершено.")

    def plot_results(self):
        data = np.array(self.history).T 
        
        plt.figure(figsize=(10, 6))
        for agent_opinions in data:
            plt.plot(range(len(self.history)), agent_opinions, linewidth=0.5, alpha=0.6)
            
        plt.title(f'Динаміка думок у соціальній мережі\nПоріг довіри: {self.threshold}, Агентів: {len(self.agents)}')
        plt.xlabel('Час (взаємодії)')
        plt.ylabel('Думка (0.0 - Лівий спектр, 1.0 - Правий спектр)')
        plt.grid(True, alpha=0.3)
        plt.show()

if __name__ == "__main__":
    model = SocialNetworkModel(num_agents=NUM_AGENTS, threshold=CONFIDENCE_THRESHOLD, speed=CONVERGENCE_SPEED)
    model.run(STEPS)
    model.plot_results()