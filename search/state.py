from dataclasses import dataclass

from env.grid_world import GridWorld


@dataclass(frozen=True)
class State:
    locations: tuple[int, int]

    def covered(self, world: GridWorld) -> set[tuple[int, int]]:
        covered_locations = set()
        for loc in self.locations:
            x, y = loc
            covered_locations = covered_locations.union(
                self.covered_point(x, y, world.sensor_range)
            )
        return covered_locations

    @staticmethod
    def covered_point(x: int, y: int, n: int) -> set[tuple[int, int]]:
        covered = set()
        for i in range(-n, n + 1):
            for j in range(-n, n + 1):
                if abs(i) + abs(j) <= n:
                    covered.add((x + i, y + j))
        return covered

