"""
University: University of Isfahan
Faculty: Mathematics and Statistics
Branch: Computer Science
Course: Artificial Intelligence
Professor: Dr. Faria Nasiri Mofakham
TAs: MehrAzin Marzough, Mohammad Karimi, Anahita Honarmandian
Project: Implementing Local Search Algorithms for a Sensor Placement Optimization Problem
"""

from env.grid_world import GridWorld
from search import HillClimbing, SimulatedAnnealing
from utils import represent

import re
import matplotlib

matplotlib.use("TkAgg")


def run_algorithms(world, initial_state, algorithm_classes):
    best_states = []
    best_costs = []
    evaluations = []
    histories = []
    names = []

    for algorithm_class in algorithm_classes:
        # Format class name for presentation (e.g., HillClimbing -> Hill Climbing)

        names.append(algorithm_class.__repr_name__)

        # Instantiate the algorithm
        algorithm_instance = algorithm_class(world)

        print(f"\nRunning {algorithm_class.__repr_name__}...")

        best_state, best_cost, evaluation, states_history = algorithm_instance.run(
            initial_state
        )

        best_states.append(best_state)
        best_costs.append(best_cost)
        evaluations.append(evaluation)
        histories.append(states_history)

    represent(
        best_states=best_states,
        best_costs=best_costs,
        evaluations=evaluations,
        histories=histories,
        names=names,
        world=world,
    )


if __name__ == "__main__":

    world = GridWorld("map1")

    algorithm_classes = [HillClimbing, SimulatedAnnealing]

    initial_state = HillClimbing.initialize_state(world)

    run_algorithms(world, initial_state, algorithm_classes)
