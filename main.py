"""
Execucao e comparacao dos algoritmos BFS e A* nas instancias de teste.
"""

import sys
import argparse
from typing import List, Tuple
from src.problem import SamplingProblem, State
from src.heuristics import SamplingHeuristic
from src.search import breadth_first_search, a_star_search, SearchResult


def format_path(actions: List[str]) -> str:
    if not actions:
        return "Nenhum movimento."
    return " -> ".join(actions)


def render_grid_path(problem: SamplingProblem, path: List[State]) -> None:
    path_coords = {(s.r, s.c) for s in path}
    target_set = set(problem.targets)

    print("\nVisualizacao da rota:")
    for r in range(problem.height):
        row_str = []
        for c in range(problem.width):
            pos = (r, c)
            if pos == problem.start:
                row_str.append("S")
            elif pos == problem.lab:
                row_str.append("L")
            elif pos in target_set:
                row_str.append("B")
            elif pos in problem.obstacles:
                row_str.append("#")
            elif pos in path_coords:
                row_str.append("·")
            else:
                row_str.append(" ")
        print("  " + " ".join(row_str))
    print("  Legenda: S = Inicio | L = Laboratorio | B = Silobag | # = Obstaculo | · = Rota percorrida\n")


def run_instance(filepath: str, algorithm: str = "ambos", visualize: bool = False) -> None:
    problem = SamplingProblem.from_file(filepath)
    heuristic = SamplingHeuristic(problem)

    print(f"\n{'='*75}")
    print(f"Instancia: {filepath}")
    print(f"Dimensoes: {problem.height}x{problem.width} | Silobags (Alvos): {problem.num_targets}")
    print(f"{'='*75}")

    results: List[SearchResult] = []

    if algorithm in ("bfs", "ambos"):
        res_bfs = breadth_first_search(problem)
        results.append(res_bfs)

    if algorithm in ("astar", "ambos"):
        res_astar = a_star_search(problem, heuristic)
        results.append(res_astar)

    for res in results:
        print(f"\n--- {res.algorithm} ---")
        if res.solution is not None:
            print(f"Status: Solucao encontrada")
            print(f"Custo total: {res.cost} movimentos")
            print(f"Nos expandidos: {res.nodes_expanded}")
            print(f"Nos gerados: {res.nodes_generated}")
            print(f"Fronteira maxima: {res.max_frontier_size}")
            print(f"Tempo de execucao: {res.time_seconds * 1000:.2f} ms")
            print(f"Memoria de pico: {res.memory_kb:.2f} KB")
            print(f"Primeiros movimentos: {format_path(res.solution[:10])} ... ({len(res.solution)} acoes no total)")
        else:
            print("Status: Falha ao encontrar solucao.")

    if visualize and results and results[-1].path:
        render_grid_path(problem, results[-1].path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="2COP015 - Inteligencia Artificial - Trabalho 1"
    )
    parser.add_argument(
        "--caso",
        type=str,
        default=None,
        help="Caminho para arquivo de teste especifico",
    )
    parser.add_argument(
        "--todos",
        action="store_true",
        help="Executa os tres casos de teste (moderado, intermediario e complexo)",
    )
    parser.add_argument(
        "--algoritmo",
        choices=["bfs", "astar", "ambos"],
        default="ambos",
        help="Estrategia: bfs, astar ou ambos (padrao)",
    )
    parser.add_argument(
        "--visualizar",
        action="store_true",
        help="Exibe a rota na grade",
    )

    args = parser.parse_args()

    default_cases = [
        "casos_de_teste/caso_1_moderado.txt",
        "casos_de_teste/caso_2_intermediario.txt",
        "casos_de_teste/caso_3_complexo.txt",
    ]

    if args.todos:
        for case in default_cases:
            run_instance(case, algorithm=args.algoritmo, visualize=args.visualizar)
    elif args.caso:
        run_instance(args.caso, algorithm=args.algoritmo, visualize=args.visualizar)
    else:
        for case in default_cases:
            run_instance(case, algorithm=args.algoritmo, visualize=args.visualizar)


if __name__ == "__main__":
    main()
