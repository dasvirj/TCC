import numpy as np
import random
import json
import math

semestre_inicial = 2
#interface do usuário -> Listar todas as disciplinas e selecionar as que já pagou -> csv
class Disciplina:
    def __init__(self, codigo, nome, semestre, horas, requisito, obrigatoria, pago, peso, semestre_atual):
        self.nome = nome
        self.codigo = codigo
        self.semestre = semestre
        self.horas = horas
#0 para sem pre-requisito, codigo da disciplina que é pre-requisito caso tenha
        self.requisito = requisito
        self.pago = pago
        self.peso = peso
        self.obrigatoria = obrigatoria
        self.semestre_atual = semestre_atual
    def __repr__(self):
       return f'{self.nome}'
    def lerGradeJson():
        with open('matriz.json', 'r', encoding='utf8') as arquivo:
            teste = arquivo.read()
        disciplinas = json.loads(teste)
        grade=[]
        for i in range(len(disciplinas)):
            grade.append(Disciplina(disciplinas[i]['codigo'], disciplinas[i]['nome'], disciplinas[i]['semestre'], disciplinas[i]['horas'], disciplinas[i]['requisito'], disciplinas[i]['obrigatoria'], disciplinas[i]['pago'], disciplinas[i]['peso'], 0))
        return grade
    def __lt__(self, other):
        # Define como comparar duas instâncias de Disciplina
        # Aqui, por exemplo, pode-se comparar pela carga horária
        return self.peso < other.peso
    def verificaPreRequisito(individuo, requisitos):
        #quero saber se cada elemento da minha lista de requisitos aparece no individuo, então verifico o código de cada uma das disciplinas do individuo
        # se for igual então adiciono 0, se não aparecer então adiciono 1
        #requisitos é uma lista
        resultado = []
        for i in range(len(individuo)):
            sublist = individuo[:(i+1)]
            if(len(requisitos[i])!=0):
                aux = requisitos[i]
                if(set(aux).issubset(set(sublist))):
                    resultado.append(0)
                else:
                    resultado.append(1)
            elif(len(requisitos[i]) == 0):
                if(requisitos[i]==0):
                    resultado.append(0)
                elif(requisitos[i] not in sublist):
                    resultado.append(1)
        
        return sum(resultado)
        '''while True:
            if(elemento.requisito[0]==0):
                return True
            else:
                for j in range(len(elemento.requisito)):
                    for k in range(len(disciplinas)):
                        if(elemento.requisito[j] == disciplinas[k].codigo):
                            cont+=1
                if(cont==len(elemento.requisito)):
                    return True
                else:
                    return False'''
    def requisitoSemestre(individuo, listaparimpar):
        requisitos=[]
        codigos=[]
        for i in range(len(individuo)):
            requisitos.append(individuo[i].requisito)
            codigos.append(individuo[i].codigo)
        print(requisitos)
        agrupados2 = []
        agrupados3 = []
        semestre_atual2 = []
        semestre_atual3 = []
        semestre_anterior = None
        for semestre, codigo, requisito1 in (zip(listaparimpar, codigos, requisitos)):
            #print(semestre, codigo, requisito)
            if(semestre!=semestre_anterior):
                if(semestre_atual2 and semestre_atual3):
                    agrupados2.append(semestre_atual2)
                    agrupados3.append(semestre_atual3)
                semestre_atual2 = [codigo]
                semestre_atual3 = requisito1.copy()
                semestre_anterior=semestre
            else:
                semestre_atual2.append(codigo)
                semestre_atual3.extend(requisito1)
        if semestre_atual2 and semestre_atual3:
            agrupados2.append(semestre_atual2)
            agrupados3.append(semestre_atual3)
        resultado = []
        for i in range(len(agrupados2)):
            lista2 = agrupados2[i]
            lista3 = agrupados3[i]
            soma = 0
            for elem in lista3:
                print("elemento e lista", elem, lista3, lista2)
                if (elem != 0):
                    if elem in lista2:
                        soma += 1
                    else:
                        soma += 0
            resultado.append(soma)
        '''print("Lista de listas agrupadas 2:", agrupados2)
        print("Lista de listas agrupadas 3:", agrupados3)'''
        print("resultados ", resultado)
        return sum(resultado)
    def criaIndividuo():
        todas = Disciplina.lerGradeJson()
        obrigatorias = []
        optativas =[]
        for i in range(len(todas)):
            if(todas[i].pago!=1 and todas[i].obrigatoria == 1): #-- pago == 0 são as disciplinas que precisam ser tratadas no algoritmo
                obrigatorias.append(Disciplina(todas[i].codigo, todas[i].nome, todas[i].semestre, todas[i].horas, todas[i].requisito, todas[i].obrigatoria, todas[i].pago, todas[i].peso, todas[i].semestre_atual))
        for i in range(len(obrigatorias)):
            for j in range(len(obrigatorias[i].requisito)):
                if(obrigatorias[i].requisito[j] != 0):
                    for k in range(len(todas)):
                        if(obrigatorias[i].requisito[j] == todas[k].codigo and todas[k].pago == 1):
                            obrigatorias[i].requisito[j] = 0
        for i in range(len(obrigatorias)):
            for j in range(len(obrigatorias[i].requisito)):
                if(len(obrigatorias[i].requisito)>1):
                    for elemento in obrigatorias[i].requisito[:]:  #cópia da lista para evitar problemas com o loop
                        if elemento == 0:
                            obrigatorias[i].requisito.remove(elemento)
                if(len(obrigatorias[i].requisito)==0):
                    obrigatorias[i].requisito.append(0)
        random.shuffle(obrigatorias)
        return obrigatorias #Disciplina.ordenaGrade(obrigatorias)
    def optativas():
        todas = Disciplina.lerGradeJson()
        optativas =[]
        for i in range(len(todas)):
            if(todas[i].pago!=1 and todas[i].obrigatoria !=1):
                optativas.append(Disciplina(todas[i].codigo, todas[i].nome, todas[i].semestre, todas[i].horas, todas[i].requisito, todas[i].obrigatoria, todas[i].pago, todas[i].peso, todas[i].semestre_atual))                    
        return optativas
    def criaPopulacaoInicial(tam):
        # Recebe um tamanho tam e retorna um conjunto de individuos chamado populacao
        populacao = []
        for i in range(tam):
            individuo = Disciplina.criaIndividuo()
            populacao.append(individuo)
        return populacao
    def parimpar(individuo):
        disciplinas = []
        #nome = []
        tam = len(individuo)
        for i in range(tam):
            if(individuo[i].semestre%2==0):
                #nome.insert(i, individuo[i].nome)
                disciplinas.insert(i, 2)
            else:
                disciplinas.insert(i, 1)
                #nome.insert(i, individuo[i].nome)
        return disciplinas
    ############### funções auxiliares ###########
    def avaliaIndividuo(semestre, disciplinas):
        peso=0
        requisito = []
        # quantidade de semestres
        individuo = Disciplina.parimpar(disciplinas)
        qtd_semestre = Disciplina.qtdSemestres(individuo)
        # quantidade de disciplinas por semestre
        qtd_disc_semestre = Disciplina.somaSemestre(individuo)
        #print(individuo, "\n", qtd_disc_semestre, qtd_semestre)
        # prerequisito no mesmo semestre        
        for i in range(len(qtd_disc_semestre)):
            if qtd_disc_semestre[i] > 7:
                peso +=3
            elif qtd_disc_semestre[i]==2:
                peso +=1
            elif qtd_disc_semestre[i] ==1:
                peso+=2
        for i in range(len(disciplinas)):
            requisito.append(disciplinas[i].requisito)
        peso += Disciplina.verificaPreRequisito(disciplinas, requisito)
        if(semestre == semestre_inicial):
            peso += qtd_semestre
        else:
            peso+=len(disciplinas)
        peso += Disciplina.requisitoSemestre(disciplinas, individuo)
        return peso
    def semestreAtual(individuo):
        inicio = 0
        if(individuo[0].semestre %2==0):
            inicio = 2
        else:
            inicio = 1
        return inicio
    def avaliaPopulacao(populacao):
        pesos = []
        for i in range(len(populacao)):
            pesos.append(Disciplina.avaliaIndividuo(populacao[i]))
        return pesos
    def menorElemento(lista):
        # pegar o elemento de menor peso
        menor_peso = min(lista)
        index = lista.index(menor_peso)
        return menor_peso, index
    def cruzaIndividuo(populacao):
        aux = []        
        for _ in range(len(populacao)):
            linha = []
            linha = Disciplina.criaIndividuo()
            aux.append(linha.copy())
        return aux
    def ordenaPopulacao(pop, pesos):
        populacao=pop
        pares = sorted(zip(pesos, populacao))
        _, popordenada = zip(*pares)
        popordenada = list(popordenada)
        return popordenada
    def encontraDuplicacao(elemento, lista):
        cont = 0
        for i in range(len(lista)):
            if(elemento == lista[i]):
                cont+=1
        return cont
    def qtdSemestres(disciplinas):
        lista = disciplinas
        #print(disciplinas, lista[0])
        cont_semestre = 1
        ultimo=lista[0]
        for i in lista[1:]:
            if(i!=ultimo):
                cont_semestre+=1
                ultimo=i
        return cont_semestre
    def somaSemestre(disciplinas):
        soma = []
        cont=1
        for i in range(1, len(disciplinas)):
            if(disciplinas[i]==disciplinas[i-1]):
                cont +=1
            else:
                soma.append(cont)
                cont=1
        soma.append(cont)
        return soma
