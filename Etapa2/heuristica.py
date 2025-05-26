import heapq
from collections import deque
from google.colab import files
from grafo import Grafo

class HeuristicaConstrutiva:
    def __init__(self, arquivo_entrada):
        self.grafo = Grafo(arquivo_entrada)
        self.grafo.gerar_matriz_caminhos()
        self.rotas = []
        self.total_custo = 0
        self.servicos_pendentes = (
            list(self.grafo.arcos_requeridos) +
            list(self.grafo.arestas_requeridas) +
            list(self.grafo.nos_requeridos.items())
        )

    def construir_rotas(self):
        capacidade_veiculo_padrao = self.grafo.capacidade_veiculo
        deposito = self.grafo.deposito
        id_servico = 0

        while self.servicos_pendentes:
            rota = []
            custo_rota = 0
            demanda_rota = 0
            capacidade_veiculo = capacidade_veiculo_padrao
            posicao_atual = deposito

            while capacidade_veiculo > 0:
                candidatos_dict = self.obter_elementos_vizinhos_nao_atendidos(posicao_atual)
                melhor_servico = self._selecionar_melhor_servico(candidatos_dict, posicao_atual, capacidade_veiculo)

                if not melhor_servico:
                    break

                tipo = melhor_servico["tipo"]

                if tipo == "no":
                    no = melhor_servico["no"]
                    demanda = melhor_servico["demanda"]
                    #custo_servico = melhor_servico["custo_servico"]
                    custo_total = melhor_servico["custo_transito_e_servico"]
                    id_servico = melhor_servico["id_servico"]

                    rota.append(("S", id_servico, posicao_atual, no))
                    capacidade_veiculo -= demanda
                    demanda_rota += demanda
                    custo_rota += custo_total
                    posicao_atual = no

                    self.servicos_pendentes = [
                        s for s in self.servicos_pendentes
                        if not (isinstance(s, tuple) and s[0] == no)
                    ]

                elif tipo in ("aresta", "arco"):
                    u = melhor_servico["de"]
                    v_arco = melhor_servico["para"]
                    demanda = melhor_servico["demanda"]
                    #custo_servico = melhor_servico["custo_"]
                    custo_total = melhor_servico["custo_transito_e_servico"]
                    id_servico = melhor_servico["id_servico"]

                    rota.append(("S", id_servico, u, v_arco))
                    capacidade_veiculo -= demanda
                    demanda_rota += demanda
                    custo_rota += custo_total
                    posicao_atual = v_arco

                    if tipo == "aresta":
                        for s in self.servicos_pendentes:
                            if isinstance(s, dict) and (
                                (s["de"] == u and s["para"] == v_arco) or
                                (s["de"] == v_arco and s["para"] == u)
                            ):
                                self.servicos_pendentes.remove(s)
                                break
                    else:  # tipo == "arco"
                        for s in self.servicos_pendentes:
                            if isinstance(s, dict) and s["de"] == u and s["para"] == v_arco:
                                self.servicos_pendentes.remove(s)
                                break

            if posicao_atual != deposito:
                rota.insert(0, ("D", 0, deposito, deposito))
                custo_volta = self.grafo.matriz_distancias[posicao_atual][deposito]
                rota.append(("D", 0, deposito, deposito))
                custo_rota += custo_volta

            if rota:
                info = {
                    "rota": rota,
                    "demanda_rota": demanda_rota,
                    "custo_rota": custo_rota,
                    "total_visitas": len(rota)
                }
                self.rotas.append(info)
                self.total_custo += custo_rota

    def obter_elementos_vizinhos_nao_atendidos(self, v_inicial):
        """
        Executa uma BFS por camadas a partir de v_inicial, e retorna os elementos requeridos não atendidos
        (nós, arestas ou arcos) encontrados na camada mais próxima.
        """
        candidatos = []
        visitados = set()
        fila = deque([(v_inicial, [v_inicial])])
        encontrou_na_camada = False

        while fila and not encontrou_na_camada:
            tamanho_da_camada = len(fila)

            for _ in range(tamanho_da_camada):
                v, caminho = fila.popleft()

                if v in visitados:
                    continue
                visitados.add(v)

                # --- Verifica nó requerido e não atendido
                if v in self.grafo.nos_requeridos:
                    info = self.grafo.nos_requeridos[v]
                    if (v, info) in self.servicos_pendentes:
                        custo = self.grafo.matriz_distancias[v_inicial][v]
                        candidatos.append({
                            "tipo": "no",
                            "no": v,
                            "demanda": info["demanda"],
                            "custo_servico": info["custo_servico"],
                            "id_servico": info["id_servico"],
                            "custo_transito_e_servico": custo + info["custo_servico"]
                            #"caminho": caminho
                        })
                        encontrou_na_camada = True

                # Verifica se algum vizinho de v é nó requerido
                for vizinho, *_ in self.grafo.lista_adjacencia.get(v, []):
                    if vizinho in self.grafo.nos_requeridos:
                        info = self.grafo.nos_requeridos[vizinho]
                        if (vizinho, info) in self.servicos_pendentes:
                            custo = self.grafo.matriz_distancias[v_inicial][vizinho]
                            candidatos.append({
                                "tipo": "no",
                                "no": vizinho,
                                "demanda": info["demanda"],
                                "custo_servico": info["custo_servico"],
                                "id_servico": info["id_servico"],
                                "custo_transito_e_servico": custo + info["custo_servico"]
                                #"caminho": caminho + [vizinho]
                            })
                            encontrou_na_camada = True

                # --- Verifica arestas requeridas incidentes em v
                for aresta in self.grafo.arestas_requeridas:
                    u, w = aresta["de"], aresta["para"]
                    if v == u or v == w:
                        if aresta in self.servicos_pendentes:
                            #outro_extremo = w if v == u else u
                            custo = min(self.grafo.matriz_distancias[v_inicial][u], self.grafo.matriz_distancias[v_inicial][w])
                            candidatos.append({
                                "tipo": "aresta",
                                "de": u,
                                "para": w,
                                "demanda": aresta["demanda"],
                                "custo_servico": aresta["custo_servico"],
                                "custo_transito": aresta["custo_transito"],
                                "id_servico": aresta["id_servico"],
                                "custo_transito_e_servico": custo + aresta["custo_servico"]
                                #"caminho": caminho + [outro_extremo]
                            })
                            encontrou_na_camada = True

                # --- Verifica arcos requeridos saindo de v
                for arco in self.grafo.arcos_requeridos:
                    if arco["de"] == v and arco in self.servicos_pendentes:
                        custo = self.grafo.matriz_distancias[v_inicial][arco["de"]]
                        candidatos.append({
                            "tipo": "arco",
                            "de": arco["de"],
                            "para": arco["para"],
                            "demanda": arco["demanda"],
                            "custo_servico": arco["custo_servico"],
                            "custo_transito": arco["custo_transito"],
                            "id_servico": arco["id_servico"],
                            "custo_transito_e_servico": custo + arco["custo_servico"]
                            #"caminho": caminho + [arco["para"]]
                        })
                        encontrou_na_camada = True

                # --- Adiciona vizinhos à fila
                for vizinho, *_ in self.grafo.lista_adjacencia.get(v, []):
                    if vizinho not in visitados:
                        fila.append((vizinho, caminho + [vizinho]))

        return candidatos

    def _selecionar_melhor_servico(self, candidatos, posicao_atual, capacidade_disponivel):
        def melhor_servico(servico):
            if servico["demanda"] > capacidade_disponivel:
                return -1  # inviável
            custo_total = servico["custo_transito_e_servico"]
            return servico["demanda"] / custo_total if custo_total > 0 else 0

        candidatos_viaveis = [(s, melhor_servico(s)) for s in candidatos]
        candidatos_viaveis = [s for s in candidatos_viaveis if s[1] > 0]

        if not candidatos_viaveis:
            return None

        candidatos_viaveis.sort(key=lambda x: x[1], reverse=True)
        return candidatos_viaveis[0][0]

    def imprimir_rotas(self, clock_algoritmo, clock_solucao):
        print(self.total_custo)
        print(len(self.rotas))
        print(clock_algoritmo)
        print(clock_solucao)
        for id_rota, rota in enumerate(self.rotas, 1):
            print(0, 1, id_rota, rota["demanda_rota"], rota["custo_rota"], " ", rota["total_visitas"], end=" ")
            for passo in rota["rota"]:
                print(passo, end=" ")
            print()

    def salvar_e_baixar_rotas(self, clock_algoritmo, clock_solucao, nome_arquivo="sol-instancia.dat"):
        with open(nome_arquivo, "w") as f:
            f.write(f"{self.total_custo}\n")
            f.write(f"{len(self.rotas)}\n")
            f.write(f"{clock_algoritmo}\n")
            f.write(f"{clock_solucao}\n")
            for id_rota, rota in enumerate(self.rotas, 1):
                linha_inicial = f"0 1 {id_rota} {rota['demanda_rota']} {rota['custo_rota']}  {rota['total_visitas']}"
                passos = " ".join(map(str, rota["rota"]))
                f.write(f"{linha_inicial} {passos}\n")

        # Faz o download do arquivo para o computador
        files.download(nome_arquivo)
