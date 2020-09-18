# %% codecell
from sympy import Matrix, Symbol, derive_by_array, Lambda, Function, MatrixSymbol, Derivative
from sympy import var
from sympy.abc import x, i, j, a, b



# %% markdown
# Defining myvariable-element matrices $X \in \mathbb{R}^{n \times m}$ and $W \in \mathbb{R}^{m \times p}$:
# %% codecell
def myvar(letter: str, i: int, j: int) -> Symbol:
    letter_ij = Symbol('{}_{}{}'.format(letter, i+1, j+1), is_commutative=True)
    return letter_ij


n,m,p = 3,3,2

X = Matrix(n, m, lambda i,j : myvar('x', i, j)); X
# %% codecell
W = Matrix(m, p, lambda i,j : myvar('w', i, j)); W
# %% codecell
A = MatrixSymbol('X',3,3); Matrix(A)
B = MatrixSymbol('W',3,2)






# %% markdown
# Defining $N = \nu(X, W) = X \times W$
#
# * $\nu : \mathbb{R}^{(n \times m) \times (m \times p)} \rightarrow \mathbb{R}^{n \times p}$
# * $N \in \mathbb{R}^{n \times p}$
# %% codecell
v = lambda a,b: a*b

vL = Lambda((a,b), a*b)

n = Function('v') #, Lambda((a,b), a*b))

vN = lambda mat1, mat2: Matrix(mat1.shape[0], mat2.shape[1], lambda i, j: Symbol("n_{}{}".format(i+1, j+1))); vN


Nelem = vN(X, W)
Nelem

# %% codecell
Nspec = v(X,W)
Nspec
# %% codecell
#N = v(X, W); N
N = n(A,B)
N









# %% markdown
#
# Defining $S = \sigma_{\text{apply}}(N) = \sigma_{\text{apply}}(\nu(X,W)) = \sigma_\text{apply}(X \times W) = \Big \{ \sigma(XW_{ij}) \Big\}$.
#

# Assume that $\sigma_{\text{apply}} : \mathbb{R}^{n \times p} \rightarrow \mathbb{R}^{n \times p}$ while $\sigma : \mathbb{R} \rightarrow \mathbb{R}$, so the function $\sigma_{\text{apply}}$ takes in a matrix and returns a matrix while the simple $\sigma$ acts on the individual elements $N_{ij} = XW_{ij}$ in the matrix argument $N$ of $\sigma_{\text{apply}}$.
#
# * $\sigma : \mathbb{R} \rightarrow \mathbb{R}$
# * $\sigma_\text{apply} : \mathbb{R}^{n \times p} \rightarrow \mathbb{R}^{n \times p}$
# * $S \in \mathbb{R}^{n \times p}$

# %% codecell
# way 2 of declaring S (better way)
sigma = Function('sigma')

sigmaApply = Function("sigma_{apply}") #lambda matrix:  matrix.applyfunc(sigma)

sigmaApply_ = lambda matrix: matrix.applyfunc(sigma)

S = sigmaApply(N); S

# %% codecell
Sspec = S.subs({A:X, B:W}).replace(n, v).replace(sigmaApply, sigmaApply_)
Sspec
# %% codecell
Selem = S.replace(n, vN).replace(sigmaApply, sigmaApply_)
Selem


# %% codecell
import itertools

elemToSpec = dict(itertools.chain(*[[(Nelem[i, j], Nspec[i, j]) for i in range(3)] for j in range(2)]))
Matrix(list(elemToSpec.items()))
# %% codecell
elemToSpecFunc = dict(itertools.chain(*[[(Nelem[i, j], Function("n_{}{}".format(i + 1, j + 1))(Nspec[i, j])) for i in range(3)] for j in range(2)]))

Matrix(list(elemToSpecFunc.items()))

# %% codecell
Selem.subs(elemToSpec)
# %% codecell
Selem[0,1].diff(Nelem[0,1])
# %% codecell
Selem[0,1].diff(Nelem[0,1]).subs(elemToSpec[1])
# %% codecell
Selem[0,1].diff(Nelem[0,1]).subs(elemToSpec[1]).subs({Nspec[0,1] : 23})
# %% codecell
Selem[0,1].diff(Nelem[0,1]).subs(elemToSpec[1]}).replace(sigma, lambda x: 8*x**3)
# %% codecell
Selem[0,1].diff(Nelem[0,1]).replace(sigma, lambda x: 8*x**3)
# %% codecell
Selem[0,1].diff(Nelem[0,1]).replace(sigma, lambda x: 8*x**3).doit()
# %% codecell
# ### GOT IT: can replace now with expression and do derivative with respect to that expression.
Selem[0,1].diff(Nelem[0,1]).subs(elemToSpec[1]).replace(sigma, lambda x: 8*x**3).doit()

# %% codecell
Selem

# %% codecell
nt = Nelem.subs(elemToSpecFunc); nt
# %% codecell
st = Selem.subs(elemToSpecFunc); st
# %% codecell
st.diff(nt)
# %% codecell
st[0,0].diff(st[0,0].args[0])
# %% codecell
st[0,0].diff(X[0,0])
# %% codecell
st[0,0].diff(st[1,0].args[0])
# %% codecell
Selem.diff(Nelem)
# %% codecell
Selem.diff(Nelem).subs(elemToSpecFunc)

# %% codecell
# CAN even replace elements after have done an operation on them!!! replacing n_21 * 2 with the number 4.
Sspec.subs({Nspec[0, 0]: 3}).replace(sigma, lambda x: 2 * x).replace(Nspec[2, 1] * 2, 4)









# %% codecell
lambd = Function("lambda")
lambd_ = lambda matrix : sum(matrix)


