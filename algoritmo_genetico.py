import numpy as np
import random
import json
import math

tam_populacao = 5
geracoes = 10

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
    def criaPopulacaoInicial(tam):
        # Recebe um tamanho tam e retorna um conjunto de individuos chamado populacao
        populacao = []
        for i in range(tam):
            individuo = Disciplina.criaIndividuo()
            populacao.append(individuo)
        return populacao
    def cruzaIndividuo(populacao):
        aux = []        
        for _ in range(len(populacao)):
            linha = []
            linha = Disciplina.criaIndividuo()
            aux.append(linha.copy())
        return aux
    def parimpar(individuo):
        disciplinas = []
        tam = len(individuo)
        for i in range(tam):
            if(individuo[i].semestre%2==0):
                disciplinas.insert(i, 2)
            else:
                disciplinas.insert(i, 1)
        return disciplinas
    def qtdSemestres(disciplinas):
        lista = disciplinas
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
    def semestreAtual(individuo):
        inicio = 0
        if(individuo[0].semestre %2==0):
            inicio = 2
        else:
            inicio = 1
        return inicio
    def avaliaIndividuo(disciplinas):
        peso = 0
        # quantidade de semestres
        individuo = Disciplina.parimpar(disciplinas)
        qtd_semestre = Disciplina.qtdSemestres(individuo)
        # quantidade de disciplinas por semestre
        qtd_disc_semestre = Disciplina.somaSemestre(individuo)
        #print(individuo, "\n", qtd_disc_semestre, qtd_semestre)
        # prerequisito no mesmo semestre        
        for i in range(len(qtd_disc_semestre)):
            if qtd_disc_semestre[i] > 7:
                peso +=5
            elif qtd_disc_semestre[i] == 2:
                peso +=3
            elif qtd_disc_semestre[i] == 1:
                peso+=4
        peso += qtd_semestre
        return peso
    def verificaPreRequisito(individuo, requisitos):
        #quero saber se cada elemento da minha lista de requisitos aparece no individuo, então verifico o código de cada uma das disciplinas do individuo
        # se for igual então adiciono 0, se não aparecer então adiciono 1
        #requisitos é uma lista
        resultado = []
        subdisc = []
        #print(requisitos)
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
        #auxsoma = sum(resultado)
        print("Lista de individuos que violam os requisitos", resultado)
        return sum(resultado)*5
    def requisitoSemestre(individuo, listaparimpar):
        requisitos=[]
        codigos=[]
        for i in range(len(individuo)):
            requisitos.append(individuo[i].requisito)
            codigos.append(individuo[i].codigo)
        agrupados2 = []
        agrupados3 = []
        semestre_atual2 = []
        semestre_atual3 = []
        semestre_anterior = None
        for semestre, codigo, requisito1 in (zip(listaparimpar, codigos, requisitos)):
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
                if (elem != 0):
                    if elem in lista2:
                        soma += 1
                    else:
                        soma += 0
            resultado.append(soma)
        #print("Resultados:", resultado)
        return sum(resultado)*2
    def retornaRequisitos(individuo):
        requisito = []
        for i in range(len(individuo)):
            if(len(individuo[i].requisito)==1):
                requisito.append(individuo[i].requisito)
            requisito.append(individuo[i].requisito)
        return requisito
    def optativas():
        todas = Disciplina.lerGradeJson()
        optativas =[]
        for i in range(len(todas)):
            if(todas[i].pago!=1 and todas[i].obrigatoria !=1):
                optativas.append(Disciplina(todas[i].codigo, todas[i].nome, todas[i].semestre, todas[i].horas, todas[i].requisito, todas[i].obrigatoria, todas[i].pago, todas[i].peso, todas[i].semestre_atual))                    
        return optativas
    ############### funções auxiliares ###########
    def avaliaPopulacao(populacao):
        peso_total = []
        peso_semestre_atual = []
        peso_pre_requisito = []
        semestres_par_impar = []
        peso_semestre_par_impar = []
        par_impar = []
        requisito = []
        normalizado = []
        for i in range(len(populacao)):
            peso_total.append(Disciplina.avaliaIndividuo(populacao[i]))
            requisito = Disciplina.retornaRequisitos(populacao[i])
            semestres_par_impar.append(Disciplina.semestreAtual(populacao[i]))
            par_impar.append(Disciplina.parimpar(populacao[i]))
            if semestres_par_impar[i] == semestre_inicial:
                peso_semestre_par_impar.append(0)
                peso_pre_requisito.append(Disciplina.verificaPreRequisito(populacao[i], requisito))
                peso_semestre_atual.append(Disciplina.requisitoSemestre(populacao[i], par_impar))
            else:
                peso_semestre_par_impar.append(len(populacao[i]))
                peso_pre_requisito.append(len(populacao[i]))
                peso_semestre_atual.append(len(populacao[i]))
        normalizado = np.full(len(populacao), -1)
        for i in range(len(populacao)):
            if(peso_pre_requisito[i] == 0 and peso_semestre_atual[i] == 0):
                normalizado[i]=0
            if(peso_pre_requisito[i] == 0 and peso_semestre_atual[i] != 0):
                normalizado[i]=1
            if(peso_pre_requisito[i] != 0 and peso_semestre_atual[i] == 0):
                normalizado[i]=2
            if(peso_pre_requisito[i] != 0 and peso_semestre_atual[i] != 0):
                normalizado[i]=3           
        return peso_total, peso_pre_requisito, peso_semestre_atual, peso_semestre_par_impar, normalizado
    def ordenaPopulacao(pop, pesos, normalizado):
        ordenados = list(zip(normalizado, pesos, pop ))
        dados_ordenados = sorted(ordenados, key=lambda x: (x[0], x[1]))
        _,_, popordenada = zip(*dados_ordenados)
        popordenada = list(popordenada)
        return popordenada
