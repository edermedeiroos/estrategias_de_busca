================================================================================
2COP015: INTELIGENCIA ARTIFICIAL - TRABALHO PRATICO 1
UNIVERSIDADE ESTADUAL DE LONDRINA (UEL)
Aluno: Eder Medeiros
Professor: Prof. Dr. Antonio Parmezan
Tema: Roteamento para Coleta e Amostragem de Graos em Patio de Silobags (Agro-TIC)
================================================================================

1. REQUISITOS
- Python 3.10 ou superior instalado.
- O resolvedor de busca e a modelagem do problema utilizam apenas modulos nativos
  da biblioteca padrao do Python (sys, time, tracemalloc, collections, heapq).
- Bibliotecas opcionais para plotagem de graficos e geracao do relatorio em PDF:
    pip install matplotlib numpy reportlab pymupdf

2. INSTRUCOES DE EXECUCAO

A) Executar todos os tres casos de teste (Moderado, Intermediario e Complexo):
    python main.py --todos

B) Executar um caso especifico e visualizar a rota no terminal:
    python main.py --caso casos_de_teste/caso_1_moderado.txt --visualizar
    python main.py --caso casos_de_teste/caso_2_intermediario.txt --visualizar
    python main.py --caso casos_de_teste/caso_3_complexo.txt --visualizar

C) Executar apenas um algoritmo especifico:
    python main.py --caso casos_de_teste/caso_1_moderado.txt --algoritmo astar
    python main.py --caso casos_de_teste/caso_1_moderado.txt --algoritmo bfs

D) Rodar o benchmark estatistico completo e gerar o grafico comparativo:
    python benchmark.py

E) Gerar o relatorio tecnico em PDF (relatorio.pdf, estritamente 2 paginas):
    python gerar_relatorio.py

3. ESTRUTURA DOS ARQUIVOS DE ENTRADA (GRADE DO PATIO)
- S : Ponto de partida do coletor
- L : Laboratorio de classificacao de graos (meta final)
- B : Silobag com lote a ser amostrado
- # : Obstaculo intransponivel (maquinario, dreno, vala)
- . : Terreno livre transitavel
================================================================================