vN(X, W)
# %% codecell
vN(A, B)
# %% codecell
L = lambd(S); L
# %% codecell
Nelem
# %% codecell
L.replace(n, vN)
# %% codecell
L.replace(n, vN).replace(sigmaApply, sigmaApply_)
# %% codecell
L.replace(n, v)
# %% codecell

L.replace(n, v).replace(sigmaApply, sigmaApply_)

# %% codecell
L.subs({A:X, B:W}).replace(n, vL).replace(sigmaApply, sigmaApply_)
# %% codecell
L.subs({n: v, A:X, B:W}).replace(sigmaApply, sigmaApply_).subs({Nspec[0, 1]: 34})

# %% codecell
L.subs({n: v, A:X, B:W}).replace(sigmaApply, sigmaApply_).replace(lambd, lambd_)







# %% codecell
from sympy import symbols, Derivative

x, y, r, t = symbols('x y r t') # r (radius), t (angle theta)
f, g, h = symbols('f g h', cls=Function)
h = g(f(x))
Derivative(h, f(x)).doit()


# %% codecell

# %% codecell
# ### WAY 1: of substituting to differentiate with respect to expression:
n_ij = Function('n_ij')
n_ij(A,B) # (N[0,0]); n_ij

# %% codecell
n_ij(A,B).args

# %% codecell
# sigma(n_ij).diff(n_ij).replace(n_ij, N[0,0]) # ERROR cannot deriv wi.r.t to the expression w11*x11 + ...

sigma(n_ij(A,B)).diff(n_ij(A,B))
# %% codecell
sigma(n_ij(*X,*W)).diff(X[0,0])
# %% codecell
nab_ij = n_ij(A,B)
sigma(nab_ij).diff(nab_ij)#.subs({nab_ij : Nspec[0, 0]})
# %% codecell
sigma(nab_ij).diff(nab_ij).subs({nab_ij : Nspec[2, 1]})

# %% codecell
sigma(nab_ij).diff(nab_ij).subs({nab_ij : Nspec[2,1]}).subs({X[2,1]:77777})
# %% codecell
sigma(nab_ij).diff(nab_ij).subs({nab_ij : 23}) # ERROR if using replace() since it says can't calc derivs w.r.t to the x_11*w_11 + ...

# %% codecell
sigma(nab_ij).diff(nab_ij).subs({nab_ij : Nspec[2,1]}).doit()
# %% codecell
sigma(nab_ij).subs({nab_ij : Nspec[2,1]})#.diff(X[2,1])
# %% codecell
# Substituting the value of the function n_ij first, and THEN differentiating with respect to something in that substitution. (X_21)
sigma(nab_ij).subs({nab_ij : Nspec[2,1]}).diff(X[2,1])


# %% codecell
Selem[2,1].subs({Nelem[2,1] : Nspec[2,1]}).diff(X[2,1])




# %% codecell
# ### WAY 2:
n_11 = Function('n_11')(Nspec[0, 0]); n_11

# %% codecell
sigma(n_11)
# %% codecell
assert Nspec[0,0] == n_11.args[0]

sigma(n_11).subs({n_11 : n_11.args[0]})
# %% codecell
sigma(n_11).diff(n_11) #.replace(n_ij, n_ij.args[0])
# %% codecell
sigma(n_11).diff(n_11).subs({n_11 : n_11.args[0]}).subs({X[0,0]:77777})
# %% codecell
sigma(n_11).diff(n_11).subs({n_11 : n_11.args[0]}).replace(n_11.args[0], 23) # same as subs in this case

# %% codecell
sigma(n_11).diff(X[0,0])
# %% codecell
id = Lambda(x, x)

sigma(n_11).diff(X[0,0]).subs({n_11 : id})

# %% codecell
# NOTE: so I don't think WAY 2 is correct because here it doesn't simplify the derivative d n11 / d eps11, since this should equal 1 because now n11 = eps11. Correct one is below (repeated from above)
sigma(n_11).diff(X[0,0]).subs({n_11 : Nspec[0,0]})
# %% codecell
# CORRECT WAY 1
sigma(n_11).subs({n_11 : Nspec[0,0]}).diff(X[0,0])
# %% codecell
# CORRECT WAY 2

sigma(nab_ij).subs({nab_ij : Nspec[0,0]}).diff(X[0,0])
# %% codecell
# CORRECT WAY 3
Selem[2,1].subs({Nelem[2,1] : Nspec[2,1]}).diff(X[2,1])

# %%codecell
sigma(n_11) # WAY 1: sigma argument is already hardcoded
# %%codecell
sigma(nab_ij) # Way 2: sigma argument is function of matrixsymbol (better than 1)
# %% codecell
Selem[2,1] # WAY 3: sigma argument is just symbol and we replace it as function with argument hardcoded only later. (better than 2)




# %% codecell
L

# %% codecell
assert Selem == S.replace(n, vN).replace(sigmaApply, sigmaApply_)

Selem

# %% codecell
L.replace(n, vN).replace(sigmaApply, sigmaApply_)
# %% codecell
#L.replace(n, vN).replace(sigmaApply, sigmaApply_).diff(Nelem[0,0])

# %% codecell
Lsum = L.replace(n, vN).replace(sigmaApply, sigmaApply_).replace(lambd, lambd_)
Lsum
# %% codecell
Lsum.diff(Nelem)
# %% codecell
Lsum.subs(elemToSpec)#.diff(X[2,1])
# %% codecell
Lsum.subs(elemToSpec).diff(X)
# %% codecell

specToElem = {v : k for k, v in elemToSpec.items()}

Lsum.subs(elemToSpec).diff(X).subs(specToElem)
