"""
Calculo da heuristica admissivel (Manhattan + MST via Prim).
"""

from typing import List, Tuple, Dict
from src.problem import State, SamplingProblem


def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class SamplingHeuristic:
    def __init__(self, problem: SamplingProblem):
        self.problem = problem
        self.targets = problem.targets
        self.num_targets = problem.num_targets
        self.lab = problem.lab
        self.mst_cache: Dict[int, int] = {}
        self.min_to_lab_cache: Dict[int, int] = {}
        self._precompute_mst_cache()

    def _compute_mst(self, points: List[Tuple[int, int]]) -> int:
        if len(points) <= 1:
            return 0

        # MST via Prim
        n = len(points)
        visited = [False] * n
        min_cost = [float("inf")] * n
        min_cost[0] = 0
        total_mst = 0

        for _ in range(n):
            u = -1
            best_val = float("inf")
            for i in range(n):
                if not visited[i] and min_cost[i] < best_val:
                    best_val = min_cost[i]
                    u = i

            visited[u] = True
            total_mst += int(best_val)

            for v in range(n):
                if not visited[v]:
                    dist = manhattan_distance(points[u], points[v])
                    if dist < min_cost[v]:
                        min_cost[v] = dist

        return total_mst

    def _precompute_mst_cache(self) -> None:
        total_subsets = 1 << self.num_targets
        for mask in range(total_subsets):
            points = [
                self.targets[i]
                for i in range(self.num_targets)
                if (mask & (1 << i))
            ]
            self.mst_cache[mask] = self._compute_mst(points)

            if points:
                self.min_to_lab_cache[mask] = min(
                    manhattan_distance(p, self.lab) for p in points
                )
            else:
                self.min_to_lab_cache[mask] = 0

    def __call__(self, state: State) -> int:
        remaining_mask = self.problem.goal_mask ^ state.collected
        pos = (state.r, state.c)

        if remaining_mask == 0:
            return manhattan_distance(pos, self.lab)

        min_agent_to_target = min(
            manhattan_distance(pos, self.targets[i])
            for i in range(self.num_targets)
            if (remaining_mask & (1 << i))
        )

        mst_val = self.mst_cache[remaining_mask]
        min_target_to_lab = self.min_to_lab_cache[remaining_mask]

        return min_agent_to_target + mst_val + min_target_to_lab
