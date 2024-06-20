
# matriz 2019:
# 46 disciplinas: 10 optativas e 36 obrigatorias
# 3 disciplinas: CR 2 ou CH 30
# 4 disciplinas: CR 6 ou CH 90
# 39 disciplinas: CR 4 ou CH 60
# disciplinas por semestre (total): CR 30 ou 28
# limite maximo de semestres: 8+4=12
# pre requisitos
# optativa/obrigatoria
# periodo das disciplinas
# ano de oferta do semestre par ou impar
# creditos de cada disciplina

# lista de disciplinas:
# codigo(nome), periodo, prerequisito, credito

# avaliacao:
# quantidade de semestres
# quantidade de disciplinas por semestre (ideal [5, 7])
# pre requisito
# pre requisito no mesmo semestre


import numpy as np
import random

tampopulacao = 2
geracoes = 2
maxCRsemestre = 28
maxsemestres = 12 # 8 + 4 semestres ((ano_atual - ano_ingresso) + dois_anos)
semestreparimpar = 2 # 1 ou 2

#matriz regular
nomes = ["Direito e Ética", "Filosofia das Ciências Naturais", "Introdução à Programação de Computadores", "Lógica Matemática Aplicada a Computação", "Matemática Fundamental", "Produção Textual", "Cálculo", "Circuitos Digitais", "Estrutura de Dados", "Geometria Analítica", "Metodologia Para o Trabalho Científico", "Paradigmas de Programação", "Álgebra Linear", "Eletricidade e Magnetismo", "Engenharia de Software", "Estruturas Auto-ajustáveis e Grafos", "Linguagens Formais e Autômatos", "Sistemas Digitais", "Análise de Sistemas", "Arquitetura de Computadores", "Banco de Dados", "Cálculo Numérico Computacional", "Compiladores", "Probabilidade e Estatística", "Transmissão de Dados", "Inteligência Artificial", "Métodos Formais", "Redes de Computadores", "Sistemas Operacionais", "Optativa I", "Optativa II", "Optativa III", "Computação Gráfica", "Programação Paralela", "Projeto de Graduação", "Sistemas Distribuídos", "Teoria Geral de Administração e Empreendedorismo", "Optativa IV", "Optativa V", "Projeto de Trabalho de Conclusão de Curso", "Optativa VI", "Optativa VII", "Optativa VIII", "Optativa IX", "Optativa X", "Trabalho de Conclusão de Curso"]
matreg = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]
perreg = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2,  2,  2,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  4,  4,  5,  5,  5,  5,  0,  0,  0,  6,  6,  6,  6,  6,  0,  0,  7,  0,  0,  0,  0,  0,  8]
reqreg = [0, 0, 0, 0, 0, 0, 0, 0, 3, 0,  0,  3,  10, 0,  0,  9,  0,  0,  15, 8,  0,  0,  17, 0,  0,  0,  0,  25, 0,  0,  0,  0,  13, 0,  [1, 6, 8, 11, 12, 9, 18, 17, 15, 16, 20, 23, 19, 22, 25, 21, 26, 27, 29, 28],  0,  0,  0,  0,  [35, 33, 34, 37, 36],  0,  0,  0,  0,  0,  [40, 1, 2, 3, 4, 5, 6, 7,8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]]
crereg = [2, 4, 6, 4, 6, 2, 6, 4, 4, 4,  2,  4,  4,  6,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4]

# lista de todas as disciplinas que faltam
mat = [26, 27, 28, 29, 30, 31, 32, 33, 34, 35,               36, 37, 38, 39, 40,                                    41, 42, 43, 44, 45, 46]
#semestre
per = [5,  5,  5,  5,  0,  0,  0,  6,  6,  6,                6,  6,  0,  0,  7,                                     0,  0,  0,  0,  0,  8]
#requisito
req = [0,  0,  0,  0,  0,  0,  0,  0,  0,  [26, 27, 28, 29], 0,  0,  0,  0,  [35, 26, 27, 28, 29, 33, 34, 37, 36],  0,  0,  0,  0,  0,  [40, 35, 33, 34, 36, 37, 26, 27, 28, 29]]
#caraga horaria
cre = [4,  4,  4,  4,  4,  4,  4,  4,  4,  4,                4,  4,  4,  4,  4,                                     4,  4,  4,  4,  4,  4]
# lista de disciplinas sem optativas
matob = []
perob = []
reqob = []
creob = []
matop = []
perop = []
reqop = []
creop = []
for i in range(len(mat)):
  if (per[i]==0):
    matop.insert(i, mat[i])
    perop.insert(i, per[i])
    reqop.insert(i, req[i])
    creop.insert(i, cre[i])
  else:
    matob.insert(i, mat[i])
    perob.insert(i, per[i])
    reqob.insert(i, req[i])
    creob.insert(i, cre[i])
