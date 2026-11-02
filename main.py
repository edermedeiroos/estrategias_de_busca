"""
Ponto de entrada principal para execução e visualização do Trabalho Prático 1.
Permite executar casos de teste específicos ou todos os casos em lote,
comparando a Busca em Largura (BFS) e a Busca Heurística A*.
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

    print("\nVisualização do Pátio e Trajetória Percorrida:")
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
    print("  Legenda: S = Início | L = Laboratório | B = Silobag | # = Obstáculo | · = Rota percorrida\n")


def run_instance(filepath: str, algorithm: str = "ambos", visualize: bool = False) -> None:
    problem = SamplingProblem.from_file(filepath)
    heuristic = SamplingHeuristic(problem)

    print(f"\n{'='*75}")
    print(f"Instância: {filepath}")
    print(f"Dimensões do Pátio: {problem.height}x{problem.width} | Total de Silobags (Alvos): {problem.num_targets}")
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
            print(f"Status: Solução encontrada com SUCESSO!")
            print(f"Custo total ótimo: {res.cost} movimentos")
            print(f"Nós expandidos (visitados): {res.nodes_expanded}")
            print(f"Nós gerados (fronteira): {res.nodes_generated}")
            print(f"Fronteira máxima na memória: {res.max_frontier_size} nós")
            print(f"Tempo de execução: {res.time_seconds * 1000:.2f} ms")
            print(f"Pico de memória alocada: {res.memory_kb:.2f} KB")
            print(f"Primeiros movimentos: {format_path(res.solution[:10])} ... ({len(res.solution)} ações no total)")
        else:
            print("Status: Falha ao encontrar solução.")

    if visualize and results and results[-1].path:
        render_grid_path(problem, results[-1].path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="2COP015 - Inteligência Artificial - Trabalho Prático 1"
    )
    parser.add_argument(
        "--caso",
        type=str,
        default=None,
        help="Caminho para o arquivo de caso de teste específico (ex: casos_de_teste/caso_1_moderado.txt)",
    )
    parser.add_argument(
        "--todos",
        action="store_true",
        help="Executa automaticamente os três casos de teste (moderado, intermediário e complexo)",
    )
    parser.add_argument(
        "--algoritmo",
        choices=["bfs", "astar", "ambos"],
        default="ambos",
        help="Estratégia de busca a executar: bfs, astar ou ambos (padrão)",
    )
    parser.add_argument(
        "--visualizar",
        action="store_true",
        help="Exibe a representação visual da rota percorrida na grade do pátio",
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
        # Por padrão, roda os três casos com visualização resumida
        print("Executando os três casos de teste padrão (use --help para opções):")
        for case in default_cases:
            run_instance(case, algorithm=args.algoritmo, visualize=args.visualizar)


if __name__ == "__main__":
    main()
