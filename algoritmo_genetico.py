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
       return f' "{self.codigo}, {self.nome}", {self.semestre}, {self.requisito}'
    def lerGradeJson():
        with open('tcc/matriz.json', 'r', encoding='utf8') as arquivo:
            teste = arquivo.read()
        disciplinas = json.loads(teste)
        grade=[]
        for i in range(len(disciplinas)):
            grade.append(Disciplina(disciplinas[i]['codigo'], disciplinas[i]['nome'], disciplinas[i]['semestre'], disciplinas[i]['horas'], disciplinas[i]['requisito'], disciplinas[i]['obrigatoria'], disciplinas[i]['pago'], disciplinas[i]['peso'], 0))
        return grade
    def verificaPreRequisito(elemento, disciplinas):
        cont = 0
        while True:
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
                    return False
    def ordenaGrade(disciplinas):
        lista = []
        i = 0
        cont = 0
        while disciplinas:
            if(Disciplina.verificaPreRequisito(disciplinas[i], lista)==True):
                lista.append(disciplinas[i])
                del(disciplinas[i])
                i=0
            else:
                i+=1
        return lista
    def criaIndividuo():
        todas = Disciplina.lerGradeJson()
        disciplinas = []
        for i in range(len(todas)):
            if(int(todas[i].pago)!=1): #-- pago == 0 são as disciplinas que precisam ser tratadas no algoritmo
                disciplinas.append(Disciplina(todas[i].codigo, todas[i].nome, todas[i].semestre, todas[i].horas, todas[i].requisito, todas[i].obrigatoria, todas[i].pago, todas[i].peso, todas[i].semestre_atual))
        for i in range(len(disciplinas)):
            for j in range(len(disciplinas[i].requisito)):
                if(disciplinas[i].requisito[j] != 0):
                    for k in range(len(todas)):
                        if(disciplinas[i].requisito[j] == todas[k].codigo and todas[k].pago == 1):
                            disciplinas[i].requisito[j] = 0
        for i in range(len(disciplinas)):
            for j in range(len(disciplinas[i].requisito)):
                if(len(disciplinas[i].requisito)>1):
                    for elemento in disciplinas[i].requisito[:]:  #cópia da lista para evitar problemas com o loop
                        if elemento == 0:
                            disciplinas[i].requisito.remove(elemento)
                if(len(disciplinas[i].requisito)==0):
                    disciplinas[i].requisito.append(0)
        random.shuffle(disciplinas)
        return Disciplina.ordenaGrade(disciplinas)
    def criaPopulacaoInicial(tam):
        # Recebe um tamanho tam e retorna um conjunto de individuos chamado populacao
        populacao = []
        pesos = []
        for i in range(tam):
            individuo = Disciplina.criaIndividuo()
            populacao.append(individuo)
            pesos.append(Disciplina.avaliaIndividuo(individuo))
        return populacao, pesos
    def roleta(pop, pesos):
        roleta = []
        for i in range(0, len(pesos)):
           prop = math.ceil((pesos[i]*100)/np.sum(pesos))
           for j in range(0, prop):
                roleta.append(i)
        return roleta
    def selecionaIndividuo(populacao, fit):
        roleta = Disciplina.roleta(populacao, fit)
        t = roleta[random.randint(0, len(roleta)-1)]
        a = populacao[t]
        return a
    ############### funções auxiliares ###########
    def avaliaIndividuo(individuo):
        aux = []
        peso=0
        lista = []
        cont = 0
        i = 0
        # verificar o semestre_atual da disciplina,se for par par ou impar impar, então penaliza +=2
        populacao, semestre = Disciplina.agruparSemestre(individuo, 0) #- 0 par e 1 impar
        for i in range(len(populacao)):
            for j in range(len(populacao[i])):
                aux.append(populacao[i][j])
        for i in range(len(populacao)):
            peso = len(populacao[i])
            if(len(populacao[i])>7):
                peso+=8
            if(len(populacao[i])==4):
                peso+=3
            if(len(populacao[i])==3):
                peso+=4
            if(len(populacao[i])==2):
                peso+=5
            if(len(populacao[i])==1):
                peso+=5
        for i in range(len(semestre)-1):
            if(semestre[i] == semestre[i+1]):
                peso+=2
        while aux:
            if(Disciplina.verificaPreRequisito(aux[i], lista)==True):
                lista.append(aux[i])
                del(aux[i])
                i=0
            else:
                i+=1
                cont+=50
        peso+=cont
        return peso
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
    def cruzaIndividuo(pai1, pai2):
        c_n = 0
        c_v = 0
        divisao = int(len(pai1)/2)
        filho1 = pai1[:divisao]+pai2[divisao:]
        filho2 = pai2[:divisao]+pai1[divisao:]
        if(Disciplina.validaFilho(filho1, pai1) == True and Disciplina.validaFilho(filho2, pai1) == True):
            c_n+=1
            print("nao valido")
            return filho1, filho2
        else:
            c_v+=1
            print("valido")
            return pai1, pai2
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
    def validaFilho(filho, disciplinas):
        # ver se tem repetidos ou se ta faltando disciplina
        for i in range(len(filho)):
            if(Disciplina.encontraDuplicacao(filho[i], filho)>1):
                return False
    def encontraDuplicacao(elemento, lista):
        cont = 0
        for i in range(len(lista)):
            if(elemento == lista[i]):
                cont+=1
        return cont
    def agruparSemestre(disciplinas, atual):
        final = []
        impar = []
        par = []
        c_max_par = 0
        c_max_impar = 0
        semestres = []
        i=0
        cont=0
        print("individuo", disciplinas)
        if(atual==0):
            while disciplinas:
                if(len(disciplinas)==0):
                    break
                if(Disciplina.retornaPar(disciplinas[i].semestre) == 2):
                    if(c_max_par + disciplinas[i].horas <=420):
                        if par:
                            for j in range(len(disciplinas[i].requisito)):
                                for k in range(len(par)):
                                    if(disciplinas[i].requisito[j]==par[k].codigo):
                                        cont+=1
                            if(cont!=0):
                                final.append(par)
                                semestres.append(2)
                                par = [disciplinas[i]]
                                c_max_par = disciplinas[i].horas
                                del(disciplinas[i])
                                i=0
                                cont=0
                        if(len(final)>0):
                            for k in range(len(final)):
                                if(Disciplina.verificaPreRequisito(disciplinas[i], final[k])==True):
                                     cont+=1
                            if(len(final)==cont):
                                print('verificando dentro da lista final se a disciplina existe')
                                par.append(disciplinas[i])
                                c_max_par+=disciplinas[i].horas
                                del(disciplinas[i])
                                i=0
                            else:
                                final.append(par)
                                semestres.append(2)
                                par = [disciplinas[i]]
                                c_max_par = disciplinas[i].horas
                                del(disciplinas[i])
                                i=0
                                '''cont = 0
                                print("nao pode adicionar par", i)
                                aux = disciplinas[i]
                                del(disciplinas[i])
                                disciplinas.insert(len(disciplinas), aux)
                                aux = 0
                                i=0 '''
                        else:
                            par.append(disciplinas[i])
                            c_max_par+=disciplinas[i].horas
                            del(disciplinas[i])
                            i=0
                    else:
                        if par:
                            final.append(par)
                            semestres.append(2)
                            par = [disciplinas[i]]
                            c_max_par = disciplinas[i].horas
                            del(disciplinas[i])
                            i=0
                if(len(disciplinas)==0):
                    break
                if(Disciplina.retornaPar(disciplinas[i].semestre) == 1):
                    if(c_max_impar + disciplinas[i].horas <=420):
                        if impar:
                            for j in range(len(disciplinas[i].requisito)):
                                for k in range(len(impar)):
                                    if(disciplinas[i].requisito[j]==impar[k].codigo):
                                        cont+=1
                            if(cont!=0):
                                final.append(impar)
                                semestres.append(1)
                                impar = [disciplinas[i]]
                                c_max_impar = disciplinas[i].horas
                                del(disciplinas[i])
                                i=0
                                cont=0
                        if(len(final)>0):
                            for k in range(len(final)):
                                if(Disciplina.verificaPreRequisito(disciplinas[i], final[k])==True):
                                     cont+=1
                            if(len(final)==cont):
                                print('verificando dentro da lista final se a disciplina existe')
                                impar.append(disciplinas[i])
                                c_max_impar+=disciplinas[i].horas
                                del(disciplinas[i])
                                i=0
                            else:
                                final.append(impar)
                                semestres.append(2)
                                impar = [disciplinas[i]]
                                c_max_impar = disciplinas[i].horas
                                del(disciplinas[i])
                                i=0
                                '''cont = 0
                                print("nao pode adicionar par", i)
                                aux = disciplinas[i]
                                del(disciplinas[i])
                                disciplinas.insert(len(disciplinas), aux)
                                aux = 0
                                i=0 '''
                        else:
                            impar.append(disciplinas[i])
                            c_max_impar+=disciplinas[i].horas
                            del(disciplinas[i])
                            i=0
                    else:
                        if impar:
                            final.append(impar)
                            semestres.append(1)
                            impar = [disciplinas[i]]
                            c_max_impar = disciplinas[i].horas
                            del(disciplinas[i])
                            i=0
                if(len(disciplinas)==0):
                    break
                if(Disciplina.retornaPar(disciplinas[i].semestre)==0):
                    if(c_max_par + disciplinas[i].horas <=420):
                        par.append(disciplinas[i])
                        c_max_par+=disciplinas[i].horas
                        del(disciplinas[i])
                        i=0
                    if(len(disciplinas)==0):
                        break
                    if(c_max_impar + disciplinas[i].horas <=420):
                        impar.append(disciplinas[i])
                        c_max_impar+=disciplinas[i].horas
                        del(disciplinas[i])
                        i=0
            if par:
                final.append(par)
                semestres.append(2)
            if impar:
                final.append(impar)
                semestres.append(1)
        print("AAAAAAAAAAAAAAAAA", final)
        return final, semestres
    def retornaPar(x):
        if(x==0):
            return 0
        elif(x%2==0):
            return 2
        else:
            return 1
