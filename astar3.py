''' No .csv, os dois primeiros números representam – L linhas e C colunas da matriz A; nas linhas seguintes, cada número é um elemento
na posicao A i,j em que i ∈ {0, L-1}, j ∈ {0, C-1} (matrizes indexadas a partir de 0).
Cada elemento A i,j pode ser:
0 – que representa a saída do labirinto;
1 – que representa um caminho livre para o personagem;
# – que representa paredes; e
C – que representa a posição inicial do personagem. '''

import csv
from math import sqrt
from math import pow

# Dada uma matriz e um valor, encontra as coordenadas (i,j) que contenham o valor procurado.
def encontraPosicoes (matriz, L, C, valor):
    # lista com as posições
	posicoes = []
	for i in range(0, L):
		for j in range(0, C):
			if matriz[i][j] == valor:
				posicoes.append((i, j))
	return posicoes

# Dada uma matriz e a posicao atual pelas coordenadas (i,j), encontra os estados sucessores com 1 passo de (i,j)
def encontra_estados_sucessores (matriz, L, C, posicao_atual):
	i = posicao_atual[0]
	j = posicao_atual[1]
	# Lista com os estados sucessores
	estados_sucessores = []
	# Só se será sucessor de for diferente de #, que é a parede
	if i > 0 and matriz[i-1][j] != '#': # Move para cima na matriz.
		estados_sucessores.append ((i-1, j))
	if i+1 < L and matriz[i+1][j] != '#': # Move para baixo na matriz.
		estados_sucessores.append ((i+1, j))
	if j > 0 and matriz[i][j-1] != '#': # Move para esquerda na matriz.
		estados_sucessores.append ((i, j-1))
	if j+1 < C and matriz[i][j+1] != '#': # Move para direita na matriz.
		estados_sucessores.append ((i, j+1))
	if j > 0 and i > 0 and matriz[i-1][j-1] != '#': # Move diagonalmente para esq sup.
		estados_sucessores.append ((i-1, j-1))
	if j > 0 and i+1 < L and matriz[i+1][j-1] != '#': # Move diagonalmente para esq inf.
		estados_sucessores.append ((i+1, j-1))
	if j+1 < C and i > 0 and matriz[i-1][j+1] != '#': # Move diagonalmente para dir sup.
		estados_sucessores.append ((i-1, j+1))
	if j+1 < C and i+1 < L and matriz[i+1][j+1] != '#': # Move diagonalmente para dir inf.
		estados_sucessores.append ((i+1, j+1)) 
	return estados_sucessores

# Dado um estado considerado final, uma lista de predecessores e um numero de iteracao, apresenta em qual iteracao foi encontrada a solucao e como partir do estado inicial 
# e chegar ate o estado final a partir da solucao parcial armazenada em predecessores.
def apresenta_solucao (estado, predecessores, iteracao):
	caminho = []
	caminho.append(estado)
	print("Solucao encontrada na iteracao " + str(iteracao) + ":")
	while predecessores[estado] != None:
		caminho.append(predecessores[estado])
		estado = predecessores[estado]
	caminho = caminho[::-1]
	print(caminho, "\n\n")

# Dado um estado qualquer e um conjunto de estados finais, 
# calcula a distancia do estado qualquer ate um estado final mais proximo.
def calcula_distancia_meta (estado, estados_finais):
	x = estado[0]
	y = estado[1]
	distancia_minima = 1000000000

	for estado_final in estados_finais:
		x_estado_final = estado_final[0]
		y_estado_final = estado_final[1]
		#diff1 = x_estado_final - x
		#diff2 = y_estado_final - y
		diff1 = x - x_estado_final
		diff2 = y - y_estado_final
		somaDiffs = pow(diff1, 2) + pow(diff2, 2)
		distancia_atual = sqrt(somaDiffs)
		#somaDiffs = diff1 + diff2
		#distancia_atual = somaDiffs
		if distancia_atual < distancia_minima:
			distancia_minima = distancia_atual
	return distancia_minima

