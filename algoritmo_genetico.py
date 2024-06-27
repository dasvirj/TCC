import numpy as np
import random
import json
from app import app 
#interface do usuário -> Listar todas as disciplinas e selecionar as que já pagou -> csv
class Disciplina:
    def __init__(self, codigo, nome, semestre, horas, requisito, obrigatoria, pago, peso):
        self.nome = nome
        self.codigo = codigo
        self.semestre = semestre
        self.horas = horas
#0 para sem pre-requisito, codigo da disciplina que é pre-requisito caso tenha
        self.requisito = requisito
        self.pago = pago
        self.peso = peso
        self.obrigatoria = obrigatoria
    def __repr__(self):
        return json.dumps({
            'codigo': self.codigo,
            'nome': self.nome
        })
    def lerGradeJson(nome_arquivo):
        with open(nome_arquivo, 'r', encoding='utf8') as arquivo:
            teste = arquivo.read()
        disciplinas = json.loads(teste)
        grade=[]
        for i in range(len(disciplinas)):
            grade.append(Disciplina(disciplinas[i]['codigo'], disciplinas[i]['nome'], disciplinas[i]['semestre'], disciplinas[i]['horas'], disciplinas[i]['requisito'], disciplinas[i]['obrigatoria'], disciplinas[i]['pago'], disciplinas[i]['peso'], 0))
        return grade
    def lerJson(data):
        disciplinas = []
        # Iterar sobre as disciplinas na matriz
        for disciplina_json in data['matriz']:
        # Criar objeto Disciplina para cada disciplina
            disciplina = Disciplina(
                disciplina_json['codigo'],
                disciplina_json['nome'],
                disciplina_json['semestre'],
                disciplina_json['horas'],
                disciplina_json['requisito'],
                disciplina_json['obrigatoria'],
                disciplina_json['pago'],
                disciplina_json['peso']
            )
            # Adicionar disciplina à lista
            disciplinas.append(disciplina)
        return disciplinas
    def __lt__(self, other):
        # Define como comparar duas instâncias de Disciplina
        # Aqui, por exemplo, pode-se comparar pela carga horária
        return self.peso < other.peso
    def criaIndividuo(dados):
        todas = Disciplina.lerJson(dados)
        #todas = Disciplina.lerGradeJson(nome_arquivo)
        obrigatorias = []
        for i in range(len(todas)):
            if(todas[i].pago!=1 and todas[i].obrigatoria == 1): 
                obrigatorias.append(Disciplina(todas[i].codigo, todas[i].nome, todas[i].semestre, todas[i].horas, todas[i].requisito, todas[i].obrigatoria, todas[i].pago, todas[i].peso))
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
        return obrigatorias
    def criaPopulacaoInicial(dados, tam):
        # Recebe um tamanho tam e retorna um conjunto de individuos chamado populacao
        populacao = []
        for i in range(tam):
            individuo = Disciplina.criaIndividuo(dados)
            populacao.append(individuo)
        return populacao
    def cruzaIndividuo(dados, populacao):
        aux = []
        for _ in range(len(populacao)):
            linha = []
            linha = Disciplina.criaIndividuo(dados)
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
        # pre requisito no mesmo semestre
        for i in range(len(qtd_disc_semestre)):
            if qtd_disc_semestre[i] > 7:
                peso += 8
            elif qtd_disc_semestre[i] == 5:
                peso += 0
            elif qtd_disc_semestre[i] == 4:
                peso += 3
            elif qtd_disc_semestre[i] == 3:
                peso += 4
            elif qtd_disc_semestre[i] == 2:
                peso += 5
            elif qtd_disc_semestre[i] == 1:
                peso += 6
        peso += qtd_semestre
        return peso * 2
    def verificaPreRequisito(individuo, requisitos):
        #quero saber se cada elemento da minha lista de requisitos aparece no individuo, então verifico o código de cada uma das disciplinas do individuo
        # se for igual então adiciono 0, se não aparecer então adiciono 1
        #requisitos é uma lista
        resultado = []
        subdisc = []
        codigos=[]
        for i in range(len(individuo)):
          codigos.append(individuo[i].codigo)
        tamsubreq = [len(item) if isinstance(item, list) else 0 for item in requisitos] # lista o tamanho da lista de requisitos de cada disciplina (disciplinas com um requisito recebe zero tbm)
        cont=0
        for i in range(len(codigos)):
            subdisc = codigos[:(i+1)]
            if (tamsubreq[i] != 0):
                aux = requisitos[i]
                for j in range(len(aux)):
                  for k in range(len(subdisc)):
                    if(aux[j]==0):
                      cont=1
                    else:
                      if(aux[j] == subdisc[k]):
                        cont+=1
                if(cont==len(aux)):
                  resultado.append(0)
                else:
                  resultado.append(1)
                cont=0
        return sum(resultado)*2
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
        return sum(resultado)*2
    def retornaRequisitos(individuo):
        requisito = []
        for i in range(len(individuo)):
            requisito.append(individuo[i].requisito)
        return requisito
    def optativas(nome_arquivo):
        todas = Disciplina.lerGradeJson(nome_arquivo)
        optativas =[]
        for i in range(len(todas)):
            if(todas[i].pago!=1 and todas[i].obrigatoria !=1):
                optativas.append(Disciplina(todas[i].codigo, todas[i].nome, todas[i].semestre, todas[i].horas, todas[i].requisito, todas[i].obrigatoria, todas[i].pago, todas[i].peso))
        return optativas
    ############### funções auxiliares ###########
    def avaliaPopulacao(populacao, semestre_inicial):
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
                normalizado[i]=4
            if(peso_pre_requisito[i] != 0 and peso_semestre_atual[i] == 0):
                normalizado[i]=4
            if(peso_pre_requisito[i] != 0 and peso_semestre_atual[i] != 0):
                normalizado[i]=4
        return peso_total, peso_pre_requisito, peso_semestre_atual, peso_semestre_par_impar, normalizado
    def ordenaPopulacao(pop, pesos, normalizado):
        ordenados = list(zip(normalizado, pesos, pop ))
        dados_ordenados = sorted(ordenados, key=lambda x: (x[0], x[1]))
        _,_, popordenada = zip(*dados_ordenados)
        popordenada = list(popordenada)
        return popordenada
    def exibeGrupos(individuo, listaparimpar):
        requisitos=[]
        codigos=[]
        for i in range(len(individuo)):
            requisitos.append(individuo[i].requisito)
            codigos.append(individuo[i].nome)
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
        return agrupados2
