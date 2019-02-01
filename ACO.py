import acopy
import tsplib95

a=20
coste = []
it_alpha = []

#for i in range (30):
#    it_alpha.append(a)

solver = acopy.Solver(rho=0.55, q=0.7)
colony = acopy.Colony(alpha=0.7, beta=4)
threshold = acopy.plugins.Threshold(threshold=95345)

problem = tsplib95.load_problem('C://Users//Vicente//PycharmProjects//TSPproblem//venv//datasetcorto')
G = problem.get_graph()
tour = solver.solve(G, colony, limit=90)

#    a = a + 10

print (tour.cost)
print (tour.nodes)
#coste.append(tour.cost)

'''import matplotlib.pyplot as plt

plt.plot(it_alpha, coste)
plt.show()'''