# Dada uma franja (fringe) e uma funcao heuristica, encontra o estado com menor valor nessa franja.
def encontra_estado_mais_promissor (franja, heuristica_estados):
	valor_mais_promissor = 1000000000
	estado_mais_promissor = None
	indice_mais_promissor = 0
	indice = 0
	for estado in franja:
		if heuristica_estados[estado] < valor_mais_promissor:
			estado_mais_promissor = estado
			valor_mais_promissor = heuristica_estados[estado]
			indice_mais_promissor = indice
		indice = indice + 1
	return indice_mais_promissor


def encontra_estado_mais_promissor_guloso (franja, valor_estados):
	valor_mais_promissor = 1000000000
	estado_mais_promissor = None
	indice_mais_promissor = 0
	indice = 0
	for estado in franja:
		if valor_estados[estado] < valor_mais_promissor:
			estado_mais_promissor = estado
			valor_mais_promissor = valor_estados[estado]
			indice_mais_promissor = indice
		indice = indice + 1
	return indice_mais_promissor

def encontra_estado_mais_promissor_uniforme (franja, valor_estados):
	valor_mais_promissor = 1000000000
	estado_mais_promissor = None
	indice_mais_promissor = 0
	indice = 0
	for estado in franja:
		if valor_estados[estado] < valor_mais_promissor:
			estado_mais_promissor = estado
			valor_mais_promissor = valor_estados[estado]
			indice_mais_promissor = indice
		indice = indice + 1
	return indice_mais_promissor

contador1 = 0
contador2 = 0
contador3 = 0
contador4 = 0

# Dada uma fila com alguns estados, apresenta cada um deles.
def mostra_estados_fila (fila):
	print("===================================")
	print("Estados para analisar")
	expandidos1 = 0
	global contador1
	for estado in fila:
		print(str(estado))
		contador1 += 1
	print("===================================")


# Dada uma franja (fringe) com alguns estados, apresenta o valor heuristico de cada um deles.
def mostra_valores_franja (franja, heuristica):
	print("===================================")
	print("Valores da lista")
	global contador2
	for estado in franja:
		print("f(n) = " + str(estado) + " = " + str(heuristica[estado]))
		contador2 += 1
	print("===================================")

def mostra_valores_guloso (franja):
	print("===================================")
	print("Valores da lista")
	global contador3
	for estado in franja:
		print("f(n) = " + str(estado))
		contador3 += 1
	print("===================================")

def mostra_valores_uniforme (franja):
        print("===================================")
        print("Valores da lista")
        global contador4
        for estado in franja:
                print("f(n) = " + str(estado))
                contador4 += 1
        print("===================================")
	

# Algoritmo: Busca em Largura (Breadth-First Search)
# Dada uma matriz, um estado inicial e estados finais, define um conjunto de acoes para alcancar um dos estados finais.
def busca_em_largura (matriz, L, C, estado_inicial, estados_finais):
	estados_visitados = []
	estados_expandidos = []
	profundidade_estados = {}
	predecessores = {}
	solucao_encontrada = False
	print("Algoritmo: Busca em Largura")
	estados_visitados.append(estado_inicial)
	profundidade_estados[estado_inicial] = 0
	predecessores[estado_inicial] = None
	iteracao = 1
	while len(estados_visitados) != 0:
		mostra_estados_fila (estados_visitados) # Mostra a fila do algoritmo em cada iteracao.
		estado = estados_visitados.pop(0) # Retira o primeiro elemento e confere se é o estado final
		if estado in estados_finais:
			solucao_encontrada = True # Se for o objetivo, para
			break
		estados_sucessores = encontra_estados_sucessores (matriz, L, C, estado)
		estados_expandidos.append(estado) # Append na lista de estados expandidos
		for i in range (0, len(estados_sucessores)):
			sucessor = estados_sucessores[i]
			if sucessor not in estados_expandidos and sucessor not in estados_visitados:
					estados_visitados.append(estados_sucessores[i])
					profundidade_estados[estados_sucessores[i]] = profundidade_estados[estado] + 1
					predecessores[estados_sucessores[i]] = estado
		iteracao = iteracao + 1

	if solucao_encontrada == True:
		apresenta_solucao(estado, predecessores, iteracao)
	else:
		print("Nao foi possivel encontrar uma solucao para o problema.")

