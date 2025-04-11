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
                      "custo_servico": int(partes[2])
                  }
                  self.nos.add(no)

              elif secao_atual == "arestas_requeridas":
                  aresta = {
                      "de": int(partes[1]),
                      "para": int(partes[2]),
                      "custo_transito": int(partes[3]),
                      "demanda": int(partes[4]),
                      "custo_servico": int(partes[5])
                  }
                  self.arestas_requeridas.append(aresta)
                  self.arestas.append((aresta["de"], aresta["para"]))

              elif secao_atual == "arcos_requeridos":
                  arco = {
                      "de": int(partes[1]),
                      "para": int(partes[2]),
                      "custo_transito": int(partes[3]),
                      "demanda": int(partes[4]),
                      "custo_servico": int(partes[5])
                  }
                  self.arcos_requeridos.append(arco)
                  self.arcos.append(arco)

              elif secao_atual == "arcos_nao_requeridos":
                  arco = {
                      "de": int(partes[1]),
                      "para": int(partes[2]),
                      "custo_transito": int(partes[3])
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
        """Cria a lista de adjacência com trânsito, demanda e custo de parada."""
        for no in self.nos:
            self.lista_adjacencia[no] = []

        for aresta in self.arestas_requeridas:
            info = (aresta["para"], aresta["custo_transito"], aresta["demanda"], aresta["custo_servico"])
            self.lista_adjacencia[aresta["de"]].append(info)

            info_inversa = (aresta["de"], aresta["custo_transito"], aresta["demanda"], aresta["custo_servico"])
            self.lista_adjacencia[aresta["para"]].append(info_inversa)

        for arco in self.arcos_requeridos:
            info = (arco["para"], arco["custo_transito"], arco["demanda"], arco["custo_servico"])
            self.lista_adjacencia[arco["de"]].append(info)

        for u, v in self.arestas:
            if not any(vv == v for vv, *_ in self.lista_adjacencia[u]):
                self.lista_adjacencia[u].append((v, 1, "-", "-"))
            if not any(uu == u for uu, *_ in self.lista_adjacencia[v]):
                self.lista_adjacencia[v].append((u, 1, "-", "-"))

        for arco in self.arcos:
            if (arco["de"], arco["para"]) not in {(a["de"], a["para"]) for a in self.arcos_requeridos}:
                info = (arco["para"], arco["custo_transito"], "-", "-")
                self.lista_adjacencia[arco["de"]].append(info)


    def gerar_matriz_caminhos(self):
        """Implementa o algoritmo de Floyd-Warshall para matriz de distâncias e predecessores."""
        nos = sorted(self.nos)
        self.matriz_distancias = {i: {j: float('inf') for j in nos} for i in nos}
        self.matriz_predecessores = {i: {j: None for j in nos} for i in nos}

        for no in nos:
            self.matriz_distancias[no][no] = 0

        # Inicializa com valores da lista de adjacência
        for origem in self.lista_adjacencia:
            for destino, custo, *_ in self.lista_adjacencia[origem]:
                if custo < self.matriz_distancias[origem][destino]:
                    self.matriz_distancias[origem][destino] = custo
                    self.matriz_predecessores[origem][destino] = origem

        # Algoritmo Floyd-Warshall
        for k in nos:
            for i in nos:
                for j in nos:
                    if self.matriz_distancias[i][k] + self.matriz_distancias[k][j] < self.matriz_distancias[i][j]:
                        self.matriz_distancias[i][j] = self.matriz_distancias[i][k] + self.matriz_distancias[k][j]
                        self.matriz_predecessores[i][j] = self.matriz_predecessores[k][j]

    def depurar_dados(self):
        print(f"\n🔹 Nome da Instância: {self.nome}")
        print(f"🔹 Capacidade do Veículo: {self.capacidade_veiculo}")
        print(f"🔹 Nó Depósito: {self.deposito}")

        print("\n📌 Dados Gerais do Grafo:")
        print(f"   - Número Total de Nós: {len(self.nos)} (Incluindo inferidos)")
        print(f"   - Número Total de Arestas: {len(self.arestas)}")
        print(f"   - Número Total de Arcos: {len(self.arcos)}")

        print("\n📌 Nós Requeridos:")
        for no, dados in self.nos_requeridos.items():
            print(f"   - {no}: Demanda = {dados['demanda']}, Custo Serviço = {dados['custo_servico']}")

        print("\n📌 Nós Inferidos (Não Requeridos Explicitamente):")
        nos_inferidos = sorted(self.nos - set(self.nos_requeridos.keys()))
        for no in nos_inferidos:
            print(f"   - {no}")

        print("\n📌 Arestas Requeridas:")
        for aresta in self.arestas_requeridas:
            print(f"   - {aresta['de']} ←→ {aresta['para']} | Custo Trânsito = {aresta['custo_transito']}, "
                  f"Demanda = {aresta['demanda']}, Custo Serviço = {aresta['custo_servico']}")

        print("\n📌 Arestas Não Requeridas:")
        arestas_requeridas_tuplas = {(a["de"], a["para"]) for a in self.arestas_requeridas}
        for aresta in self.arestas:
            if aresta not in arestas_requeridas_tuplas:
                print(f"   - {aresta[0]} ←→ {aresta[1]}")

        print("\n📌 Arcos Requeridos:")
        for arco in self.arcos_requeridos:
            print(f"   - {arco['de']} → {arco['para']} | Custo Trânsito = {arco['custo_transito']}, "
                  f"Demanda = {arco['demanda']}, Custo Serviço = {arco['custo_servico']}")

        print("\n📌 Arcos Não Requeridos:")
        arcos_requeridos_tuplas = {(a["de"], a["para"]) for a in self.arcos_requeridos}
        for arco in self.arcos:
            if (arco["de"], arco["para"]) not in arcos_requeridos_tuplas:
                print(f"   - {arco['de']} → {arco['para']} | Custo Trânsito = {arco['custo_transito']}")

    def imprimir_matriz(self, matriz, nome="Matriz"):
        nos_ordenados = sorted(self.nos)
        print(f"\n📌 {nome}:")
        header = "\t" + "\t".join(map(str, nos_ordenados))
        print(header)
        print("-" * len(header.expandtabs()))
        for origem in nos_ordenados:
            linha = [str(origem)]
            for destino in nos_ordenados:
                valor = matriz.get(origem, {}).get(destino, float('inf'))
                if nome.lower().startswith("matriz de predecessores"):
                    linha.append("∞" if valor is None else str(valor))
                else:
                    linha.append("∞" if valor == float('inf') else str(valor))
            print("\t".join(linha))

    def imprimir_lista_adjacencia(self):
        print("\n📌 Lista de Adjacência:")
        for no in sorted(self.lista_adjacencia):
            print(f"{no}: {self.lista_adjacencia[no]}")

    # CALCULANDO AS ESTATÍSICAS DO GRAFO
    def centralidade_intermediacao(self):
        """Calcula a centralidade de intermediação"""
        intermediacao = {no: 0 for no in self.nos}

        for origem in self.nos:
            for destino in self.nos:
                if origem != destino:
                    caminho = self.reconstruir_caminho(origem, destino)
                    # Remove origem e destino — só é necessário nos intermediários
                    for no in caminho[1:-1]:
                        intermediacao[no] += 1

        return intermediacao


    def reconstruir_caminho(self, origem, destino):
        """Reconstrói o caminho mínimo de origem até destino"""
        if self.matriz_predecessores[origem][destino] is None:
            return []  # Não existe caminho
        caminho = [destino]
        atual = destino
        while atual != origem:
            atual = self.matriz_predecessores[origem][atual]
            caminho.append(atual)
        caminho.reverse()
        return caminho

    def calcular_estatisticas(self):
        total_arcos = self.num_arcos + 2 * self.num_arestas
        densidade = total_arcos / (self.num_nos * (self.num_nos - 1))

        grau_saida = [len(vizinhos) for vizinhos in self.lista_adjacencia.values()]
        grau_entrada_dict = {no: 0 for no in self.lista_adjacencia}
        for vizinhos in self.lista_adjacencia.values():
            for destino, *_ in vizinhos:
                grau_entrada_dict[destino] += 1
        grau_entrada = list(grau_entrada_dict.values())
        grau_total = [entrada + saida for entrada, saida in zip(grau_entrada, grau_saida)]

        intermed = self.centralidade_intermediacao()

        distancias = self.matriz_distancias
        soma = 0
        qtd = 0
        diametro = 0
        for u in distancias:
            for v in distancias[u]:
                if u != v and distancias[u][v] < float('inf'):
                    soma += distancias[u][v]
                    qtd += 1
                    diametro = max(diametro, distancias[u][v])
        caminho_medio = soma / qtd if qtd > 0 else float('inf')

        # Retorna 2 coisas: dicionário com estatísticas gerais + dict com centralidade por nó
        estatisticas_gerais = {
            "vértices": self.num_nos,
            "arestas": self.num_arestas,
            "arcos": self.num_arcos,
            "nós requeridos": self.num_nos_req,
            "arestas requeridas": self.num_arestas_req,
            "arcos requeridos": self.num_arcos_req,
            "densidade": densidade,
            "grau_saida_min": min(grau_saida),
            "grau_saida_max": max(grau_saida),
            "grau_entrada_min": min(grau_entrada),
            "grau_entrada_max": max(grau_entrada),
            "grau_total_min": min(grau_total),
            "grau_total_max": max(grau_total),
            "caminho_medio": caminho_medio,
            "diâmetro": diametro,
        }

        return estatisticas_gerais, intermed