print("obrigatorias: ", matob)
print("optativas: ", matop)
#matriz = []
#for i in range(pgdisc):
#  tupla = (mat[i], per[i], req[i], cre[i])
#  matriz.append(tupla)
#print("matriz   : ", matriz)
# encontrar a posicao de uma disciplina
#disc = 30
#pos = mat.index(disc)

def criar_individuo():
  individuo = matob.copy()
  random.shuffle(individuo)
  #print("criar individuo")
  return individuo

def criar_populacao(tampopulacao):
  populacao = []
  for i in range(tampopulacao):
    linha = []
    linha  = criar_individuo()
    populacao.append(linha.copy())
  #print(populacao)
  #print("criar populacao")
  return populacao

def crossover(populacao):
  # (teoricamente) seleciona dois pais e faz o cruzamento e verifica valivade (se contém todas disciplinas ou se não repete disciplinas)
  populacaoc = []
  for _ in range(tampopulacao):
    linha = []
    linha  = criar_individuo()
    populacaoc.append(linha.copy())
  #print(populacaoc)
  #print("crossover")
  return populacaoc

# agrupa disciplinas por semestres pares e impares (ou 3 para optativa)
def parimpar(individuo):
  listaparimpar = []
  tamind = len(individuo)
  for i in range(tamind):
    disc = individuo[i]
    #matreg - codigo da disciplina
    pos = matreg.index(disc)
    #perreg - semestre
    aux = perreg[pos]
    if perreg[pos]==0:
      listaparimpar.insert(i, 3)
    elif (perreg[pos]%2)==0:
      listaparimpar.insert(i, 2)
    else:
      listaparimpar.insert(i, 1)
  #print(listaparimpar)
  #print("clusters")
  return listaparimpar

def quantsemestres(listpi):
  lista = listpi
  cont_semestres = 1
  ultimo = lista[0]
  for val in lista[1:]:
    if (val!=ultimo):
      cont_semestres += 1
      ultimo = val
  #print("semestres: ", cont_semestres)
  #print("conta semestres")
  print(cont_semestres)
  return cont_semestres

# total(soma) de disciplinas em cada semestre por individuo
def somaseqsemestres(listpi):
  somas = []
  contagem_atual = 1
  for i in range(1, len(listpi)):
    if listpi[i] == listpi[i - 1]:
      contagem_atual += 1
    else:
      somas.append(contagem_atual)
      contagem_atual = 1
  somas.append(contagem_atual)
  #print("soma disciplinas por semestres")
  return somas

# individuos que iniciam com disciplina par ou impar de acordo com o semestre a ser ofertado
def individuopi(individuo):
  #listindpq = 0
  disc = individuo[0]
  pos = matreg.index(disc)
  aux = perreg[pos]
  if (perreg[pos]%2)==0:
    listindpq = 2
  else:
    listindpq = 1
  return listindpq

# pesos diferentes pas semestres com mais de 7 disciplinas ou menos de 3
def somadiscsemestres(aux):
  pesossomadiscsem = 0
  for i in range(len(aux)):
    if (aux[i] > 7):
      pesossomadiscsem += 3 #(maxsemestres-4) # maxsemestres menos 2 anos
    elif (aux[i] == 2):
      pesossomadiscsem += 1
    elif (aux[i] == 1):
      pesossomadiscsem += 2
  return pesossomadiscsem

# cria lista de individuos que violam os requisitos
def verificar_restricoes(individuo, requisitos):
  resultado = []
  subdisc = []
  tamsubreq = [len(item) if isinstance(item, list) else 0 for item in requisitos] # lista o tamanho da lista de requisitos de cada disciplina (disciplinas com um requisito recebe zero tbm)
  #print("tamsubreq ", tamsubreq)
  for i in range(len(individuo)):
    subdisc = individuo[:(i+1)]
    #print("subdisc ", subdisc)
    if (tamsubreq[i] != 0):
      aux = requisitos[i]
      #print("aux ", aux)
      if (set(aux).issubset(set(subdisc))):
        resultado.append(0)
      else:
        resultado.append(1)
    elif (tamsubreq[i] == 0):
      if (requisitos[i] == 0):
        resultado.append(0)
      elif (requisitos[i] not in subdisc):
        resultado.append(1)
  auxsoma = sum(resultado)*4
  #print("resultado ", resultado)
  #print("auxsoma ", auxsoma)
  return auxsoma
