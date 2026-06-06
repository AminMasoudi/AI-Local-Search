from functools import lru_cache

from env.utils import random_position
from search.local_search_base import LocalSearchBase
from search.state import State


class HillClimbing(LocalSearchBase):
    def run(self, initial_state, **kwargs):
        """
        TODO: Implement the Hill Climbing algorithm.

        Parameters
        ----------
        initial_state : list of tuples
            The initial configuration of sensors.
        **kwargs :
            Define and add any other parameters you might need for the algorithm

        Returns
        -------
        best_state : list of tuples
            The best configuration found.
        best_cost : int or float
            The cost of the best configuration.
        evaluations : list
            List of costs at each iteration (used for plotting).
        states_history : list of lists
            List of states at each iteration (used for animation).
        """        
        current = initial_state
        self.state_history = [list(current.locations)]
        cost_history = [self.heuristic(current)]
        i = 0
        while i < 100:
            successors = self.get_neighbor(current)
            new_state = max(successors, key=lambda x: self.heuristic(x))
            if cost_history[-1] > self.heuristic(new_state) or cost_history[-1] == 100:
                break
            current = new_state
            self.state_history.append(list(current.locations))
            cost_history.append(self.heuristic(current))
            i += 1
        return (
            self.state_history[-1],
            self.evaluate(self.heuristic(current)),
            list(map(lambda x: self.evaluate(x), cost_history)),
            self.state_history,
        )