def main():
    pop = Disciplina.criaPopulacaoInicial(tam_populacao)
    pesos = []
    semestres = []
    for i in range(geracoes):
        nova_populacao = Disciplina.cruzaIndividuo(pop)
        populacao = pop + nova_populacao
        peso_total, peso_pre_requisito, peso_semestre_atual, peso_semestre_par_impar, normalizado = Disciplina.avaliaPopulacao(populacao)
        print("Peso_total: ", peso_total)
        print("Peso_pre_requisito: ", peso_pre_requisito)
        print("Peso_semestre_atual: ", peso_semestre_atual)
        print("Peso_semestre_par_impar: ", peso_semestre_par_impar)
        pesos = [a + b + c for a, b, c in zip(peso_total, normalizado , peso_semestre_par_impar)]
        #print(populacao)
        #print("------------------metade------------")
        pop_ordenada = Disciplina.ordenaPopulacao(populacao, pesos, normalizado)
        print("Peso final:", pesos)
        print("\n")
        metade =  len(populacao)//2
        nova_populacao = pop_ordenada[:metade]
        #print(nova_populacao)
        #print()
    print("--------------- Melhores resultados -------------")
    print(Disciplina.parimpar(pop_ordenada[0]))
    for i in range(len(populacao[0])):
        print("\n", pop_ordenada[0][i])
    print(Disciplina.parimpar(pop_ordenada[1]))
    for i in range(len(populacao[1])):
        print("\n", pop_ordenada[1][i])
    print(Disciplina.parimpar(pop_ordenada[2]))
    for i in range(len(populacao[2])):
        print("\n", pop_ordenada[2][i])
if __name__ == '__main__':
    main()
'''d =  [[ "Programação Paralela", 6], [ "Optativa X", 7,  "Optativa VIII", 7,  "Optativa I", 5,  "Optativa III", 5,  "Redes de Computadores", 5,  "Optativa VI", 7,  "Métodos Formais", 5], [ "Sistemas Distribuídos", 6], [ "Sistemas Operacionais", 5,  "Inteligência Artificial", 5], [ "Arquitetura de Computadores", 4,  "Projeto de Graduação", 6], [ "Programação Paralela", 6,  "Computação Gráfica", 6], [ "Sistemas Operacionais", 5], [ "Teoria Geral de Administração e Empreendedorismo", 6], [ "Optativa VII", 7,  "Optativa X", 7,  "Métodos Formais", 5,  "Redes de Computadores", 5], [ "Projeto de Graduação", 6], [ "Projeto de Trabalho de Conclusão de Curso", 7], [ "Trabalho de Conclusão de Curso", 8]]
lista = set(d)
print(lista)'''


#Agrupamento das disciplinas e verreqsem 

