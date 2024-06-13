import numpy as np
import random
import json
import math
SEMESTRE_ATUAL = 3
# 1 - ler o csv - ok
# 2 - atribuir o peso de cada disciplina - ok
# 3 - embaralhar as disciplinas [montar cromossomo] - ok
# 4 - somar o peso de cada cromossomo - ok
# 5 - ordernar pelo menor peso
    #[] ordernar pelo menor peso, considerando a diferença de semestre. com isso, considerar as disciplinas de semestre inicial antes das disciplinas finais;
# 6 - os 100 primeiros são usados na população inicial - ok
# 7 - Escolher as melhores opções por semestre
# 8 - 10 sugestões finais
#https://www.youtube.com/watch?v=CfccRjKrmVY&list=PLNa5V12lHXCx-B--e8BwlmS_8GH8WAXfW&index=6

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
       return f' "{self.codigo}, {self.nome}", {self.semestre}'
    def lerGradeJson():
        with open('matriz.json', 'r', encoding='utf8') as arquivo:
            teste = arquivo.read()
        disciplinas = json.loads(teste)
        grade=[]
        for i in range(len(disciplinas)):
            grade.append(Disciplina(disciplinas[i]['codigo'], disciplinas[i]['nome'], disciplinas[i]['semestre'], disciplinas[i]['horas'], disciplinas[i]['requisito'], disciplinas[i]['obrigatoria'], disciplinas[i]['pago'], disciplinas[i]['peso'], 0))
        return grade
    def lerGrade():
        #ler o csv com o histórico do aluno
        dados = []
        teste = np.genfromtxt('matriz.csv', dtype='str', delimiter=',', encoding='utf8')
        codigo, nome, semestre, horas, requisito, obrigatoria, pago, peso = np.genfromtxt('matriz.csv',
                            delimiter=',',
                            unpack=True,
                            dtype='str', 
                            encoding="utf8")
        grade = Disciplina(codigo, nome, semestre, horas, requisito, obrigatoria, pago, peso)
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
        #t_lista = len(lista)
        #t_disciplinas = len(disciplinas)
        i = 0
        cont = 0
        while disciplinas:
            #print(disciplinas[i])
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
        lista = []
        cont = 0
        i = 0
        # verificar o semestre_atual da disciplina,se for par par ou impar impar, então penaliza +=2
        populacao, semestres = Disciplina.agruparSemestre(individuo, 0) #- 0 par e 1 impar
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
        for i in range(len(semestres)-1):
            if(semestres[i]==semestres[i+1]):
                peso+=10
        while aux:
            #print(aux[i], "-------", lista)
            if(Disciplina.verificaPreRequisito(aux[i], lista)==True):
                lista.append(aux[i])
                del(aux[i])
                i=0
            else:
                i+=1
                cont+=2 
                #print("contadooor", cont)
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
        '''if(len(set(filho))==len(set(disciplinas))):
            return True'''
    def encontraDuplicacao(elemento, lista):
        cont = 0
        for i in range(len(lista)):
            if(elemento == lista[i]):
                cont+=1
        return cont
    def agruparSemestre(disciplinas, atual):
        print("individuo", disciplinas)
        final = []
        impar = []
        par = []
        c_max_par = 0
        c_max_impar = 0
        semestre = []
        i=0
        cont=0
        if(atual==0):
            while disciplinas:
                #0 é optativa, 2 semestre par e 1 semestre impar
                #verifica se a disciplina é par ou optitativa
                if(Disciplina.retornaPar(disciplinas[i].semestre) == 0 or Disciplina.retornaPar(disciplinas[i].semestre) == 2):
                    # verifica se atd de horas de par ultrapassa o máximo
                    if(c_max_par + disciplinas[i].horas <=200):
                        #verifica se a lista está vazia, se estiver, então verifica o pre requisito na lista atual
                        if(len(final)==0):
                            if(Disciplina.verificaPreRequisito(disciplinas[i], par)==True):
                                par.append(disciplinas[i])
                                c_max_par+=disciplinas[i].horas
                                del(disciplinas[i])
                                i=0
                            else:
                                i+=1
                        else:
                            for k in range(len(final)):
                                if(Disciplina.verificaPreRequisito(disciplinas[i], final[k])==True):
                                    cont+=1
                            if(len(final)==cont):
                                print('verificando dentro da lista final se a disciplina existe (par)')
                                #se existir então posso adicionar
                                par.append(disciplinas[i])
                                c_max_par+=disciplinas[i].horas
                                #removo a disciplina que adicionei
                                del(disciplinas[i])
                                cont = 0
                                #recomeço na lista 
                                i=0
                            else:
                                i+=1
                    else:
                        if par:
                            final.append(par)
                            semestre.append(2)
                            par = [disciplinas[i]]
                            c_max_par = disciplinas[i].horas
                if(Disciplina.retornaPar(disciplinas[i].semestre) == 1 or Disciplina.retornaPar(disciplinas[i].semestre) == 2):
                    # verifica se atd de horas de par ultrapassa o máximo
                    if(c_max_impar + disciplinas[i].horas <=200):
                        #verifica se a lista está vazia, se estiver, então verifica o pre requisito na lista atual
                        if(len(final)==0):
                            if(Disciplina.verificaPreRequisito(disciplinas[i], impar)==True):
                                impar.append(disciplinas[i])
                                c_max_impar+=disciplinas[i].horas
                                del(disciplinas[i])
                                i=0
                            else:
                                i+=1
                        else:
                            for k in range(len(final)):
                                if(Disciplina.verificaPreRequisito(disciplinas[i], final[k])==True):
                                    cont+=1
                            if(len(final)==cont):
                                print('verificando dentro da lista final se a disciplina existe (impar)')
                                #se existir então posso adicionar
                                impar.append(disciplinas[i])
                                c_max_impar+=disciplinas[i].horas
                                #removo a disciplina que adicionei
                                del(disciplinas[i])
                                cont = 0
                                #recomeço na lista 
                                i=0
                            else:
                                #se não puder adicionar, então pulo para o próximo
                                i+=1
                    else:
                        #ultrapassei o limite maximo de horas
                        #se existir algo em impar
                        if impar:
                            #adiciono a final
                            final.append(impar)
                            semestre.append(1)
                            #comeco a adicionar coisas em impar
                            impar = [disciplinas[i]]
                            c_max_impar = disciplinas[i].horas
            if par:
                print("adiocionari par aqui")
                final.append(par)
                semestre.append(2)
            if impar:
                print("aidiconei impar aquio")
                final.append(impar)
                semestre.append(1)
        return final, semestre
    def agrupaSemestre(disciplinas, atual):
        final = []
        impar = []
        par = []
        c_max_par = 0
        c_max_impar = 0
        qtd_semestre = 0
        if(atual==0):
            for item in disciplinas:
                if Disciplina.retornaPar(item.semestre) == 0 or Disciplina.retornaPar(item.semestre) == 2:
                    if c_max_par + item.horas <= 160 :
                        if Disciplina.verificaPreRequisito(item, final) == True:
                        # se verificaPreRequisito == False, 
                        # então pulo o elemento e adiciono o próximo
                        # se for verdadeiro então adiciono o item e continuo

                        # substituir semestre das optativas por 0 e 
                        # adicionar optativa em qualquer semestre, 
                        # independente se for par ou impar

                        # com o contador, se for impar e o semestre da disciplina for impar, 
                        # então gera um vazio e incrementa o contador
                        # definir uma constante para o semestre vazio
                        ### ajustar para não permitir impar e impar ou par e par
                            par.append(item)
                            c_max_par+=item.horas
                            del[item]
                        else:
                            print("nao pode adicionar")
                    else:
                        if par:
                            final.append(par)
                            #preencher todos com 2 para par e 1 para impar
                            item.semestre_atual = 2
                            par = [item]
                            c_max_par = item.horas
                else:
                    if c_max_impar + item.horas <= 160:
                        impar.append(item)
                        c_max_impar += item.horas
                        del[item]
                    else:
                        if impar:
                            final.append(impar)
                            impar = [item]
                            c_max_impar = item.horas
            if par:
                final.append(par)
            if impar:
                final.append(impar)
        else:
            for item in disciplinas:
                if item.semestre %2 != 0:
                    if c_max_impar + item.horas <= 420:
                        impar.append(item)
                        c_max_impar+=item.horas
                    else:
                        if impar:
                            final.append(impar)
                            impar = [item]
                            c_max_impar = item.horas
                else:
                    if c_max_par + item.horas <= 420:
                        par.append(item)
                        c_max_par += item.horas
                    else:
                        if par:
                            final.append(par)
                            par = [item]
                            c_max_par = item.horas
            if impar:
                final.append(impar)
            if par:
                final.append(par)
        return final, qtd_semestre
    def retornaPar(x):
        if(x==0):
            return 0
        elif(x%2==0):
            return 2
        else:
            return 1
