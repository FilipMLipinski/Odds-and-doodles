# I made this to understand pyplot better and also 
# visualise the lagrangian multiplier method.
# This code finds the minimum of a two-dimensional quadratic
# function, which is vectorized (although the values used to plot the graph are not vectorized),
# subject to a condition of the form h(x) = x^T . d = 0.
# Solution is not numerical - the lagrange multiplier method allows for a
# purely algebraic solution. But this helped me a lot in understanding constraints,
# lagrange multipliers, gradients of functions - all the basics.

import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from scipy import linalg

# minimizing f(x) = x^T . A . x + x^T . b + c, when x is a 2-dimensional vector.
# requiring non-zero matrix rows

# defining the cost function and the parameters
A = np.array([[3, 2], [2, 4]])
b = np.array([2,4])
c = -300

def genQuad(x):
    return np.dot(np.transpose(x), np.dot(A, x)) + np.dot(np.transpose(x), b) + c

# raising an error if some row in A is all-zero
nonzeroRows = True
for row in A:
    if (row[0] == 0 and row[1] == 0):
        raise NameError('The A matrix cannot have any all-zero rows')

# defining the constraint function and the parameters, d2 must be non-zero
# the constrain is as follows: h(x) = x^T . d = 0
d = np.array([1,1])
if(d[1]==0):
    raise NameError('d2 cannot be 0')

def eqConstr(x):
    return np.dot(np.transpose(x), d)

# checking whether the minimum exists
H = np.transpose(A) + A
eigens = np.real(linalg.eigvals(H))
minimumexists = True
for a in eigens:
    if (a < 0):
        minimumexists = False
print("does minimum exist: " + str(minimumexists))

# finding the minimum, lagrange multiplier method
# NOT A NUMERICAL SOLUTION, JUST ALGEBRA
if(minimumexists):
    i,j,k,l = A[0][0],A[0][1],A[1][0],A[1][1]
    b1,b2,d1,d2 = b[0],b[1],d[0],d[1]
    M = np.array([[2*i,j+k,d1],[j+k, 2*l,d2],[d1,d2,0]])
    xstar = linalg.solve(M, np.array([-1*b1,-1*b2,0]))
    print('minimum equals: [' + str(xstar[0]) + ", " + str(xstar[1]) + "]")

# plotting the function
fig = plt.figure()
ax = plt.axes(projection='3d')

rangeOfValues = 1
numOfValues = 21
x1 = np.linspace(-1*rangeOfValues,rangeOfValues,numOfValues)
x2 = np.linspace(-1*rangeOfValues,rangeOfValues,numOfValues)
X1, X2 = np.meshgrid(x1,x2)

# computing the Y values using a nested for loop - not the best idea
# but I have not found a good numpy function for this...
Y = np.empty(shape=(numOfValues,numOfValues))
for i in range(0,numOfValues):
    for j in range(0,numOfValues):
        Y[i][j] = genQuad([X1[i][j],X2[i][j]])

ax.contour3D(X1, X2, Y, 100, cmap='binary')
if(minimumexists):
    ax.scatter(xstar[0],xstar[1],genQuad(np.array([xstar[0],xstar[1]])))
ax.plot(x1,-1*d1*x1/d2,genQuad(np.array([xstar[0],xstar[1]])))
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('y')
plt.show()