def main():
    pop, peso = Disciplina.criaPopulacaoInicial(1)
    nova_populacao = []
    t_pop = len(pop)*2
    for i in range(1):
        while len(nova_populacao) < t_pop:
            pai = Disciplina.selecionaIndividuo(pop, peso)
            mae = Disciplina.selecionaIndividuo(pop, peso)
            filho1, filho2 = Disciplina.cruzaIndividuo(pai, mae)
            nova_populacao.append(filho1)
            nova_populacao.append(filho2)
        peso = Disciplina.avaliaPopulacao(nova_populacao)
        nova_populacao, peso = Disciplina.ordenaPopulacao(nova_populacao, peso)
        pop = nova_populacao[:len(pop)]
    menor, ind = Disciplina.menorElemento(peso)
    print("Melhor grade: ", pop[ind], "\n", Disciplina.agruparSemestre(pop[ind], 0), "\nCom peso", menor)
if __name__ == '__main__':
    main()
'''d =  [[ "Programação Paralela", 6], [ "Optativa X", 7,  "Optativa VIII", 7,  "Optativa I", 5,  "Optativa III", 5,  "Redes de Computadores", 5,  "Optativa VI", 7,  "Métodos Formais", 5], [ "Sistemas Distribuídos", 6], [ "Sistemas Operacionais", 5,  "Inteligência Artificial", 5], [ "Arquitetura de Computadores", 4,  "Projeto de Graduação", 6], [ "Programação Paralela", 6,  "Computação Gráfica", 6], [ "Sistemas Operacionais", 5], [ "Teoria Geral de Administração e Empreendedorismo", 6], [ "Optativa VII", 7,  "Optativa X", 7,  "Métodos Formais", 5,  "Redes de Computadores", 5], [ "Projeto de Graduação", 6], [ "Projeto de Trabalho de Conclusão de Curso", 7], [ "Trabalho de Conclusão de Curso", 8]]
lista = set(d)
print(lista)'''