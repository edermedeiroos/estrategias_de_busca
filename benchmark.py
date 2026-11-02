"""
Benchmarking e geracao de graficos comparativos entre BFS e A*.
"""

import time
import tracemalloc
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import numpy as np

from src.problem import SamplingProblem
from src.heuristics import SamplingHeuristic
from src.search import breadth_first_search, a_star_search, SearchResult


CASES = [
    ("Moderado (6x6, 2 silobags)", "casos_de_teste/caso_1_moderado.txt"),
    ("Intermediario (10x10, 4 silobags)", "casos_de_teste/caso_2_intermediario.txt"),
    ("Complexo (14x14, 6 silobags)", "casos_de_teste/caso_3_complexo.txt"),
]


def run_benchmark(num_runs: int = 5) -> Dict[str, Any]:
    benchmark_data: Dict[str, Any] = {
        "cases": [],
        "bfs": {"expanded": [], "generated": [], "frontier": [], "time_ms": [], "memory_kb": [], "cost": []},
        "astar": {"expanded": [], "generated": [], "frontier": [], "time_ms": [], "memory_kb": [], "cost": []},
    }

    print("=" * 70)
    print("Benchmarking: BFS vs A*")
    print(f"Repeticoes por caso: {num_runs}")
    print("=" * 70)

    for label, path in CASES:
        prob = SamplingProblem.from_file(path)
        heur = SamplingHeuristic(prob)
        benchmark_data["cases"].append(label)

        # BFS
        bfs_times = []
        bfs_res: SearchResult = None
        for _ in range(num_runs):
            res = breadth_first_search(prob)
            bfs_times.append(res.time_seconds * 1000.0)
            if bfs_res is None:
                bfs_res = res

        avg_bfs_time = float(np.mean(bfs_times))
        benchmark_data["bfs"]["cost"].append(bfs_res.cost)
        benchmark_data["bfs"]["expanded"].append(bfs_res.nodes_expanded)
        benchmark_data["bfs"]["generated"].append(bfs_res.nodes_generated)
        benchmark_data["bfs"]["frontier"].append(bfs_res.max_frontier_size)
        benchmark_data["bfs"]["time_ms"].append(avg_bfs_time)
        benchmark_data["bfs"]["memory_kb"].append(bfs_res.memory_kb)

        # A*
        astar_times = []
        astar_res: SearchResult = None
        for _ in range(num_runs):
            res = a_star_search(prob, heur)
            astar_times.append(res.time_seconds * 1000.0)
            if astar_res is None:
                astar_res = res

        avg_astar_time = float(np.mean(astar_times))
        benchmark_data["astar"]["cost"].append(astar_res.cost)
        benchmark_data["astar"]["expanded"].append(astar_res.nodes_expanded)
        benchmark_data["astar"]["generated"].append(astar_res.nodes_generated)
        benchmark_data["astar"]["frontier"].append(astar_res.max_frontier_size)
        benchmark_data["astar"]["time_ms"].append(avg_astar_time)
        benchmark_data["astar"]["memory_kb"].append(astar_res.memory_kb)

        print(f"\n[{label}]")
        print(f"  Custo: {astar_res.cost}")
        print(f"  BFS -> Nos: {bfs_res.nodes_expanded:5d} | Tempo: {avg_bfs_time:6.2f} ms | Memoria: {bfs_res.memory_kb:7.2f} KB")
        print(f"  A*  -> Nos: {astar_res.nodes_expanded:5d} | Tempo: {avg_astar_time:6.2f} ms | Memoria: {astar_res.memory_kb:7.2f} KB")
        red_nodes = (1.0 - astar_res.nodes_expanded / bfs_res.nodes_expanded) * 100.0
        red_mem = (1.0 - astar_res.memory_kb / bfs_res.memory_kb) * 100.0
        speedup = avg_bfs_time / max(avg_astar_time, 1e-4)
        print(f"  Reducao nos: {red_nodes:.1f}% | Reducao memoria: {red_mem:.1f}% | Speedup: {speedup:.2f}x")

    return benchmark_data


def plot_charts(data: Dict[str, Any], output_path: str = "graficos_desempenho.png") -> None:
    cases = ["Moderado", "Intermediario", "Complexo"]
    x = np.arange(len(cases))
    width = 0.35

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
    plt.subplots_adjust(wspace=0.3)

    # 1. Nos Expandidos
    ax1 = axes[0]
    ax1.bar(x - width/2, data["bfs"]["expanded"], width, label="BFS", color="#2b5c8f")
    ax1.bar(x + width/2, data["astar"]["expanded"], width, label="A*", color="#388e3c")
    ax1.set_ylabel("Nos Expandidos (Escala Log)")
    ax1.set_title("Nos Expandidos")
    ax1.set_xticks(x)
    ax1.set_xticklabels(cases)
    ax1.set_yscale("log")
    ax1.grid(True, linestyle="--", alpha=0.5, which="both")
    ax1.legend()

    # 2. Tempo de Execucao (ms)
    ax2 = axes[1]
    ax2.bar(x - width/2, data["bfs"]["time_ms"], width, label="BFS", color="#2b5c8f")
    ax2.bar(x + width/2, data["astar"]["time_ms"], width, label="A*", color="#388e3c")
    ax2.set_ylabel("Tempo (ms)")
    ax2.set_title("Tempo Medio de Execucao")
    ax2.set_xticks(x)
    ax2.set_xticklabels(cases)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend()

    # 3. Memoria (KB)
    ax3 = axes[2]
    ax3.bar(x - width/2, data["bfs"]["memory_kb"], width, label="BFS", color="#2b5c8f")
    ax3.bar(x + width/2, data["astar"]["memory_kb"], width, label="A*", color="#388e3c")
    ax3.set_ylabel("Memoria Pico (KB)")
    ax3.set_title("Consumo de Memoria")
    ax3.set_xticks(x)
    ax3.set_xticklabels(cases)
    ax3.grid(True, linestyle="--", alpha=0.5)
    ax3.legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)


def main() -> None:
    data = run_benchmark(num_runs=5)
    plot_charts(data, output_path="graficos_desempenho.png")


if __name__ == "__main__":
    main()
