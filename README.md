# Trabalho Prático 1: Estratégias de Busca Cega e Informada
**Disciplina:** 2COP015 – Inteligência Artificial  
**Instituição:** Universidade Estadual de Londrina (CCE / Departamento de Computação)  
**Docente:** Prof. Dr. Antonio Parmezan  
**Discente:** Eder Medeiros  

---

## 1. Visão Geral do Problema

Este trabalho aborda o **Problema de Roteamento para Coleta e Amostragem de Grãos em Pátio de Silobags (Agro-TIC)**. 

No contexto da classificação de grãos e emissão de laudos de conformidade (umidade, impureza e avarias), um agente coletor autônomo deve planejar sua rota em um pátio logístico contendo obstáculos (maquinários, valas e drenos), visitar *K* silobags designadas para amostragem e entregar o material coletado no Laboratório Central de Classificação no menor número de passos possível.

### Modelagem Formal no Espaço de Estados (5-tupla)
1. **Ambiente:** Grade bidimensional $N \times M$, estática, discreta e totalmente observável.
2. **Estados ($S$):** Tuplas imutáveis `(r, c, bitmask)` representando a coordenada atual `(r, c)` e a máscara de bits indicando quais silobags já foram amostradas.
3. **Estado Inicial ($s_0$):** Posição de partida ($S$) com `bitmask = 0`.
4. **Ações e Transições:** Movimentos ortogonais (`CIMA`, `BAIXO`, `ESQUERDA`, `DIREITA`) para células válidas e livres de obstáculos (`#`). Ao ingressar na célula de uma silobag alvo, a amostragem é registrada ativando o respectivo bit da máscara.
5. **Teste de Objetivo:** O agente encontra-se nas coordenadas do Laboratório ($L$) e todas as $K$ silobags foram amostradas (`bitmask == (1 << K) - 1`).
6. **Custo do Caminho ($g$):** Custo unitário de passo ($c = 1$). O custo total é a soma dos deslocamentos realizados.

---

## 2. Estratégias de Busca Implementadas

### A) Busca Não Informada: Busca em Largura (BFS) em Grafo
* **Completude e Otimalidade:** Em espaços com custos uniformes ($c = 1$), o BFS em grafo garante completude e encontra a solução de custo ótimo (mínimo número de passos).
* **Limitação:** Complexidade de tempo e memória $O(b^d)$, expandindo nós em todas as direções de forma exaustiva.

### B) Busca Informada: Algoritmo A*
* **Função de Avaliação:** $f(n) = g(n) + h(n)$, onde $g(n)$ é o custo real acumulado e $h(n)$ é a função heurística.
* **Definição da Heurística $h(n)$:**
  $$h(n) = \min_{u \in U} d_M(\text{agente}, u) + \text{MST}(U) + \min_{u \in U} d_M(u, \text{laboratório})$$
  onde $U$ é o conjunto de silobags ainda não coletadas, $d_M$ é a distância de Manhattan e $\text{MST}(U)$ é a Árvore Geradora Mínima conectando os alvos restantes (calculada pelo algoritmo de Prim).
* **Admissibilidade e Consistência:** A distância de Manhattan e a MST são relaxações que nunca superestimam o percurso real, satisfazendo $h(n) \le h^*(n)$ e a desigualdade triangular $h(n) \le c(n, a, n') + h(n')$, o que assegura a otimalidade da solução no A*.

---

## 3. Estrutura do Repositório

```text
├── casos_de_teste/
│   ├── caso_1_moderado.txt        # Grade 6x6, 2 silobags
│   ├── caso_2_intermediario.txt   # Grade 10x10, 4 silobags
│   └── caso_3_complexo.txt        # Grade 14x14, 6 silobags
├── src/
│   ├── __init__.py
│   ├── problem.py                 # Representação de Estado, Ações e Grade
│   ├── search.py                  # Implementação de Nó, BFS e A*
│   └── heuristics.py              # Heurística de Manhattan + MST (Prim)
├── main.py                        # Execução e visualização via terminal
├── benchmark.py                   # Script de testes estatísticos e gráficos
├── gerar_relatorio.py             # Compilador do relatório em PDF (2 páginas)
├── graficos_desempenho.png        # Gráficos comparativos gerados
├── relatorio.pdf                  # Relatório técnico final em PDF
├── README.md                      # Documentação completa
└── README.txt                     # Instruções sumárias de execução
```

---

## 4. Instruções de Execução

### Pré-requisitos
* Python 3.10 ou superior.
* Dependências opcionais para gráficos e geração do relatório em PDF:
  ```bash
  pip install matplotlib numpy reportlab pymupdf
  ```
*(O resolvedor de busca e a modelagem utilizam exclusivamente a biblioteca padrão do Python).*

### Comandos de Execução

1. **Executar todos os casos de teste:**
   ```bash
   python main.py --todos
   ```

2. **Executar um caso específico com visualização da rota:**
   ```bash
   python main.py --caso casos_de_teste/caso_1_moderado.txt --visualizar
   ```

3. **Rodar apenas um algoritmo (ex: apenas A* ou apenas BFS):**
   ```bash
   python main.py --caso casos_de_teste/caso_2_intermediario.txt --algoritmo astar --visualizar
   ```

4. **Executar benchmark estatístico e gerar gráficos de desempenho:**
   ```bash
   python benchmark.py
   ```

5. **Gerar o relatório técnico em PDF (máx. 2 páginas):**
   ```bash
   python gerar_relatorio.py
   ```

---

## 5. Tabela Comparativa de Resultados

| Instância | Algoritmo | Custo ($g$) | Nós Expandidos | Nós Gerados | Fronteira Máx. | Tempo Médio | Memória Pico |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Moderado** (6×6, K=2) | BFS | 14 | 120 | 123 | 16 | 1,10 ms | 23,79 KB |
| **Moderado** (6×6, K=2) | **A\*** | **14** | **14** | **29** | **15** | **0,38 ms** | **7,19 KB** |
| **Intermediário** (10×10, K=4) | BFS | 38 | 1.055 | 1.062 | 61 | 10,36 ms | 138,71 KB |
| **Intermediário** (10×10, K=4) | **A\*** | **38** | **176** | **236** | **60** | **4,19 ms** | **50,34 KB** |
| **Complexo** (14×14, K=6) | BFS | 60 | 7.665 | 7.710 | 332 | 83,22 ms | 1.230,98 KB |
| **Complexo** (14×14, K=6) | **A\*** | **60** | **1.134** | **1.374** | **227** | **29,26 ms** | **250,69 KB** |

### Principais Conclusões
* **Otimalidade Equivalente:** Ambas as buscas atingem rigorosamente o mesmo custo ótimo para todas as instâncias (14, 38 e 60 movimentos).
* **Poda do Espaço de Busca:** O A* reduziu os nós expandidos em até **88,3%** (caso moderado) e **85,2%** (caso complexo).
* **Consumo de Memória:** Enquanto a memória do BFS cresceu exponencialmente até 1,23 MB no caso complexo, o A* alocou apenas 250 KB (redução de **79,6%**).
* **Velocidade:** O algoritmo A* proporcionou uma aceleração média de **2,5× a 2,9×** em relação à busca em largura.
