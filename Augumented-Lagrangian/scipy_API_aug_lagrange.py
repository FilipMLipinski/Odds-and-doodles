import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def mainFunc(fun, x0, args=(), jac = None, constraints=(), tol = None):


	# each constraint is a dictionary with the values
	#   type : str [eq, or ineq]
	#	fun : callable

	# assuming we get only one nonlinear equality constraint.
	constrFuncH = [c for c in constraints if c['type'] == 'eq']
	constrFuncG = [c for c in constraints if c['type'] == 'ineq']

	# defining the penalty-multiplier function
	lambd = np.full(len(constrFuncH), 1.0) 
	min_lambd = 0
	max_lambd = 1000
	penalt = 1
	max_penalt = 1000
	gamma = 2 # how the penalty increases on each iteration

	def pmF_eq(p, l, x):
		temp_sum = 0
		for i in range(0, len(constrFuncH)):
			temp_sum += (constrFuncH[i]['fun'](x) + l[i]/p)**2
		return (p/2)*temp_sum

    # defining the augumented lagrangian
	def AugLag(x):
	    return fun(x) + pmF_eq(penalt, lambd, x)

	# running the algorithm (4.1 on page 33 in BM)
	x_appr = x0 #initial guess
	closeEnough = False
	while(not closeEnough):
	    # STEP 1 - find the approximate minimizer for the lagrangian
	    x_appr = optimize.minimize(AugLag, x_appr).x

	    # STEPS 2,3 - update the multipliers and penalty
	    for i in range(0, len(constrFuncH)):
	    	lambd[i] = max(min(lambd[i] + penalt*constrFuncH[i]['fun'](x_appr), max_lambd), min_lambd)

	    if (penalt <= max_penalt): penalt = min(penalt*gamma, max_penalt)

	    closeEnough = (penalt==max_penalt)
	return x_appr

def f(x):
    return (x[0]-6)**2 + x[1]**2 # function from page 32 of Brigin and Martinez (BM)
def h(x):
    return (x[1]-(x[0]/4)**2)**2 + (x[0]/4 - 1)**2 - 1 # p32 BM
def h1(x):
	return x[1]

constrainth = {'fun' : h, 'type' : 'eq'}
constrainth1 = {'fun' : h1, 'type' : 'eq'}

print(mainFunc(fun=f, x0=[0,0], constraints=[constrainth, constrainth1]))