def main():
    pop, peso = Disciplina.criaPopulacaoInicial(10)
    nova_populacao = []
    t_pop = len(pop)*2
    for i in range(2):
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
    '''for i in range(len(pop)):
        print(pop[i], peso[i])'''
    print()
    print("Melhor grade: ", pop[ind], "\n", Disciplina.agrupaSemestre(pop[ind], 0), "\nCom peso", menor)
if __name__ == '__main__':
    main()
# lista de disciplinas, aleatória (já tenho) - ok
# gerar populacao inicial - ok
# cruzamento das disciplinas - ok
# algoritmo de agrupamento de qual disciplina será por semestre (considerar o semestre atual) - carga horário máxima e pré-requisito (se ultrapassar então é o máximo por semestre)
    # Ordernar a lista de disciplinas de acordo com a ordem a ser paga, considerando os pré-requisitos] - ok
    # Se tiver um pré-requisito já pago, então altera o parametro da disciplina para sem pré-requisito - ok
# verificar se é válido (repetiu disciplina ou se falta alguma a ser paga) - tem que verificar se não é só a ordem que tá mudando (ou seja eliminar repetidos)
# considerar semestre par e semestre impar - ok
# calcular o peso de acordo com as restrições - ok
    # somatório de alterações necessárias para ordernar a lista acrescenta um peso
    # a intenção é o que menos tem alteração ter o menor peso e ser melhor
    # algoritmo de ordenação simples

    # considerar a quantidade final de semestres, quantas mais semestres maior será o peso (plus)