# Algoritmo: Busca A* (A Estrela / A Star)
def busca_a_estrela (matriz, L, C, estado_inicial, estados_finais):
	distancia_meta = {}
	distancia_percorrida = {}
	heuristica = {}
	predecessores = {}
	estados_expandidos = []
	solucao_encontrada = False

	print("Algoritmo: A* (A Estrela)")

	# Inicializacao de distancia percorrida (f), distancia ate a meta (g) e heuristica (h = f+g).
	distancia_percorrida[estado_inicial] = 0
	distancia_meta[estado_inicial] = calcula_distancia_meta (estado_inicial, estados_finais) 
	heuristica[estado_inicial] = distancia_percorrida[estado_inicial] + distancia_meta[estado_inicial]
	predecessores[estado_inicial] = None
	print("Heuristica da Distancia no Estado Inicial: " + str(heuristica[estado_inicial]))
	franja = []
	franja.append(estado_inicial)
	iteracao = 1
	while len(franja) != 0:
		mostra_valores_franja (franja, heuristica)
		indice_mais_promissor = encontra_estado_mais_promissor(franja, heuristica)
		estado = franja.pop(indice_mais_promissor)
		if estado in estados_finais:
			solucao_encontrada = True
			break
		estados_sucessores = encontra_estados_sucessores(matriz, L, C, estado)
		estados_expandidos.append(estado)
		for i in range (0, len(estados_sucessores)):	
			sucessor = estados_sucessores[i]
			if sucessor not in estados_expandidos and sucessor not in franja:
				franja.append(sucessor)
				if sucessor not in heuristica.keys():
					distancia_meta[sucessor] = calcula_distancia_meta(sucessor, estados_finais)
					distancia_percorrida[sucessor] = distancia_percorrida[estado] + 1
					heuristica[sucessor] = distancia_meta[sucessor] + distancia_percorrida[sucessor]
					predecessores[sucessor] = estado
		iteracao = iteracao + 1

	if solucao_encontrada == True:
		apresenta_solucao(estado, predecessores, iteracao)
	else:
		print("Nao foi possivel encontrar uma solucao para o problema.")

def busca_gulosa (matriz, L, C, estado_inicial, estados_finais):
	distancia_meta = {}
	distancia_percorrida = {}
	valor_estados = {}
	predecessores = {}
	estados_expandidos = []
	solucao_encontrada = False

	print("Algoritmo: Guloso")

	# Inicializacao de distancia percorrida (f), distancia ate a meta (g) e heuristica (h = f+g).
	distancia_percorrida[estado_inicial] = 0
	distancia_meta[estado_inicial] = calcula_distancia_meta(estado_inicial,estados_finais) 
	valor_estados[estado_inicial] = distancia_meta[estado_inicial]
	predecessores[estado_inicial] = None
	franja = []
	franja.append(estado_inicial)
	iteracao = 1
	while len(franja) != 0:
		mostra_valores_guloso (franja)
		indice_mais_promissor = encontra_estado_mais_promissor_guloso(franja, valor_estados)
		estado = franja.pop(indice_mais_promissor)
		if estado in estados_finais:
			solucao_encontrada = True
			break
		estados_sucessores = encontra_estados_sucessores(matriz, L, C, estado)
		estados_expandidos.append(estado)
		for i in range (0, len(estados_sucessores)):	
			sucessor = estados_sucessores[i]
			if sucessor not in estados_expandidos and sucessor not in franja:
				franja.append(sucessor)
				if sucessor not in valor_estados.keys():
					distancia_meta[sucessor] = calcula_distancia_meta(sucessor, estados_finais)
					#distancia_percorrida[sucessor] = distancia_percorrida[estado] + 1
					valor_estados[sucessor] = distancia_meta[sucessor]
					predecessores[sucessor] = estado
		iteracao = iteracao + 1

	if solucao_encontrada == True:
		apresenta_solucao(estado, predecessores, iteracao)
	else:
		print("Nao foi possivel encontrar uma solucao para o problema.")

