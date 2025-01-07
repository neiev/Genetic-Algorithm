"""O problema da mochila: um problema de otimização combinatória.
O nome dá-se devido ao modelo de uma situação em que é necessário
preencher uma mochila com objetos de diferentes pesos e valores.
O objetivo é que se preencha a mochila com o maior valor possível,
não ultrapassando o peso máximo."""
#RODAR COM PYTHON 3!!!

#Importar bibliotecas e dependências
from random import getrandbits,randint,random,choice
import pandas as pd
import matplotlib.pyplot as plt

#[peso,valor]
pesos_e_valores=[
[4, 30.00],
[8, 10.00], 
[8, 30.00],
[25, 75.00],
[2, 10.00],
[50, 100.00], 
[6, 300.00], 
[12, 50.00],
[100, 400.00],
[8, 300.00]
]

n_de_cromossomos=150
n_de_itens=len(pesos_e_valores) #Analogo aos pesos e valores
peso_maximo=100
geracoes=100

#Cria um membro da população
def individual(n_de_itens):
    return [getrandbits(1) for x in range(n_de_itens)]

#Cria a população
def population(n_de_cromossomos,n_de_itens):
    return [individual(n_de_itens) for x in range(n_de_cromossomos)]

#Faz avaliacao do individuo
def fitness(individuo,peso_maximo,pesos_e_valores):
    peso_total,valor_total=0,0
    for i in range(len(individuo)):
        peso_total+=(individuo[i]*pesos_e_valores[i][0])
        valor_total+=(individuo[i]*pesos_e_valores[i][1])
    if peso_maximo-peso_total<0:
        return -1 #retorna -1 no caso de peso excedido
    return valor_total #se for um individuo válido, retorna seu valor. Sendo maior melhor

#Encontra a avalição média da população
def media_fitness(populacao,peso_maximo,pesos_e_valores): #só leva em consideracao os elementos que respeitem o peso maximo da mochila 
    summed=sum(fitness(individuo,peso_maximo,pesos_e_valores) for individuo in populacao if fitness(individuo,peso_maximo,pesos_e_valores)>=0)
    return summed/(len(populacao)*1.0)

#Seleciona um pai e uma mãe baseado nas regras da roleta
def selecao_roleta(pais):
    def sortear(fitness_total,indice_a_ignorar=-1): #2 parametro garante que não vai selecionar o mesmo elemento

        #Monta roleta para realizar o sorteio
        roleta,acumulado,valor_sorteado=[],0,random()

        if indice_a_ignorar!=-1: #Desconta do total, o valor que sera retirado da roleta
            fitness_total-=valores[0][indice_a_ignorar]

        for i,j in enumerate(valores[0]):
            if indice_a_ignorar==i: #ignora o valor ja utilizado na roleta
                continue
            acumulado+=j
            roleta.append(acumulado/fitness_total)
            if roleta[-1]>=valor_sorteado:
                return i
    
    valores=list(zip(*pais)) #cria 2 listas com os valores fitness e os cromossomos
    fitness_total=sum(valores[0])

    indice_pai=sortear(fitness_total) 
    indice_mae=sortear(fitness_total,indice_pai)

    pai=valores[1][indice_pai]
    mae=valores[1][indice_mae]
    
    return pai,mae

#Tabula cada indivíduo e o seu fitness
def evolve(populacao,peso_maximo,pesos_e_valores,n_de_cromossomos,mutate=0.05): 
    pais=[[fitness(individuo,peso_maximo,pesos_e_valores),individuo] for individuo in populacao if fitness(individuo,peso_maximo,pesos_e_valores)>=0]
    pais.sort(reverse=True)
    
    #Reprodução
    filhos=[]
    while len(filhos)<n_de_cromossomos:
        pai,mae=selecao_roleta(pais)
        meio=len(pai)//2
        filho=pai[:meio]+mae[meio:]
        filhos.append(filho)
    
    #Mutação
    for individuo in filhos:
        if mutate>random():
            pos_to_mutate=randint(0,len(individuo)-1)
            if individuo[pos_to_mutate]==1:
                individuo[pos_to_mutate]=0
            else:
                individuo[pos_to_mutate]=1
    return filhos


#Execução dos procedimentos
populacao=population(n_de_cromossomos,n_de_itens)
historico_de_fitness=[media_fitness(populacao,peso_maximo,pesos_e_valores)]

for i in range(geracoes):
    populacao=evolve(populacao,peso_maximo,pesos_e_valores,n_de_cromossomos)
    historico_de_fitness.append(media_fitness(populacao,peso_maximo,pesos_e_valores))

#Prints do terminal
print('\nItens disponíveis\n')
a=pd.DataFrame(pesos_e_valores,columns=['Peso(g)','Valor(R$)'])
a.index.name='Item'
print(a)

print('\nExemplos de boas soluções\n')
b=pd.DataFrame(populacao,columns=['A','B','C','D','E','F','G','H','I','J'])
b.index.name='Solução'
print(b)

print('\nMédia de valor na mochila\n')
c=pd.DataFrame({'Média':historico_de_fitness})
c.index.name='Geração'
print(c)

#Gerador de gráfico
plt.plot(range(len(historico_de_fitness)),historico_de_fitness)
plt.grid(True,zorder=0)
plt.title("Problema da mochila")
plt.xlabel("Geracao")
plt.ylabel("Valor medio da mochila")
plt.show()