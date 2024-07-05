import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import argparse

# Grid size
WIDTH, HEIGHT = 100, 100

# Plant and herbivore settings
INITIAL_PLANTS = 300
INITIAL_HERBIVORES = 20
PLANT_GROWTH_RATE = 0.01
HERBIVORE_ENERGY_INIT = 20
HERBIVORE_REPRODUCE_ENERGY = 30
ENERGY_FROM_PLANT = 10

# Directions for movement
DIRECTIONS = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])

class Ecosystem:
    def __init__(self):
        self.grid = np.zeros((WIDTH, HEIGHT), dtype=int)
        self.plants = {(np.random.randint(WIDTH), np.random.randint(HEIGHT)) for _ in range(INITIAL_PLANTS)}
        self.herbivores = [{'position': (np.random.randint(WIDTH), np.random.randint(HEIGHT)), 'energy': HERBIVORE_ENERGY_INIT}
                           for _ in range(INITIAL_HERBIVORES)]
    
    def step(self):
        # Grow new plants
        for _ in range(int(WIDTH * HEIGHT * PLANT_GROWTH_RATE)):
            self.plants.add((np.random.randint(WIDTH), np.random.randint(HEIGHT)))

        # Move herbivores
        new_herbivores = []
        for herbivore in self.herbivores:
            direction = DIRECTIONS[np.random.randint(4)]
            new_position = ((herbivore['position'][0] + direction[0]) % WIDTH, (herbivore['position'][1] + direction[1]) % HEIGHT)

            if new_position in self.plants:
                herbivore['energy'] += ENERGY_FROM_PLANT
                self.plants.remove(new_position)
            
            herbivore['energy'] -= 1
            if herbivore['energy'] > 0:
                new_herbivores.append(herbivore)
                
                # Reproduction
                if herbivore['energy'] >= HERBIVORE_REPRODUCE_ENERGY:
                    new_herbivores.append({'position': herbivore['position'], 'energy': HERBIVORE_ENERGY_INIT})
                    herbivore['energy'] -= 10
            
            herbivore['position'] = new_position
        
        self.herbivores = new_herbivores

    def animate(self, i):
        self.step()  # Update the ecosystem state
        plt.cla()  # Clear the current axes
        herb_positions = [h['position'] for h in self.herbivores]
        if self.plants:
            plt.scatter(*zip(*self.plants), color='green', s=10, label='Plants')
        if herb_positions:
            plt.scatter(*zip(*herb_positions), color='blue', s=10, label='Herbivores')
        plt.xlim(0, WIDTH)
        plt.ylim(0, HEIGHT)
        plt.title(f"Step: {i+1}")
        plt.legend()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the ecosystem simulation.")
    parser.add_argument("--steps", type=int, default=200, help="Number of steps for the simulation")
    args = parser.parse_args()

    STEPS = args.steps

    ecosystem = Ecosystem()
    fig = plt.figure()
    ani = animation.FuncAnimation(fig, ecosystem.animate, frames=STEPS, repeat=False)
    plt.show()
