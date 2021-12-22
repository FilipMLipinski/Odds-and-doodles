import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def mainFunc(fun, x0, args=(), jac = None, constraints=(), tol = None):

	# wrapper is used to call fun together with the given args.
	def wrapper(x):
		if(args):
			return fun(x, *args)
		else: return fun(x)

	# each constraint is a dictionary with the values
	#   type : str [eq, or ineq]
	#	fun : callable

	constrFuncH = [c for c in constraints if c['type'] == 'eq']
	constrFuncG = [c for c in constraints if c['type'] == 'ineq']

	# defining the penalty-multiplier function
	lambd = np.full(len(constrFuncH), 1.0) # each equality constraint gets a different multiplier
	mu = np.full(len(constrFuncG), 1.0) # ... and each inequality constraint gets a different multiplier
	min_lambd = 0
	max_lambd = 1000
	max_mu = 1000
	penalt = 1
	max_penalt = 1000
	gamma = 2 # how the penalty increases on each iteration
	defTol = 0.00001 # default tolerance, in case tol=None
	tolerance = defTol if (tol is None) else tol

	def pmF_eq(p, l, x):
		temp_sum = 0
		for i in range(0, len(constrFuncH)):
			temp_sum += (constrFuncH[i]['fun'](x) + l[i]/p)**2
		return (p/2)*temp_sum

	def pmF_ineq(p, m, x):
		temp_sum = 0
		for i in range(0, len(constrFuncG)):
			temp_sum += max(0, (constrFuncG[i]['fun'](x) + m[i]/p))**2
		return (p/2)*temp_sum

    # defining the augumented lagrangian
	def AugLag(x):
	    return wrapper(x) + pmF_eq(penalt, lambd, x) + pmF_ineq(penalt, mu, x)

	# running the algorithm (4.1 on page 33 in BM)
	x_appr = x0 #initial guess
	closeEnough = False
	while(not closeEnough):
		# calculating the previous value to see if enough progress has been made
		prev = wrapper(x_appr) 

		# STEP 1 - find the approximate minimizer for the lagrangian
		x_appr = optimize.minimize(AugLag, x_appr).x

		# STEPS 2,3 - update the multipliers and penalty
		for i in range(0, len(constrFuncH)):
			lambd[i] = max(min(lambd[i] + penalt*constrFuncH[i]['fun'](x_appr), max_lambd), min_lambd)
		for i in range(0, len(constrFuncG)):
			mu[i] = max(min(mu[i] + penalt*constrFuncG[i]['fun'](x_appr), max_mu), 0)
		if (penalt <= max_penalt): penalt = min(penalt*gamma, max_penalt)

		# break if progress is below the tolerance
		closeEnough = (abs(prev - wrapper(x_appr)) <= tolerance)

	return x_appr

def f(x, a):
    return (x[0]-6)**2 + x[1]**2 + a # function from page 32 of Brigin and Martinez (BM). With the additional argument 'a' that doesn't do anything if set to 0.
def h(x):
    return (x[1]-(x[0]/4)**2)**2 + (x[0]/4 - 1)**2 - 1 # p32 BM
def h1(x):
	return 0
def g(x):
	return (x[1]-(x[0]/4)**2)**2 + (x[0]/4 - 1)**2 - 1 + 0.0001# a little offset from h(x) to see how the result is influenced.

constrainth = {'fun' : h, 'type' : 'eq'}
constrainth1 = {'fun' : h1, 'type' : 'eq'}
constraintg = {'fun' : g, 'type' : 'ineq'}

print(mainFunc(fun=f, x0=[0,0], constraints=[constrainth, constrainth1, constraintg], args=[0]))

