"""
Implementacao dos algoritmos de busca: Busca em Largura (BFS) e A*.
"""

import time
import tracemalloc
from collections import deque
import heapq
from typing import Optional, List, Dict, Callable, Tuple
from src.problem import State, SamplingProblem


class Node:
    __slots__ = ("state", "parent", "action", "g", "h", "f", "depth")

    def __init__(
        self,
        state: State,
        parent: Optional["Node"] = None,
        action: Optional[str] = None,
        g: int = 0,
        h: int = 0,
    ):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h
        self.f = g + h
        self.depth = (parent.depth + 1) if parent else 0


class SearchResult:
    def __init__(
        self,
        algorithm: str,
        solution: Optional[List[str]],
        path: Optional[List[State]],
        cost: int,
        nodes_expanded: int,
        nodes_generated: int,
        max_frontier_size: int,
        time_seconds: float,
        memory_kb: float,
    ):
        self.algorithm = algorithm
        self.solution = solution
        self.path = path
        self.cost = cost
        self.nodes_expanded = nodes_expanded
        self.nodes_generated = nodes_generated
        self.max_frontier_size = max_frontier_size
        self.time_seconds = time_seconds
        self.memory_kb = memory_kb

    def __repr__(self) -> str:
        status = f"Custo: {self.cost}" if self.solution is not None else "Falha"
        return (
            f"[{self.algorithm}] {status} | Passos: {len(self.solution or [])} | "
            f"Expandidos: {self.nodes_expanded} | Gerados: {self.nodes_generated} | "
            f"Fronteira Max: {self.max_frontier_size} | "
            f"Tempo: {self.time_seconds * 1000:.2f}ms | Memoria: {self.memory_kb:.2f} KB"
        )


def _reconstruct_path(node: Node) -> Tuple[List[str], List[State]]:
    actions = []
    states = []
    curr = node
    while curr:
        states.append(curr.state)
        if curr.action is not None:
            actions.append(curr.action)
        curr = curr.parent
    actions.reverse()
    states.reverse()
    return actions, states


def breadth_first_search(problem: SamplingProblem) -> SearchResult:
    tracemalloc.start()
    start_time = time.perf_counter()

    root = Node(problem.initial_state())
    frontier = deque([root])
    frontier_states = {root.state}
    explored = set()

    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1
    solution_node = None

    while frontier:
        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)

        node = frontier.popleft()
        frontier_states.remove(node.state)

        if problem.is_goal(node.state):
            solution_node = node
            break

        explored.add(node.state)
        nodes_expanded += 1

        for action in problem.actions(node.state):
            next_state = problem.result(node.state, action)
            if next_state not in explored and next_state not in frontier_states:
                child = Node(
                    state=next_state,
                    parent=node,
                    action=action,
                    g=node.g + 1,
                )
                nodes_generated += 1
                frontier.append(child)
                frontier_states.add(next_state)

    elapsed_time = time.perf_counter() - start_time
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if solution_node:
        actions, path = _reconstruct_path(solution_node)
        cost = solution_node.g
    else:
        actions, path, cost = None, None, -1

    return SearchResult(
        algorithm="Busca em Largura (BFS)",
        solution=actions,
        path=path,
        cost=cost,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        max_frontier_size=max_frontier_size,
        time_seconds=elapsed_time,
        memory_kb=peak_memory / 1024.0,
    )


def a_star_search(
    problem: SamplingProblem, heuristic: Callable[[State], int]
) -> SearchResult:
    tracemalloc.start()
    start_time = time.perf_counter()

    root_state = problem.initial_state()
    root_h = heuristic(root_state)
    root = Node(state=root_state, g=0, h=root_h)

    # heapq: (f, -g, counter, node)
    counter = 0
    frontier = [(root.f, -root.g, counter, root)]
    best_g: Dict[State, int] = {root_state: 0}

    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1
    solution_node = None

    while frontier:
        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)

        f, neg_g, _, node = heapq.heappop(frontier)

        if node.g > best_g.get(node.state, float("inf")):
            continue

        if problem.is_goal(node.state):
            solution_node = node
            break

        nodes_expanded += 1

        for action in problem.actions(node.state):
            next_state = problem.result(node.state, action)
            new_g = node.g + 1

            if new_g < best_g.get(next_state, float("inf")):
                best_g[next_state] = new_g
                h_val = heuristic(next_state)
                child = Node(
                    state=next_state,
                    parent=node,
                    action=action,
                    g=new_g,
                    h=h_val,
                )
                nodes_generated += 1
                counter += 1
                heapq.heappush(frontier, (child.f, -child.g, counter, child))

    elapsed_time = time.perf_counter() - start_time
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if solution_node:
        actions, path = _reconstruct_path(solution_node)
        cost = solution_node.g
    else:
        actions, path, cost = None, None, -1

    return SearchResult(
        algorithm="Busca Heuristica A*",
        solution=actions,
        path=path,
        cost=cost,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        max_frontier_size=max_frontier_size,
        time_seconds=elapsed_time,
        memory_kb=peak_memory / 1024.0,
    )
