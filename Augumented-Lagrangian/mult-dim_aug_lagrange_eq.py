# The code implements the augumented lagrangian method for solving the following problem:
# given:
# f: Rn -> R
# h: Rn -> R
# g: Rn -> R
# find the minimizer of f satisfying h(x) = 0, g(x) <= 0
# Note that the domain is many-dimensional, however h and g are just scalar functions,
# that is, we do not have the functionality to allow for more constraints.
# The algorithm include some parameters that have arbitrary starting values, for example the
# penalty and the multipliers.

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

# defining the function and the constraint function. f(x), h(x) = 0, g(x) <= 0

domain_dim = 2 # The dimension of the domain space
def f(x):
    return (x[0]-6)**2 + x[1]**2 # function from page 32 of Brigin and Martinez (BM)

def h(x):
    return (x[1]-(x[0]/4)**2)**2 + (x[0]/4 - 1)**2 - 1 # p32 BM

def g(x):
    return 0 # setting to zero as p32 BM does not make use of it

# defining the penalty-multiplier functions -
# one penalty function for the equality contraint, one for the inequality const.
lambd = 1
min_lambd = 0
max_lambd = 1000
mu = 1
max_mu = 1000
penalt = 1
max_penalt = 1000
gamma = 2 # how the penalty increases on each iteration

# the penalty-multiplier function for the equality constraint h
def pmF_eq(p, l, x):
    return (p/2)*((h(x)+l/p)**2)

# the penalty-multiplier function for the inequality constraint g
def pmF_ineq(p, m, x):
    temp = g(x) + m/p
    if(temp < 0): return 0
    else: return (p/2)*temp**2

# defining the augumented lagrangian
def AugLag(x):
    return f(x) + pmF_eq(penalt, lambd, x) + pmF_ineq(penalt, mu, x)

# running the algorithm (4.1 on page 33 in BM)
iterations = 6 # how many times we will run the loop
x_appr = np.array([0, 0]) #initial guess
record = np.empty(shape=(iterations, domain_dim)) # a table that stores the approximate solution after each iteration
for i in range(0, iterations):
    # STEP 1 - find the approximate minimizer for the lagrangian
    x_appr = optimize.minimize(AugLag, x_appr).x
    record[i] = x_appr
    # STEPS 2,3 - update the multipliers 
    lambd = min(lambd + penalt*h(x_appr), max_lambd); lambd = max(lambd, min_lambd)
    mu = min(max_mu, max(0, mu + penalt*g(x_appr)))
    if (penalt <= max_penalt): penalt = min(penalt*gamma, max_penalt)

print(record) # for the problem on p32 BM the last element in the table should be close to (5.3541,0.8507)
