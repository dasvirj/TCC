import numpy as np
import random
import json
import math
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
       return f' {self.nome}'
    def lerGradeJson():
        with open('matriz.json', 'r', encoding='utf8') as arquivo:
            teste = arquivo.read()
        disciplinas = json.loads(teste)
        grade=[]
        for i in range(len(disciplinas)):
            grade.append(Disciplina(disciplinas[i]['codigo'], disciplinas[i]['nome'], disciplinas[i]['semestre'], disciplinas[i]['horas'], disciplinas[i]['requisito'], disciplinas[i]['obrigatoria'], disciplinas[i]['pago'], disciplinas[i]['peso'], 0))
        return grade
    def verificaPreRequisito(individuo, requisitos):
        #quero saber se cada elemento da minha lista de requisitos aparece no individuo, então verifico o código de cada uma das disciplinas do individuo
        # se for igual então adiciono 0, se não aparecer então adiciono 1
        #requisitos é uma lista
        lista = []
        if(len(requisitos)==1):
            if(requisitos[0]==0):
                lista.append(0)
        for i in range(len(individuo)):
            if(individuo[i].codigo in requisitos):
                lista.append(0)
            else:
                lista.append(1)
        return sum(lista)
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
    def ordenaGrade(elemento, individuo):
        t = len(elemento.requisito)
        resultado=[]
        for i in range(t):
            if elemento.requisito[i] in individuo.codigo:
                resultado.append(0)
            else:
                resultado.append(1)
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
    def avaliaIndividuo(disciplinas):
        peso=0
        # quantidade de semestres
        individuo = Disciplina.parimpar(disciplinas)
        qtd_semestre = Disciplina.qtdSemestres(individuo)
        # quantidade de disciplinas por semestre
        qtd_disc_semestre = Disciplina.somaSemestre(individuo)
        #print(individuo, "\n", qtd_disc_semestre, qtd_semestre)
        # prerequisito no mesmo semestre
        peso +=qtd_semestre        
        for i in range(len(qtd_disc_semestre)):
            if qtd_disc_semestre[i] > 7:
                peso +=3
            elif qtd_disc_semestre[i]==2:
                peso +=1
            elif qtd_disc_semestre[i] ==1:
                peso+=2
        print(disciplinas)
        print(individuo)
        print(peso)
        for i in range(len(disciplinas)):
            d = disciplinas[:i+1]
            peso += Disciplina.verificaPreRequisito(d, disciplinas[i].requisito)
        
        return peso
    def semestreAtual(individuo):
        inicio = 0
        if(individuo[0].semestre %2==0):
            inicio = 2
        else:
            inicio = 1
        peso = 1
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
    def ordenaPopulacao(populacao, pesos):
        menor = 0
        for i in range(len(pesos)-1):
            menor = i
            for j in range(i+1, len(pesos)):
                if(pesos[j] < pesos[menor]):
                    menor = j
            if(i != menor):
                aux = pesos[i]
                aux2 = populacao[i]
                pesos[i] = pesos[menor]
                populacao[i] = populacao[menor]
                pesos[menor] = aux
                populacao[menor] = aux2
        return populacao, pesos
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
    geracoes = 10
    pop = Disciplina.criaPopulacaoInicial(100)
    pesos=[]
    for i in range(geracoes):
        nova_populacao = Disciplina.cruzaIndividuo(pop)
        populacao = pop + nova_populacao
        for i in range(len(populacao)):
            individuo = populacao[i]
            pesos.append(Disciplina.avaliaIndividuo(individuo))
            #print("lista: ",individuo, "peso:", Disciplina.avaliaIndividuo(individuo))


if __name__ == '__main__':
    main()
'''d =  [[ "Programação Paralela", 6], [ "Optativa X", 7,  "Optativa VIII", 7,  "Optativa I", 5,  "Optativa III", 5,  "Redes de Computadores", 5,  "Optativa VI", 7,  "Métodos Formais", 5], [ "Sistemas Distribuídos", 6], [ "Sistemas Operacionais", 5,  "Inteligência Artificial", 5], [ "Arquitetura de Computadores", 4,  "Projeto de Graduação", 6], [ "Programação Paralela", 6,  "Computação Gráfica", 6], [ "Sistemas Operacionais", 5], [ "Teoria Geral de Administração e Empreendedorismo", 6], [ "Optativa VII", 7,  "Optativa X", 7,  "Métodos Formais", 5,  "Redes de Computadores", 5], [ "Projeto de Graduação", 6], [ "Projeto de Trabalho de Conclusão de Curso", 7], [ "Trabalho de Conclusão de Curso", 8]]
lista = set(d)
print(lista)'''