def main():
    geracoes = 1
    pop = Disciplina.criaPopulacaoInicial(2)
    pesos = []
    semestres = []
    for i in range(geracoes):
        nova_populacao = Disciplina.cruzaIndividuo(pop)
        populacao = pop + nova_populacao
        for i in range(len(populacao)):
            individuo = populacao[i]
            semestres.append(Disciplina.parimpar(individuo))
            pesos.append(Disciplina.avaliaIndividuo(semestres[i], individuo))
        pop_ordenada = Disciplina.ordenaPopulacao(populacao, pesos)
        metade =  abs(len(populacao)/2)
        #nova_populacao = pop_ordenada[:metade]
    '''for i in range(len(populacao)):
        print(populacao[i])
        print(pesos[i])'''
    print("--------------- Melhores resultados -------------")
    print(pop_ordenada[0])
    print(Disciplina.parimpar(pop_ordenada[0]))
    print(pop_ordenada[1])
    print(Disciplina.parimpar(pop_ordenada[1]))
    print(pop_ordenada[2])
    print(Disciplina.parimpar(pop_ordenada[2]))

def verreqsem(individuo, indpi):
  agrupados2 = []
  agrupados3 = []
  grupo_atual2 = []
  grupo_atual3 = []
  # Inicialização do grupo anterior com um valor que não aparece na lista
  grupo_anterior = None
  # Iterar sobre as listas e agrupar os elementos
  #lista par e impar, disciplinas, lista de requisitos
  # disciplinas = []
  # pre = []
