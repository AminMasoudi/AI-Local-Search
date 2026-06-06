from abc import ABC, abstractmethod
from functools import lru_cache

from env.grid_world import GridWorld
from env.utils import random_position
from search.state import State


class LocalSearchBase:

    world: GridWorld

    def __init__(self, world):
        self.world = world

    def evaluate(self, score: float):
        """
        TODO: Implement the evaluation (Cost) function.

        Design a function that calculates the cost of the current sensor placement.
        Refer to the project documentation for the primary objectives and constraints.

        Returns:
            cost (int or float): The evaluated cost of the state (lower is better).
        """
        return 100 - score

    def get_neighbor(self, state: State) -> set[State]:
        """
        TODO: Implement the neighbor generation function.

        Generate a new valid state by applying a local change to the current state.
        Ensure you include all the required operations mentioned in the project PDF
        to support a dynamic search space.

        Returns:
            neighbor_state (list of tuples): The newly generated valid state.
        """
        neigh_states = set()
        for x, y in state.locations:
            other_locations = set(
                filter(lambda loc: not (loc[0] == x and loc[1] == y), state.locations)
            )

            new_neigh_states = set(
                [
                    State(
                        locations=frozenset(other_locations.union({new_loc})),
                    )
                    for new_loc in State.covered_point(x, y, self.world.sensor_range)
                    if new_loc not in other_locations
                    and self.world.is_valid_position(new_loc[0], new_loc[1])
                ]
            )
            new_neigh_states = set(
                filter(
                    lambda new: list(new.locations) not in self.state_history,
                    new_neigh_states,
                )
            )
            neigh_states = neigh_states.union(new_neigh_states)

        if self.world.max_sensors > len(state.locations):
            new_sensor_loc = max(
                set(filter(lambda loc: loc not in state.locations, self.grid_world())),
                key=lambda loc: self.point_heuristic(loc[0], loc[1], state),
            )
            neigh_states.add(
                State(locations=state.locations.union({new_sensor_loc}))
            )
        return neigh_states

    @staticmethod
    def initialize_state(world: GridWorld):
        """
        Create a starting configuration of sensors within the grid boundaries,
        respecting the maximum sensor limits and obstacle placements.

        Returns:
            initial_state (list of tuples): The starting coordinates of the sensors.
        """
        return State(locations=frozenset([random_position(world)]))

    def heuristic(self, state: State) -> float:
        targets = self.world.get_targets()
        covered = state.covered(self.world)
        return len(list(filter(lambda x: x in covered, targets))) * 100 / len(targets)

    @lru_cache
    def point_heuristic(self, x: int, y: int, state: State) -> int:
        covered = State.covered_point(x, y, self.world.sensor_range)
        targets = self.world.get_targets()
        return len(
            list(
                filter(
                    lambda x: x in covered and x not in state.covered(self.world),
                    targets,
                )
            )
        )

    @lru_cache
    def grid_world(self):
        return [
            (i, j)
            for i in range(self.world.rows)
            for j in range(self.world.cols)
            if self.world.is_valid_position(i, j)
        ]