# o resultado é a nova população 
# 1.000 interações


# verificar disciplina a disciplina se tem pré-requisito e ordernar pelo pré-requisito
# lista 1, lista 2
# se o elemento existe não tem pre rquisito ele entra na lista 2 e considera o semestre que eu tô, se o próximo elemento tem pre requisito e não tá na lista 2, então ele não entra e pula para o próximo, até que todoso os elementos da lista 1 estejam na lista 2
# isso depois que o pre requisito for eliminado na lista de não pagos, se já tiver pago 
## a cada geração de agrupamento de semestre, será necessário marcar a disciplina do semstre gerado como pago (plus)



## 1 - tem que ler os pre requisitos como lista - ok
## 2 - considerar que eu já paguei tudo de um semestre 
## 3 - usar a função de seleção para retirar os que estão repetidos dentro do semestre, só seleciono o individuo que não for repetido
## 5 - joga na função de avaliação
## 6 - seleciona os n melhores, de menor peso
## 7 - repete o processo
'''d =  [[ "Programação Paralela", 6], [ "Optativa X", 7,  "Optativa VIII", 7,  "Optativa I", 5,  "Optativa III", 5,  "Redes de Computadores", 5,  "Optativa VI", 7,  "Métodos Formais", 5], [ "Sistemas Distribuídos", 6], [ "Sistemas Operacionais", 5,  "Inteligência Artificial", 5], [ "Arquitetura de Computadores", 4,  "Projeto de Graduação", 6], [ "Programação Paralela", 6,  "Computação Gráfica", 6], [ "Sistemas Operacionais", 5], [ "Teoria Geral de Administração e Empreendedorismo", 6], [ "Optativa VII", 7,  "Optativa X", 7,  "Métodos Formais", 5,  "Redes de Computadores", 5], [ "Projeto de Graduação", 6], [ "Projeto de Trabalho de Conclusão de Curso", 7], [ "Trabalho de Conclusão de Curso", 8]]
lista = set(d)
print(lista)'''