# if pre[i] in disiciplinas:
  # soma +=1
  for grupo, elemento2, elemento3 in zip(indpi, individuo, requisitos):
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
  #duas listas, lista1 disciplinas do semestre, lista2 pre requisitos das disciplinas, se lista 1 in elemento de lista 2 (mesmo indice), então adiciona
  pesomesmo = sum(resultados)
  print(pesomesmo)
  return pesomesmo

if __name__ == '__main__':
    main()
'''d =  [[ "Programação Paralela", 6], [ "Optativa X", 7,  "Optativa VIII", 7,  "Optativa I", 5,  "Optativa III", 5,  "Redes de Computadores", 5,  "Optativa VI", 7,  "Métodos Formais", 5], [ "Sistemas Distribuídos", 6], [ "Sistemas Operacionais", 5,  "Inteligência Artificial", 5], [ "Arquitetura de Computadores", 4,  "Projeto de Graduação", 6], [ "Programação Paralela", 6,  "Computação Gráfica", 6], [ "Sistemas Operacionais", 5], [ "Teoria Geral de Administração e Empreendedorismo", 6], [ "Optativa VII", 7,  "Optativa X", 7,  "Métodos Formais", 5,  "Redes de Computadores", 5], [ "Projeto de Graduação", 6], [ "Projeto de Trabalho de Conclusão de Curso", 7], [ "Trabalho de Conclusão de Curso", 8]]
lista = set(d)
print(lista)'''


#Agrupamento das disciplinas e verreqsem 

