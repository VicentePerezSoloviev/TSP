from operator import attrgetter
import random, sys, time, copy
import math
import numpy as np
import time

class Particula:        #clase particula
    def __init__ (self, solucion, coste):
        self.solucion = solucion
        self.mejor = solucion
        self.coste_actual = coste
        self.coste_mejor = coste

        self.velocidad = []  #(1,2,3,'alpha')

    def setMejor (self, nuevo_mejor): self.mejor = nuevo_mejor
    def getMejor (self): return self.mejor
    def getVelocidad (self): return self.velocidad
    def setVelocidad (self, nueva): self.velocidad = nueva
    def setActualSolucion (self, actual): self.solucion = actual
    def getActualSolucion (self): return self.solucion
    def getActualCoste (self): return self.coste_actual
    def setActualCoste (self, coste): self.coste_actual = coste
    def getMejorCoste (self): return self.coste_mejor
    def setMejorCoste (self, coste): self.coste_mejor = coste
    def limpiarVelocidad (self): del self.velocidad[:]

def caminoAleatorio(num_particulas, num_vertices):
    lista = list(range(0, num_vertices))
    camino = []

    while len(camino) < num_particulas:
        random.shuffle(lista)
        if lista not in camino:
            camino.append(lista[:])

    return camino

def costeGrafo (solucion):
    costeTotal = 0
    for i in range (len(solucion)-1):
        costeTotal += matriz[solucion[i]][solucion[i+1]]

    costeTotal+=matriz[solucion[0]][solucion[len(solucion)-1]]  #de la ultima ciudad al comienzo tb se suma

    return costeTotal

class AlgoritmoPSO:
    def __init__ (self, grafo, max_iteraciones, N, beta, alpha):
        self.grafo = grafo
        self.MAX_IT = max_iteraciones
        self.N = N
        self.beta = beta
        self.alpha = alpha
        self.particulas = []
        solucion = caminoAleatorio(self.N, len(grafo))       #creamos tantas soluciones aleatorias como particulas queremos

        for sol in solucion:
            particula = Particula(sol, costeGrafo(sol))
            self.particulas.append(particula)
            print (sol)

        self.N = len(self.particulas)

    def setMejor (self, nuevo): self.mejor = nuevo
    def getMejor (self): return self.mejor

    def run(self):
        for i in range(self.MAX_IT):
            self.mejor = min (self.particulas, key=attrgetter('coste_mejor'))

            for particula in self.particulas:       #en cada iteracion recorro todas las particulas

                particula.limpiarVelocidad()
                velocidad_temp = []
                solucion_mejor = copy.copy(self.mejor.getMejor())   #mejor solucion global
                solucion_mejor_ = particula.getMejor()[:]           #mejor solucion de la particula
                solucion_particula = particula.getActualSolucion()[:] #solucion actual de la particula

                for i in range(len(self.grafo)):    #recorro vertices
                    if solucion_particula[i] != solucion_mejor_[i]:
                        cambiar = (i, solucion_mejor_.index(solucion_particula[i]), self.alpha)
                        velocidad_temp.append((cambiar))
                        aux = solucion_mejor_[cambiar[0]]
                        solucion_mejor_[cambiar[0]] = solucion_mejor_[cambiar[1]]
                        solucion_mejor_[cambiar[1]] = aux

                for i in range(len(self.grafo)):
                    if solucion_particula[i] != solucion_mejor[i]:
                        cambiar = (i, solucion_mejor.index(solucion_particula[i]), self.beta)
                        velocidad_temp.append((cambiar))
                        aux = solucion_mejor[cambiar[0]]
                        solucion_mejor[cambiar[0]] = solucion_mejor[cambiar[1]]
                        solucion_mejor[cambiar[1]] = aux

                particula.setVelocidad(velocidad_temp)

                for cambiar in velocidad_temp:
                    if random.random() <= cambiar[2]:
                        aux = solucion_particula[cambiar[0]]
                        solucion_particula[cambiar[0]] = solucion_particula[cambiar[1]]
                        solucion_particula[cambiar[1]] = aux

                particula.setActualSolucion(solucion_particula)
                costeSolucionActual = costeGrafo(solucion_particula)
                particula.setActualCoste(costeSolucionActual)

                if costeSolucionActual < particula.getMejorCoste():
                    particula.setMejor(solucion_particula)
                    particula.setMejorCoste(costeSolucionActual)


def cargarMapa():
    f = open("C://Users//Vicente//PycharmProjects//TSPproblem//venv//distances")
    info = []
    num_lineas = 0
    try:
        for linea in f:
            ciudad = []
            for palabra in linea.split(' '):
                ciudad.append(float(palabra))
            info.append(ciudad)
            num_lineas += 1
    finally:
        f.close()


    matriz = np.zeros((len(info), len(info)))
    for i in range (len(info)-1):
        for j in range (i+1, len(info)):
            coste = math.sqrt((info[i][1] - info[j][1]) ** 2 + (info[i][2] - info[j][2]) ** 2)
            matriz[i][j] = coste
            matriz[j][i] = coste

    return matriz

#****************   MAIN  *********************

matriz = cargarMapa()

import matplotlib.pyplot as plt

MAX = 50
it_N = []
it_time = []
it_sol = []
it_MAX = []

for i in range (1):
  start_time = time.time()
  pso = AlgoritmoPSO (matriz, max_iteraciones=MAX, N=100, beta=0.5, alpha=0.5)
  pso.run()

  it_time.append(time.time() - start_time)
  it_sol.append(pso.getMejor().getMejorCoste())
  it_MAX.append(MAX)

  MAX = MAX + 10

  print (it_time)
  print (it_sol)

  print (pso.getMejor().getMejor())

plt.plot(it_MAX, it_sol)

plt.xlabel('population')
plt.ylabel('kms')

plt.show()