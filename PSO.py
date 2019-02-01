from operator import attrgetter
import random, sys, time, copy
import math

class Grafo:
    def __init__ (self, numero_vertices):
        self.arcos = {}
        self.vertices = set()

    def anadirArco (self, inicio, fin, coste):
        if not self.existeArco(inicio, fin):
            self.arcos[(inicio, fin)] = coste
            self.vertices.add(inicio)
            self.vertices.add(fin)

    def existeArco (self, inicio, fin):
        for i in self.arcos:
            if i == (inicio, fin): return True
        return False

    def costeGrafo (self, camino):
        total = 0
        for i in range (len(self.vertices) - 1):
            total = total + self.arcos[(camino[i], camino[i+1])]

        total = total + self.arcos[(camino[len(self.vertices) - 1], camino[0])]
        return total

    def caminoAleatorio (self, N):
        aleatorio, lista = [], list(self.vertices)

        inicial = random.choice(lista)
        lista.remove(inicial)
        lista.insert(0, inicial)

        for i in range (N):
            lista_temp = lista[1:]
            random.shuffle(lista_temp)
            lista_temp.insert(0,inicial)

            if lista_temp not in aleatorio:
                aleatorio.append(lista_temp)

        return aleatorio

class Particula:
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

class AlgoritmoPSO:
    def __init__ (self, grafo, max_iteraciones, N, beta, alpha):
        self.grafo = grafo
        self.MAX_IT = max_iteraciones
        self.N = N
        self.beta = beta
        self.alpha = alpha
        self.particulas = []

        solucion = self.grafo.caminoAleatorio(self.N)
        for sol in solucion:
            particula = Particula(sol, grafo.costeGrafo(sol))
            self.particulas.append(particula)

        self.N = len(self.particulas)

    def setMejor (self, nuevo): self.mejor = nuevo
    def getMejor (self): return self.mejor

    def run(self):
        for i in range(self.MAX_IT):
            self.mejor = min (self.particulas, key=attrgetter('coste_mejor'))
            for particula in self.particulas:
                particula.limpiarVelocidad()
                velocidad_temp = []
                solucion_mejor = copy.copy(self.mejor.getMejor())
                solucion_mejor_ = particula.getMejor()[:]
                solucion_particula = particula.getActualSolucion()[:]

                for i in range(len(self.grafo.vertices)):
                    if solucion_particula[i] != solucion_mejor:
                        cambiar = (i, solucion_mejor_.index(solucion_particula[i]), self.alpha)
                        velocidad_temp.append((cambiar))
                        aux = solucion_mejor_[cambiar[0]]
                        solucion_mejor_[cambiar[0]] = solucion_mejor_[cambiar[1]]
                        solucion_mejor_[cambiar[1]] = aux

                for i in range(len(self.grafo.vertices)):
                    if solucion_particula[i] != solucion_mejor:
                        cambiar = (i, solucion_mejor.index(solucion_particula[i]), self.alpha)
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
                costeSolucionActual = self.grafo.costeGrafo(solucion_particula)
                particula.setActualCoste(costeSolucionActual)

                if costeSolucionActual < particula.getMejorCoste():
                    particula.setMejor(solucion_particula)
                    particula.setMejorCoste(costeSolucionActual)

def cargarMapa():
    f = open("distances")
    info = []
    num_lineas = 0
    try:
        for linea in f:
            palabras = linea.split(' ')
            info.append((float(palabras[0]), float(palabras[1])))
            num_lineas += 1

            print (num_lineas)
    finally:
        f.close()

    return info

if __name__ == "__main__":
    grafo = cargarMapa()

    pso = AlgoritmoPSO (grafo, max_iteraciones=100, N=10, beta=1, alpha=0.9)
    pso.run()
    print('Solucion: %s | Coste: %d\n' % (pso.getMejor().getMejor(), pso.getMejor().getMejorCoste()))