# verifica se existe violacao dos requisitos
def verrequisito(individuo):
  #wlistareqdisc = []
  requisitos = []
  #listareqdisc = [] # lista de true/false para atendimento dos requisitos
  for i in range(len(individuo)):
    disc = individuo[i]
    pos = mat.index(disc)
    requisitos.append(req[pos]) # lista de requisitos de acordo com as disciplinas por individuo
  #print("individuo ", individuo)
  #print("requisitos ", requisitos)
  #listareqdisc.append(verificar_restricoes(individuo, requisitos))
  #wlistareqdisc.append(verificar_restricoes(individuo, requisitos))
  wlistareqdisc = verificar_restricoes(individuo, requisitos)
  #print("wlistareqdisc ", wlistareqdisc)
  #print("wlistareqdisc ", wlistareqdisc)
  #print("\n")
  return wlistareqdisc











# verifica se o requisito esta no mesmo semestre e atribui pesos
def verreqsem(individuo, indpi):
  requisitos = []
  pesomesmo = 0
  for i in range(len(individuo)):
    disc = individuo[i]
    pos = mat.index(disc)
    if isinstance(req[pos], list):
      requisitos.append(req[pos])
    else:
      requisitos.append([req[pos]])
  #
  #print("individuo", individuo)
  #print("requisitos", requisitos)
  agrupados2 = []
  agrupados3 = []
  grupo_atual2 = []
  grupo_atual3 = []
  # Inicialização do grupo anterior com um valor que não aparece na lista
  grupo_anterior = None
  # Iterar sobre as listas e agrupar os elementos
  print("AAAAAAAAAAAAAAAAAAAAAA", indpi, individuo, requisitos)
  for grupo, elemento2, elemento3 in zip(indpi, individuo, requisitos):
    # grupo -> semestre inicial do individuo
    # elemento2 -> codigo da disciplina
    # elemento3 -> lista de requisitos
    print(grupo, elemento2, elemento3)
    if grupo != grupo_anterior:
      if grupo_atual2 and grupo_atual3:  # Se os grupos atuais não estiverem vazios, adiciona à lista de grupos
        agrupados2.append(grupo_atual2)
        agrupados3.append(grupo_atual3)
      grupo_atual2 = [elemento2]  # Inicia um novo grupo
      grupo_atual3 = elemento3.copy()  # Inicia um novo grupo (lista de listas)
      grupo_anterior = grupo
    else:
      grupo_atual2.append(elemento2)  # Adiciona ao grupo atual
      grupo_atual3.extend(elemento3)  # Adiciona ao grupo atual (lista de listas)
  if grupo_atual2 and grupo_atual3:
    agrupados2.append(grupo_atual2)
    agrupados3.append(grupo_atual3)
  resultados = []
  for i in range(len(agrupados2)):
    lista2 = agrupados2[i]
    lista3 = agrupados3[i]
    soma = 0
    for elem in lista3:
      print("elemento e lista2:", elem, lista3, lista2)
      if (elem != 0):
        if (elem in lista2):
          soma += 1
        else:
          soma += 0
    resultados.append(soma)
  print("Lista de listas agrupadas 2:", agrupados2)
  print("Lista de listas agrupadas 3:", agrupados3)
  print("resultados ", resultados)
  #print("requisitos ", requisitos)
  pesomesmo = sum(resultados)
  return pesomesmo








#  ordenar a populacao em relação aos menores pesos
def ordenarpopulacao(populacao, listpesos):
  pares_ordenados = sorted(zip(listpesos, populacao))
  _, popordenada = zip(*pares_ordenados)
  popordenada = list(popordenada)
  #print("ordenacao da populacao")
  return popordenada

