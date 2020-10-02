# %% codecell
from sympy import sin, cos, Matrix
from sympy.abc import rho, phi
X = Matrix([rho*cos(phi), rho*sin(phi), rho**2])
Y = Matrix([rho, phi])

X
# %% codecell
Y

# %% codecell
X.jacobian(Y)

# %% codecell
from sympy import MatrixSymbol, Matrix
from sympy.core.function import Function
from sympy import FunctionMatrix, Lambda

n, m, p = 3, 3, 2

X = MatrixSymbol('X', n, m)
W = MatrixSymbol('W', m, p)

(X.T*X).I*W


# %% codecell
Matrix(X)
# %% codecell
Matrix(X * W)




# %% codecell
from sympy import I, Matrix, symbols
from sympy.physics.quantum import TensorProduct

m1 = Matrix([[1,2],[3,4]])
m2 = Matrix([[1,0],[0,1]])

m1
# %% codecell
TensorProduct(m1, m2)



# %% codecell
f = Function('f')
F = FunctionMatrix(3,4, f)
Matrix(F)


# %% codecell
y = Function('y')(X)
y
# %% codecell
# y.diff(X)
from sympy.abc import x,y,z,t,e,r,a,b,c
from sympy import derive_by_array
from sympy import sin, exp, cos

#basis = Matrix([x, y, z])
Matrix(X)

m = Matrix([[exp(x), sin(y*z), t*cos(x*y)], [x, x*y, t], [x,x,z] ])
basis = Matrix([[x,y,z], [x,y,z], [x,y,z]])
type(basis)
X.as_explicit()
M = Matrix([[x,y,z], [t,e,r], [a,b,c]])
ax = derive_by_array(m, M)
ax



# %% codecell
Matrix(X)[1,2]
x_12 = Matrix(X)[1,2]
type(Matrix(X)[1,2])
f = Function('f')
g = Function('g')
h = f(g(x_12))
h
h.diff(x_12)

# %% codecell




# %% codecell
from sympy import Symbol
from sympy.abc import i, j

f = Function('f')

#def makeF(i, j):
#     x_ij = Symbol('x_{}{}'.format(i,j), is_commutative=True)
#     return f(x_ij)


def makeX(i, j):
     x_ij = Symbol('x_{}{}'.format(i, j), is_commutative=True)
     return x_ij #Lambda((i,j), x_ij)


# NOTE: even if i, j are sympy Symbols, passing them here with python's lambda instead of sympy's Lambda lets the indices actually be seen!!!
X = Matrix(2, 3, lambda i,j: makeX(i+1, j+1)); X
# BAD
#X = FunctionMatrix(2,3, Lambda((a,b), makeX(int(a), int(b))))
# %% codecell
X[0,0]

# %% codecell
from sympy import derive_by_array

derive_by_array(Matrix(X), Matrix(X))
# %% codecell

from sympy import Symbol
x_11 = Symbol('x_11', is_commutative=True)
x_12 = Symbol('x_12', is_commutative=True)
x_13 = Symbol('x_13', is_commutative=True)
x_21 = Symbol('x_21', is_commutative=True)
x_22 = Symbol('x_22', is_commutative=True)
x_23 = Symbol('x_23', is_commutative=True)
x_31 = Symbol('x_31', is_commutative=True)
x_32 = Symbol('x_32', is_commutative=True)
x_33 = Symbol('x_33', is_commutative=True)
X = Matrix([[x_11,x_12, x_13], [x_21,x_22,x_23], [x_31,x_32,x_33]]); X

w_11 = Symbol('w_11', is_commutative=True)
w_12 = Symbol('w_12', is_commutative=True)
w_21 = Symbol('w_21', is_commutative=True)
w_22 = Symbol('w_22', is_commutative=True)
w_31 = Symbol('w_31', is_commutative=True)
w_32 = Symbol('w_32', is_commutative=True)
W = Matrix([[w_11, w_12], [w_21, w_22], [w_31,w_32]]); W


y_11 = Function('y_11')
y_12 = Function('y_12')
y_21 = Function('y_21')
y_22 = Function('y_22')
Y = Matrix([[y_11(X),y_12(X)],[y_21(X),y_22(X)]])
Y

#Y.diff(X)

#y = Function('y')

# %% codecell
#derive_by_array(Y, X)

# %% codecell
A = Matrix(MatrixSymbol('x', 3,3)); A
B = Matrix(MatrixSymbol('w', 3,2)); B
# %% codecell
A*B

derive_by_array(A*B, A)
# %% codecell
(A*B).diff(A)

assert (A*B).diff(A) == derive_by_array(A*B, A)

# %% codecell
X*W
# %% codecell
derive_by_array(X*W, X)
# %% codecell
(X*W).diff(X)


# %% codecell
### JACOBIAN:
def makeX(i, j):
     x_ij = Symbol('x_{}{}'.format(i,j), is_commutative=True)
     return x_ij #Lambda((i,j), x_ij)

#u = lambda i,j : makeX(i,j)
#FunctionMatrix(9,1, Lambda((i,j), makeX(i,j)))

def makeYofX(i, j):
     yx_ij = Symbol('y_{}{}'.format(i,j), is_commutative=True)
     return yx_ij #Lambda((i,j), x_ij)



# %% codecell
def var(letter: str, i: int, j: int) -> Symbol:
     letter_ij = Symbol('{}_{}{}'.format(letter, i+1, j+1), is_commutative=True)
     return letter_ij


n,m,p = 3,3,2
# NOTE: even if i, j are sympy Symbols, passing them here with python's lambda instead of sympy's Lambda lets the indices actually be seen!!!
X = Matrix(n,m, lambda i,j: var('x', i,j)); X
# %% codecell
W = Matrix(m,p, lambda i,j: var('w', i, j)); W


# %% codecell
#res = y.subs({y[0]:x[0]**2* x[2] +x[1]}); res
# %% codecell
#res.subs({x[0]: 23, x[1]: 14})
# %% codecell
#derive_by_array(res[0], x[0])
#derive_by_array(res[1], x[0])



# %% codecell
#derive_by_array(y, x)

# %% codecell
#y.diff(x)
#y.jacobian(x)

# %% codecell
from sympy import Function, hessian, pprint
from sympy.abc import x, y
f = Function('f')(x, y)
g1 = Function('g')(x, y)
g2 = x**2 + 3*y
hessian(f, (x,y),[g1,g2])
# %% codecell
#Matrix(FunctionMatrix(n, 1, Lambda((i,j), Function("y_{}{}".format(i,j)))))
rho = Matrix([[Symbol("r_{}{}".format(i+1,j+1)) for j in range(5)] for i in range(5)])
rho

# %% codecell
derive_by_array(rho, rho[2,1])
# %% codecell
derive_by_array(rho[2,1], rho)
# %% codecell
rho.diff(rho[2,1])

# %% codecell
from sympy.abc import x
from sympy.utilities.lambdify import lambdify, implemented_function
from sympy import Function

f = implemented_function('f', lambda x: x)
lam_f = lambdify(x, f(x))

lam_f(4)
