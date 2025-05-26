import heapq

class Grafo:
    # MODELANDO E IMPLEMENTANDO O GRAFO
    def __init__(self, arquivo_entrada):
        # Dados Gerais do Grafo
        self.nome = None
        self.capacidade_veiculo = None
        self.deposito = None
        self.num_nos = None
        self.num_arestas = None
        self.num_arcos = None
        self.num_nos_req = None
        self.num_arestas_req = None
        self.num_arcos_req = None

        # Elementos Requeridos
        self.nos_requeridos = {}
        self.arestas_requeridas = []
        self.arcos_requeridos = []

        # Grafo Completo
        self.nos = set()
        self.arestas = []
        self.arcos = []

        # Estruturas adicionais
        self.lista_adjacencia = {}
        self.matriz_distancias = {}
        self.matriz_predecessores = {}

        self.carregar_dados(arquivo_entrada)
        self.inferir_nos_faltantes()
        self.gerar_lista_adjacencia()
        self.gerar_matriz_caminhos()

    def carregar_dados(self, arquivo_entrada):
      with open(arquivo_entrada, 'r', encoding='utf-8') as f:
          secao_atual = None
          contador_servico = 1

          for linha in f:
              linha = linha.strip()
              if not linha:
                  continue  # Ignora linhas vazias

              # Captura as informações do cabeçalho geral
              if linha.startswith("Name:"):
                  self.nome = linha.split("\t")[-1]
              elif linha.startswith("Capacity:"):
                  self.capacidade_veiculo = int(linha.split("\t")[-1])
              elif linha.startswith("Depot Node:"):
                  self.deposito = int(linha.split("\t")[-1])
              elif linha.startswith("#Nodes:"):
                  self.num_nos = int(linha.split("\t")[-1])
              elif linha.startswith("#Edges:"):
                  self.num_arestas = int(linha.split("\t")[-1])
              elif linha.startswith("#Arcs:"):
                  self.num_arcos = int(linha.split("\t")[-1])
              elif linha.startswith("#Required N:"):
                  self.num_nos_req = int(linha.split("\t")[-1])
              elif linha.startswith("#Required E:"):
                  self.num_arestas_req = int(linha.split("\t")[-1])
              elif linha.startswith("#Required A:"):
                  self.num_arcos_req = int(linha.split("\t")[-1])

              # Identificando a seção atual
              elif linha.startswith("ReN."):
                  secao_atual = "nos_requeridos"
                  continue
              elif linha.startswith("ReE."):
                  secao_atual = "arestas_requeridas"
                  continue
              elif linha.startswith("EDGE"):
                  secao_atual = "arestas_nao_requeridas"
                  continue
              elif linha.startswith("ReA."):
                  secao_atual = "arcos_requeridos"
                  continue
              elif linha.startswith("ARC"):
                  secao_atual = "arcos_nao_requeridos"
                  continue

              # Se a linha for um cabeçalho de tabela, ignora
              if any(header in linha for header in ["FROM N.", "To N.", "T. COST", "DEMAND", "S. COST"]):
                  continue  # Ignora os cabeçalhos das tabelas

              # Processamento dos dados conforme a seção atual
              partes = linha.split("\t")

              # Ignora linhas malformadas que não possuem colunas suficientes (para os casos em que ha uma linha no final do arquivo, como na instancia teste BHW1.dat)
              if (secao_atual == "nos_requeridos" and len(partes) < 3) or \
                (secao_atual in ["arestas_requeridas", "arcos_requeridos"] and len(partes) < 6) or \
                (secao_atual == "arcos_nao_requeridos" and len(partes) < 4):
                  continue

              if secao_atual == "nos_requeridos":
                  no = ''.join(c for c in partes[0] if c.isdigit())
                  no = int(no)
                  self.nos_requeridos[no] = {
                      "demanda": int(partes[1]),
                      "custo_servico": int(partes[2]),
                      "id_servico": contador_servico
                  }
                  self.nos.add(no)
                  contador_servico += 1

              elif secao_atual == "arestas_requeridas":
                  aresta = {
                      "de": int(partes[1]),
                      "para": int(partes[2]),
                      "custo_transito": int(partes[3]),
                      "demanda": int(partes[4]),
                      "custo_servico": int(partes[5]),
                      "id_servico": contador_servico
                  }
                  self.arestas_requeridas.append(aresta)
                  self.arestas.append(aresta)
                  contador_servico += 1

              elif secao_atual == "arestas_nao_requeridas":
                  aresta = {
                      "de": int(partes[1]),
                      "para": int(partes[2]),
                      "custo_transito": int(partes[3]),
                      "id_servico": 0
                  }
                  self.arestas.append(aresta)

              elif secao_atual == "arcos_requeridos":
                  arco = {
                      "de": int(partes[1]),
                      "para": int(partes[2]),
                      "custo_transito": int(partes[3]),
                      "demanda": int(partes[4]),
                      "custo_servico": int(partes[5]),
                      "id_servico": contador_servico
                  }
                  self.arcos_requeridos.append(arco)
                  self.arcos.append(arco)
                  contador_servico += 1

              elif secao_atual == "arcos_nao_requeridos":
                  arco = {
                      "de": int(partes[1]),
                      "para": int(partes[2]),
                      "custo_transito": int(partes[3]),
                      "id_servico": 0
                  }
                  self.arcos.append(arco)

    def inferir_nos_faltantes(self):
        """ Identifica os nós faltantes (NX) e os adiciona ao conjunto de nós. """
        todos_os_nos = set(range(1, self.num_nos + 1))  # Conjunto de nós de 1 a num_nos
        nos_requeridos = set(self.nos_requeridos.keys())  # Nós requeridos

        nos_faltantes = todos_os_nos - nos_requeridos  # Pega os que não estão na lista de requeridos

        for no in sorted(nos_faltantes):  # Garantindo que a ordem fique crescente
            self.nos.add(no)  # Adiciona ao conjunto total de nós

    def gerar_lista_adjacencia(self):
        """Cria a lista de adjacência com custo de trânsito, demanda, custo e id de serviço."""
        for no in self.nos:
            self.lista_adjacencia[no] = []

        for aresta in self.arestas_requeridas:
            info = (aresta["para"], aresta["custo_transito"], aresta["demanda"], aresta["custo_servico"], aresta["id_servico"])
            self.lista_adjacencia[aresta["de"]].append(info)

            info_inversa = (aresta["de"], aresta["custo_transito"], aresta["demanda"], aresta["custo_servico"], aresta["id_servico"])
            self.lista_adjacencia[aresta["para"]].append(info_inversa)

        for arco in self.arcos_requeridos:
            info = (arco["para"], arco["custo_transito"], arco["demanda"], arco["custo_servico"], arco["id_servico"])
            self.lista_adjacencia[arco["de"]].append(info)

        for aresta in self.arestas:
            if (aresta["de"], aresta["para"]) not in {(a["de"], a["para"]) for a in self.arestas_requeridas}:
                info = (aresta["para"], aresta["custo_transito"], "-", "-", aresta["id_servico"])
                self.lista_adjacencia[aresta["de"]].append(info)

            if (aresta["para"], aresta["de"]) not in {(a["para"], a["de"]) for a in self.arestas_requeridas}:
                info = (aresta["de"], aresta["custo_transito"], "-", "-", aresta["id_servico"])
                self.lista_adjacencia[aresta["para"]].append(info)

        for arco in self.arcos:
            if (arco["de"], arco["para"]) not in {(a["de"], a["para"]) for a in self.arcos_requeridos}:
                info = (arco["para"], arco["custo_transito"], "-", "-", arco["id_servico"])
                self.lista_adjacencia[arco["de"]].append(info)


    def gerar_matriz_caminhos(self):
        """Gera a matriz de distâncias e predecessores usando Dijkstra repetidamente."""
        nos = sorted(self.nos)
        self.matriz_distancias = {u: {} for u in nos}
        self.matriz_predecessores = {u: {} for u in nos}

        for origem in nos:
            # Inicializa estruturas para Dijkstra
            distancias = {no: float('inf') for no in nos}
            predecessores = {no: None for no in nos}
            distancias[origem] = 0
            heap = [(0, origem)]

            while heap:
                dist_u, u = heapq.heappop(heap)

                if dist_u > distancias[u]:
                    continue

                for v, custo, *_ in self.lista_adjacencia.get(u, []):
                    novo_custo = dist_u + custo
                    if novo_custo < distancias[v]:
                        distancias[v] = novo_custo
                        predecessores[v] = u
                        heapq.heappush(heap, (novo_custo, v))

            # Salva os resultados da origem atual
            self.matriz_distancias[origem] = distancias
            self.matriz_predecessores[origem] = predecessores