def ag(matriz, tam, geracoes, semestre_inicial):
    pop = Disciplina.criaPopulacaoInicial(matriz, tam)
    pesos = []
    semestres = []
    for i in range(geracoes):
        nova_populacao = Disciplina.cruzaIndividuo(matriz, pop)
        populacao = pop + nova_populacao
        peso_total, peso_pre_requisito, peso_semestre_atual, peso_semestre_par_impar, normalizado = Disciplina.avaliaPopulacao(populacao, semestre_inicial)
        print("Peso_total: ", peso_total)
        print("Peso_pre_requisito: ", peso_pre_requisito)
        print("Peso_semestre_atual: ", peso_semestre_atual)
        print("Peso_semestre_par_impar: ", peso_semestre_par_impar)
        pesos = [a + b for a, b in zip(peso_total, peso_semestre_par_impar)]
        pop_ordenada = Disciplina.ordenaPopulacao(populacao, pesos, normalizado)

        peso_total1, peso_pre_requisito1, peso_semestre_atual1, peso_semestre_par_impar1, normalizado1 = Disciplina.avaliaPopulacao(pop_ordenada, semestre_inicial)
        pesos1 = [a + b for a, b in zip(peso_total1, peso_semestre_par_impar1)]
        print("Peso final:", pesos1)
        print("\n")
        metade =  len(populacao)//2
        pop = pop_ordenada[:metade]
    print("--------------- Melhores resultados -------------")
    print(Disciplina.exibeGrupos(pop_ordenada[1], Disciplina.parimpar(pop_ordenada[1])))
    print(Disciplina.exibeGrupos(pop_ordenada[2], Disciplina.parimpar(pop_ordenada[2])))
    print(Disciplina.exibeGrupos(pop_ordenada[2], Disciplina.parimpar(pop_ordenada[3])))
    print(Disciplina.exibeGrupos(pop_ordenada[2], Disciplina.parimpar(pop_ordenada[4])))
    return Disciplina.exibeGrupos(pop_ordenada[0], Disciplina.parimpar(pop_ordenada[0]))
    