def ag(tampopulacao, geracoes):
  popinit = criar_populacao(tampopulacao)
  for _ in range(geracoes):
    print("\n*geracao*")
    # gera populacao simulando cruzamento
    popcross = crossover(popinit)
    populacao = popinit + popcross
    print(populacao)

    #populacao.insert(0, matob)
    #print(populacao)

    semestrespi = []
    # agrupa disciplinas por semestres pares e impares (ou 3 para optativa)
    for i in range(len(populacao)):
      individuo = populacao[i]
      semestrespi.append(parimpar(individuo)) # lista de individos por par e impar

    quantidade_semestres = []
    listsomas = []
    # soma a quantidade de semestres por individuo e soma a quantidade de disciplinas por semestres
    for i in range(len(populacao)):
      listpi = semestrespi[i]
      #print(listpi)
      quantidade_semestres.append(quantsemestres(listpi))
      listsomas.append(somaseqsemestres(listpi))

    #crsemestre = []
    ############### soma quantidade de creditos por individuo

    semindpi = []
    wsemindpi = []
    # lista de individuos que iniciam com disciplinas pares ou impares (para atribuir pesos de acordo com a oferta do proximo semestre, considerar os individuos ou descartar)
    for i in range(len(populacao)):
      individuo = populacao[i]
      semindpi.append(individuopi(individuo))
    for i in range(len(semindpi)):
      if (semindpi[i] == semestreparimpar):
        wsemindpi.append(0)
      else:
        wsemindpi.append(len(mat))

    #atribui pesos aos semestres com mais de 7 disciplinas e menos de 3 disciplinas por semestre
    wsomadiscsemestres = []
    for i in range(len(populacao)):
      aux = listsomas[i]
      print("semindpi", semindpi)
      #semindpi é uma lista de par impar do primeiro elemento(semestre) de cada individuo da populacao
      if (semindpi[i] == semestreparimpar):
        wsomadiscsemestres.append(somadiscsemestres(aux))
      else:
        wsomadiscsemestres.append(len(mat))

    wlistrequisito = []
    # lista de semestres que violam as restricoes
    # verificacao por individuo
    # se a disciplina não tem requisito lista recebe zero
    # se a disciplina tem requisito e nao aparece antes a atual disciplina conta 1 para cada violacao (pq pode ser uma lista de requisitos)
    for i in range(len(populacao)):
      individuo = populacao[i]
      if (semindpi[i] == semestreparimpar):
        wlistrequisito.append(verrequisito(individuo))
      else:
        wlistrequisito.append(len(individuo)*2)
    #print("wlistrequisito ", wlistrequisito)

    wreqsemigual = []
    # verifica se o requisito esta no mesmo semestre e atribui peso
    for i in range(len(populacao)):
      individuo = populacao[i]
      indpi = semestrespi[i]
      if (semindpi[i] == semestreparimpar):
        wreqsemigual.append(verreqsem(individuo,indpi))
      else:
        wreqsemigual.append(len(individuo)*2)

    somapesos = []
    # soma os pesos
    #somapesos = [a + b + c + d for a, b, c, d in zip(quantidade_semestres, wsemindpi, wsomadiscsemestres, wlistrequisito)]
    #somapesos = [a + b + c for a, b, c in zip(quantidade_semestres, wsomadiscsemestres, wlistrequisito)]
    somapesos = [a + b + c for a, b, c in zip(wsomadiscsemestres, wlistrequisito, wreqsemigual)]
    #somapesos = [a + b + c + d for a, b, c, d in zip(crsemestre, wsemindpi, wsomadiscsemestres, wlistrequisito)]

    # ajusta a populacao para os individuos com menores pesos (popint)
    listpesos = somapesos # recebe a lista final de pesos da avaliacao
    populacaoordenada = ordenarpopulacao(populacao, listpesos)
    metade = len(populacao)//2
    popinit = populacaoordenada[:metade]

    print("par ou impar ", semestrespi)
    #print("soma disc/sem ", listsomas)
    #print(">7: 12, =3: 1, <=2: 2")
    #print(populacaoordenada)
    #print(semindpi)
    print("quant semestres ", quantidade_semestres)
    print("w p/i quant ", wsomadiscsemestres)
    #print("wsemindpi ", wsemindpi)
    print("wlistareqdisc ", wlistrequisito)
    print("wreqsemigual ", wreqsemigual)
    print("somapesos ", somapesos)
    print("\n ")
    print("melhores ", popinit)

    # os 3 melhores individuos
    prim = populacaoordenada[0]
    seg = populacaoordenada[1]
    terc = populacaoordenada[3]
    #print(primeiro)
    #print(segundo)
    #print(terceiro)
    print("par ou impar ", semestrespi)
  return prim, seg, terc

# imprimir as disciplinas
primeiro, segundo, terceiro = ag(tampopulacao, geracoes)
print("\n")
#print("1o: ", primeiro)
#print("2o: ", segundo)
#print("3o: ", terceiro)

print("\n1a sugestão:")
for i in range(len(primeiro)):
  disc = primeiro[i]
  pos = matreg.index(disc)
  print("\n ", nomes[pos])

print("\n2a sugestão:")
for i in range(len(segundo)):
  disc = segundo[i]
  pos = matreg.index(disc)
  print("\n ", nomes[pos])


#print("\n3a sugestão:")
#for i in range(len(terceiro)):
  #disc = terceiro[i]
  #pos = matreg.index(disc)
  #print("\n ", nomes[pos])

  '''
Lista de listas agrupadas 2: [[33, 37], [29, 27, 28, 26], [35, 36, 34], [40], [46]]
Lista de listas agrupadas 3: [[0, 0], [0, 0, 0, 0], [26, 27, 28, 29, 0, 0], [35, 26, 27, 28, 29, 33, 34, 37, 36], [40, 35, 33, 34, 36, 37, 26, 27, 28, 29]]
resultados  [0, 0, 0, 0, 0]

(2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 2)
'''