def busca_uniforme (matriz, L, C, estado_inicial, estados_finais):
	distancia_meta = {}
	distancia_percorrida = {}
	valor_estados = {}
	predecessores = {}
	estados_expandidos = []
	solucao_encontrada = False

	print("Algoritmo: Custo Uniforme")

	# Inicializacao de distancia percorrida (f), distancia ate a meta (g) e heuristica (h = f+g).
	distancia_percorrida[estado_inicial] = 0
	#distancia_meta[estado_inicial] = calcula_distancia_meta(estado_inicial,estados_finais) 
	valor_estados[estado_inicial] = distancia_percorrida[estado_inicial]
	predecessores[estado_inicial] = None
	franja = []
	franja.append(estado_inicial)
	iteracao = 1
	while len(franja) != 0:
		mostra_valores_uniforme (franja)
		indice_mais_promissor = encontra_estado_mais_promissor_uniforme(franja, valor_estados)
		estado = franja.pop(indice_mais_promissor)
		if estado in estados_finais:
			solucao_encontrada = True
			break
		estados_sucessores = encontra_estados_sucessores(matriz, L, C, estado)
		estados_expandidos.append(estado)
		for i in range (0, len(estados_sucessores)):	
			sucessor = estados_sucessores[i]
			if sucessor not in estados_expandidos and sucessor not in franja:
				franja.append(sucessor)
				if sucessor not in valor_estados.keys():
					#distancia_meta[sucessor] = calcula_distancia_meta(sucessor, estados_finais)
					distancia_percorrida[sucessor] = distancia_percorrida[estado] + 1
					valor_estados[sucessor] = distancia_percorrida[sucessor]
					predecessores[sucessor] = estado
		iteracao = iteracao + 1

	if solucao_encontrada == True:
		apresenta_solucao(estado, predecessores, iteracao)
	else:
		print("Nao foi possivel encontrar uma solucao para o problema.")


# Fluxo principal do program em Python.
# Inspirado no problema 'Duende Perdido' da Olimpiada Brasileira de Informatica de 2005 - OBI 2005.

#problema = open("caminho.csv")
problema = open("caminho2.csv")
leitor_problema = csv.reader(problema)
entrada = list(leitor_problema)
L = int(entrada[0][0]) # numero de linhas.
C = int(entrada[0][1]) # numero de colunas.
matriz = entrada[1:] # mapa representado como matriz.

estado_inicial = encontraPosicoes (matriz, L, C, 'C')
estados_finais = encontraPosicoes (matriz, L, C, '0')

print("Matriz (mapa): ")
for item in matriz:
    print(item, "\n")


print("Estado Inicial: " + str(estado_inicial))
print("Estado Final: " + str(estados_finais))

busca_em_largura (matriz, L, C, estado_inicial[0], estados_finais)
print("Expandidos: ", contador1, "\n")

busca_a_estrela (matriz, L, C, estado_inicial[0], estados_finais)
print("Expandidos: ", contador2, "\n")

busca_gulosa(matriz, L, C, estado_inicial[0], estados_finais)
print("Expandidos: ", contador3, "\n")

busca_uniforme (matriz, L, C, estado_inicial[0], estados_finais)
print("Expandidos: ", contador4, "\n")


