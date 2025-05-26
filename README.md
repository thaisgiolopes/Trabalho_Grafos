# Trabalho de Grafos
Trabalho para a disciplina GCC218-Algoritmos em Grafos da UFLA, desenvolvido pela aluna Thaís Giovanna Lopes

## Descrição do Problema 
(trecho retirado do document de especificação do trabalho)
  Estudar problemas de logística é crucial para otimizar o fluxo de bens e serviços, resultando em maior eficiência e redução de custos para empresas e consumidores. A análise detalhada de processos logísticos permite identificar gargalos, melhorar o planejamento de rotas, gerenciar estoques de forma mais eficaz e implementar tecnologias que aprimoram a tomada de decisões. A logística desempenha um papel fundamental na competitividade das empresas, influenciando diretamente a satisfação do cliente e a sustentabilidade ambiental. Ao compreender os desafios logísticos, é possível desenvolver soluções inovadoras que impulsionam o crescimento econômico e promovem um futuro mais eficiente e responsável.

### Definição formal
  O problema base pode ser definido em um grafo conexo G = (V,E), onde V é o conjunto de nós e E o conjunto de arestas. Os nós representam intersecções (ou esquinas) em uma região (urbana ou rural), enquanto as arestas são as vias de acesso (ruas, avenidas, etc). Um subconjunto ER ⊆ E dessas arestas deve ser atendido. Seja n = |ER| o número de serviços. Uma aresta (i,j) ∈ E pode ser percorrida qualquer número de vezes com um custo de cij cada vez, e uma demanda de qij está associada a qualquer aresta (i,j) ∈ ER. O problema visa encontrar um conjunto de viagens de veículos com custo mínimo, tal que cada viagem comece e termine em um nó depósito v0 ∈ V, cada aresta requerida seja atendida por uma única viagem, e a demanda total para qualquer veículo não exceda uma capacidade Q. A variação estudada no trabalho prático redefine G, em particular, como um multigrafo conectado G = (V,E,A), onde V é o conjunto de nós, E o conjunto de arestas e A o conjunto de arcos (vias de mão única). Serviços são requeridos para um subconjunto de nós VR ⊆ V, arestas ER ⊆ E e arcos AR ⊆ A, tal que n=|VR|+|ER|+|AR|.


## Organização da solução
  O projeto é organizado em duas classes principais: a classe Grafo e a classe HeuristicaConstrutiva. Abaixo uma breve descrição da funcionalidade de cada classe.
  - Classe Grafo: ela é responsável por realizar a leitura do arquivo e a modelagem do Grafo. Inclui uma função que gera a lista de adjacência e uma função que gera a matriz de distâncias e a matriz de predecessores através de um Dijkstra com repetição.
  - Classe HeuristicaConstrutiva: ela é responsável por construir a solução gulosa para o problema em questão. A partir de um grafo, ela constroi rotas que atendem todos os elementos requeridos com base na seleção do melhor serviço no momento, feita através das seguintes funções:
     - obter_elementos_vizinhos_nao_atendidos: executa uma BFS por camadas a partir do vértice inicial e retorna uma lista de candidatos com os elementos requeridos não atendidos da camada mais próxima.
     - _selecionar_melhor_servico: seleciona o melhor serviço da lista de candidatos baseado na razão demanda/custo
  Essas soluções são executadas e integradas no notebook Etapa2_Trabalho_Grafos.ipynb.

## Instruções para execução da solução
  1. Abra o arquivo Etapa2_Trabalho_Grafos.ipynb
  2. Execute as células de código
As soluções são exibidas em um arquivo .dat para cada instância teste. Além disso, é possível baixar o arquivo .zip com todas as instâncias
