import pants
import math
import random

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

def euclidean(a, b):
    return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))

nodes = cargarMapa()

world = pants.World(nodes, euclidean)
solver = pants.Solver()
solution = solver.solve(world)

print(solution.distance)
print(solution.tour)    # Nodes visited in order
print(solution.path)    # Edges taken in order



