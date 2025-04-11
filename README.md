# Trabalho de Grafos
Trabalho para a disciplina GCC218-Algoritmos em Grafos da UFLA, desenvolvido pela aluna Thaís Giovanna Lopes

# Instruções para execução da solução
  1. Abra o arquivo TrabalhoGrafos.ipynb
  2. Execute as células de código

As estatísticas podem ser exibidas em uma tabela ou em um arquivo de extensão csv.

# Descrição do Problema (trecho retirado do documento de especificação do trabalho)
  Estudar problemas de logística é crucial para otimizar o fluxo de bens e serviços, resultando em maior eficiência e redução de custos para empresas e consumidores. A análise detalhada de processos logísticos permite identificar gargalos, melhorar o planejamento de rotas, gerenciar estoques de forma mais eficaz e implementar tecnologias que aprimoram a tomada de decisões. A logística desempenha um papel fundamental na competitividade das empresas, influenciando diretamente a satisfação do cliente e a sustentabilidade ambiental. Ao compreender os desafios logísticos, é possível desenvolver soluções inovadoras que impulsionam o crescimento econômico e promovem um futuro mais eficiente e responsável.

## Definição formal
  O problema base pode ser definido em um grafo conexo G = (V,E), onde V é o conjunto de nós e E o conjunto de arestas. Os nós representam intersecções (ou esquinas) em uma região (urbana ou rural), enquanto as arestas são as vias de acesso (ruas, avenidas, etc). Um subconjunto ER ⊆ E dessas arestas deve ser atendido. Seja n = |ER| o número de serviços. Uma aresta (i,j) ∈ E pode ser percorrida qualquer número de vezes com um custo de cij cada vez, e uma demanda de qij está associada a qualquer aresta (i,j) ∈ ER. O problema visa encontrar um conjunto de viagens de veículos com custo mínimo, tal que cada viagem comece e termine em um nó depósito v0 ∈ V, cada aresta requerida seja atendida por uma única viagem, e a demanda total para qualquer veículo não exceda uma capacidade Q. A variação estudada no trabalho prático redefine G, em particular, como um multigrafo conectado G = (V,E,A), onde V é o conjunto de nós, E o conjunto de arestas e A o conjunto de arcos (vias de mão única). Serviços são requeridos para um subconjunto de nós VR ⊆ V, arestas ER ⊆ E e arcos AR ⊆ A, tal que n=|VR|+|ER|+|AR|.
