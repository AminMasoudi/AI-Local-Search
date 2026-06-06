import math
import random

from search.local_search_base import LocalSearchBase


class SimulatedAnnealing(LocalSearchBase):
    __repr_name__ = "Simulated Annealing"

    def run(self, initial_state, **kwargs):
        """
        TODO: Implement the Simulated Annealing algorithm.

        Parameters
        ----------
        initial_state : list of tuples
            The initial configuration of sensors.
        **kwargs :
            Define and add all necessary parameters required for Simulated Annealing

        Returns
        -------
        best_state : list of tuples
        best_cost : int or float
        evaluations : list
        states_history : list of lists
        """
        current = initial_state
        current_score = self.heuristic(current)

        best = current
        best_score = current_score

        self.state_history = [list(current.locations)]
        cost_history = [current_score]

        t = kwargs.get("temperature", 100)
        cooling = kwargs.get("cooling", 0.95)
        min_t = kwargs.get("min_temperature", 0.1)

        while t > min_t:

            successors = self.get_neighbor(current)

            next_state = random.choice(list(successors))
            next_score = self.heuristic(next_state)

            delta = next_score - current_score

            if delta > 0:
                current = next_state
                current_score = next_score

            else:
                p = math.exp(delta / t)

                if random.random() < p:
                    current = next_state
                    current_score = next_score

            if current_score > best_score:
                best = current
                best_score = current_score

            self.state_history.append(list(current.locations))
            cost_history.append(current_score)

            # cool down
            t *= cooling

        return (
            list(best.locations),
            self.evaluate(best_score),
            list(map(lambda x: self.evaluate(x), cost_history)),
            self.state_history,
        )
