"""
Modelagem do Problema de Roteamento para Coleta e Amostragem de Grãos
em Pátio de Silobags (Grain Sampling & Inspection Routing Problem).
"""

from typing import NamedTuple, List, Tuple, Set, Dict


class State(NamedTuple):
    r: int
    c: int
    collected: int  # Bitmask indicando quais silobags já foram amostradas


class Action:
    UP = "CIMA"
    DOWN = "BAIXO"
    LEFT = "ESQUERDA"
    RIGHT = "DIREITA"

    DELTAS = {
        UP: (-1, 0),
        DOWN: (1, 0),
        LEFT: (0, -1),
        RIGHT: (0, 1),
    }


class SamplingProblem:
    def __init__(self, grid_lines: List[str]):
        self.height = len(grid_lines)
        self.width = len(grid_lines[0]) if self.height > 0 else 0

        self.obstacles: Set[Tuple[int, int]] = set()
        self.targets: List[Tuple[int, int]] = []
        self.target_indices: Dict[Tuple[int, int], int] = {}
        self.start: Tuple[int, int] = (0, 0)
        self.lab: Tuple[int, int] = (0, 0)

        self._parse_grid(grid_lines)
        self.num_targets = len(self.targets)
        self.goal_mask = (1 << self.num_targets) - 1

    def _parse_grid(self, lines: List[str]) -> None:
        for r, line in enumerate(lines):
            tokens = line.split()
            for c, char in enumerate(tokens):
                pos = (r, c)
                if char == "#":
                    self.obstacles.add(pos)
                elif char == "S":
                    self.start = pos
                elif char == "L":
                    self.lab = pos
                elif char == "B":
                    idx = len(self.targets)
                    self.targets.append(pos)
                    self.target_indices[pos] = idx
        if lines:
            self.width = len(lines[0].split())

    @classmethod
    def from_file(cls, filepath: str) -> "SamplingProblem":
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\r\n") for line in f if line.strip() and not line.startswith("//")]
        return cls(lines)

    def initial_state(self) -> State:
        mask = 0
        if self.start in self.target_indices:
            mask |= (1 << self.target_indices[self.start])
        return State(self.start[0], self.start[1], mask)

    def is_goal(self, state: State) -> bool:
        return state.collected == self.goal_mask and (state.r, state.c) == self.lab

    def actions(self, state: State) -> List[str]:
        valid_actions = []
        for action, (dr, dc) in Action.DELTAS.items():
            nr, nc = state.r + dr, state.c + dc
            if 0 <= nr < self.height and 0 <= nc < self.width:
                if (nr, nc) not in self.obstacles:
                    valid_actions.append(action)
        return valid_actions

    def result(self, state: State, action: str) -> State:
        dr, dc = Action.DELTAS[action]
        nr, nc = state.r + dr, state.c + dc
        new_mask = state.collected

        if (nr, nc) in self.target_indices:
            new_mask |= (1 << self.target_indices[(nr, nc)])

        return State(nr, nc, new_mask)

    def step_cost(self, state: State, action: str, next_state: State) -> int:
        return 1
