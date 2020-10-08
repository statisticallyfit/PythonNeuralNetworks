# %% markdown
# # Derivations For Matrix Derivative Rule of $L = \lambda( \sigma_{\text{apply}}( \nu(X, W) ) )$


# %% codecell
from sympy import Matrix, Symbol, derive_by_array, Lambda, Function, MatrixSymbol, Derivative, symbols, diff
from sympy.abc import x, i, j, a, b

# NOTE no need to call display manually anymore! Just import display from ipython and manually init printing for sympy and then we can render equations nicely in python interactive window!
# SOURCE = https://hyp.is/Czfddgk8EeuVNlfac98M0w/confluence.jetbrains.com/display/PYH/Using+IPython+Notebook+with+PyCharm
from IPython.display import display 
from sympy.interactive import printing
printing.init_printing(use_latex='mathjax')

import itertools 

from functools import reduce

# %% codecell
def composeTwoFunctions(f, g):
    return lambda *a, **kw: f(g(*a, **kw))

def compose(*fs):
    return reduce(composeTwoFunctions, fs)


def var_i(letter: str, i: int) -> Symbol:
    letter_i = Symbol('{}_{}'.format(letter, i), is_commutative=True)
    return letter_i


def var_ij(letter: str, i: int, j: int) -> Symbol:
    letter_ij = Symbol('{}_{}{}'.format(letter, i+1, j+1), is_commutative=True)
    return letter_ij


def func(fLetter: str, i: int, xLetter, xLen):
    xs = [var_i(xLetter, i+1) for i in range(xLen)]
    func_i = Function('{}_{}'.format(fLetter, i + 1))(*xs)
    return func_i

# %% codecell
n,m,p = 3,3,2

X = Matrix(n, m, lambda i,j : var_ij('x', i, j)); X
# %%
W = Matrix(m, p, lambda i,j : var_ij('w', i, j)); W
# %%
A = MatrixSymbol('X',n,m)
B = MatrixSymbol('W',m,p)
# %%
Matrix(A)
# %%
# matrix variable for sympy Lambda function arguments
M = MatrixSymbol('M', i, j)# abstract shape
N = MatrixSymbol("N", n, p)# shape of A*B

# %%
Matrix(A)

xi  = Symbol('xi')
xi_1  = Symbol('xi_1')


# %% codecell
v = Function("nu",applyfunc=True)
v_ = lambda a,b: a*b
vL = Lambda((a,b), a*b)
vN = lambda mat1, mat2: Matrix(mat1.shape[0], mat2.shape[1], lambda i, j: Symbol("n_{}{}".format(i+1, j+1))); vN

Nelem = vN(X, W)
Nspec = v_(X,W)
N = v(A,B)

display(Nelem)
display(Nspec)
display(N)

# %%
sigma = Function('sigma')
sigmaApply = Function("sigma_apply") #lambda matrix:  matrix.applyfunc(sigma)
sigmaApply_ = lambda matrix: matrix.applyfunc(sigma)
sigmaApply_L = Lambda(M, M.applyfunc(sigma))


S = sigmaApply(N)
display(S)

Sspec = S.subs({A:X, B:W}).replace(v, v_).replace(sigmaApply, sigmaApply_)
#Selem.subs(elemToSpecD)
display(Sspec)

Selem = S.replace(v, vN).replace(sigmaApply, sigmaApply_)
display(Selem)


# %%
lambd = Function("lambda")
lambd_ = lambda matrix : sum(matrix)
#lambda_L = Lambda(M, sum(M))

ABres = MatrixSymbol("R", A.shape[0], B.shape[1])
lambd_L = Lambda(ABres, sum(ABres))

#L = lambd(sigmaApply(v(A,B)))
L = compose(lambd, sigmaApply, v)(A, B)
display(L)



# %% codecell
elemToSpecD = dict(itertools.chain(*[[(Nelem[i, j], Nspec[i, j]) for j in range(p)] for i in range(n)]))
elemToSpec = list(elemToSpecD.items())

specToElemD = {val:key for key, val in elemToSpecD.items()}
specToElem = list(specToElemD.items())

display(Matrix(elemToSpec))

# %% codecell

elemToSpecFuncD = dict(itertools.chain(*[[(Nelem[i, j], Function("n_{}{}".format(i + 1, j + 1))(Nspec[i, j])) for j in range(p)] for i in range(n)]))

elemToSpecFunc = list(elemToSpecFuncD.items())

specFuncToElemD = {val : key for key , val in elemToSpecFuncD.items()}
specFuncToElem = list(specFuncToElemD.items())

display(Matrix(elemToSpecFunc))



# %% codecell
elemToNFuncD = dict(itertools.chain(*[[(Nelem[i, j], Function("n_{}{}".format(i + 1, j + 1))(*X,*W)) for j in range(p)] for i in range(n)]))

elemToNFunc = list(elemToNFuncD.items())

nfuncToElemD = {val: key for key, val in elemToNFuncD.items()}
nfuncToElem = list(nfuncToElemD.items())

display(Matrix(elemToNFunc))



# %% codecell
elemToNmatfuncD = dict(itertools.chain(*[[(Nelem[i, j], Function("n_{}{}".format(i+1,j+1))(A,B) ) for j in range(p)] for i in range(n)]))

elemToNmatfunc = list(elemToNmatfuncD.items())

nmatfuncToElemD = {val: key for key, val in elemToNmatfuncD.items()}
nmatfuncToElem = list(nmatfuncToElemD.items())

display(Matrix(elemToNmatfunc))



# %% codecell
nmatfuncToSpecD = dict(zip(elemToNmatfuncD.values(), elemToSpecD.values()))

nmatfuncToSpec = list(nmatfuncToSpecD.items())

display(Matrix(nmatfuncToSpec))





# %% codecell
#L.replace(v,v_).replace(sigmaApply, sigmaApply_).diff(B)

dL_dW_abstract = L.replace(v,v_).replace(sigmaApply, sigmaApply_).diff(B)

dL_dW_abstract
# %%
display(dL_dW_abstract)

display( dL_dW_abstract.subs({lambd : lambd_L}) )
# %%
dL_dX_abstract = L.replace(v, v_).replace(sigmaApply, sigmaApply_).diff(A)

display(dL_dX_abstract)




# %% codecell
dL_dW_direct = L.replace(v, vN).replace(sigmaApply, sigmaApply_).replace(lambd, lambd_).subs(elemToSpecD).diff(W).subs(specToElemD)

display(dL_dW_direct)

dL_dX_direct = L.replace(v, vN).replace(sigmaApply, sigmaApply_).replace(lambd, lambd_).subs(elemToSpecD).diff(X).subs(specToElemD)

display(dL_dX_direct)

# %% codecell
dN_dW_times_dS_dN = compose(sigmaApply, v)(A,B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(B).subs({A*B : vN(A,B)}).doit()

display(dN_dW_times_dS_dN)

display(dN_dW_times_dS_dN.subs({A:X})) # replace won't work here

# Carrying out the multplication: 
display(dN_dW_times_dS_dN.subs({A:X}).doit()) # replace won't work here



# %%
unapplied = sigmaApply_L(vN(A,B))
# Also works: same as above: 
#compose(sigmaApply, v)(A,B).replace(v, vN).replace(sigmaApply , sigmaApply_L)
applied = unapplied.doit()


display(unapplied)
display(applied)




# %%
dL_dW_step = compose(lambd, sigmaApply, v)(A,B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(B).subs({A*B : vN(A,B)}).doit()

display(dL_dW_step)
display(dL_dW_step.replace(unapplied, applied))
#display(dL_dW_step.subs({A:X})) # replace won't work here

# Carrying out the multplication: 
display(dL_dW_step.subs({A:X}).doit()) # replace won't work here
display(dL_dW_step.subs({A:X}).doit().replace(unapplied, applied))

# %%
dle = lambd(xi).diff(xi)
#display(dle)

dle_repl = lambd(xi).diff(xi).subs(xi, applied).replace(lambd, lambd_L)
#display(dle_repl)


display(dL_dW_abstract.replace(sigmaApply_L(A*B), xi))
display(dL_dW_abstract.replace(sigmaApply_L(A*B), xi).doit())
display(dL_dW_abstract.replace(sigmaApply_L(A*B), xi).doit().replace(dle, dle_repl)) #.doit())
# NOTE here it says the matrices are not aligned if we execute doit() to reveal the ones matrix that is dL_dS. True since assumption here is matrix multplication with dL_dS and right hand side, but in fact it is hadamard multiplication. 


# %% 
dL_dX_step = compose(lambd, sigmaApply, v)(A,B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(A).subs({A*B : vN(A,B)}).doit()

display(dL_dX_step)
display(dL_dX_step.replace(unapplied, applied))
#display(dL_dW_step.subs({A:X})) # replace won't work here

# Carrying out the multplication: 
display(dL_dX_step.subs({B:W}).doit()) # replace won't work here
display(dL_dX_step.subs({B:W}).doit().replace(unapplied, applied))




# %% markdown
# The first part: dldn

# %% markdown
# Direct substitution way: 
# %%
display( lambd(xi).diff(xi).subs(xi, applied) )
display( lambd(xi).diff(xi).subs(xi, applied).replace(lambd, lambd_L) )
display( lambd(xi).diff(xi).subs(xi, applied).replace(lambd, lambd_L).doit() )
# %% markdown
# The substitute into derivative way: 
# %%
display( lambd(xi).diff(xi).subs(xi, unapplied) )

display( lambd(xi).diff(xi).subs(xi, unapplied).replace(unapplied, applied) ) # gives same expression as in dldx

display( lambd(xi).diff(xi).subs(xi, unapplied).replace(unapplied, applied).replace(lambd, lambd_L) ) 



# %% 
# TODO cannot substitute here, gives error
ones = lambd(xi).diff(xi).subs(xi, applied).replace(lambd, lambd_L).doit()
display(ones)

#display(dL_dX_step.replace(lambdExpr, ones))



# %% markdown
# The second part: dndx * dsdn
# %% codecell
dN_dX_times_dS_dN = compose(sigmaApply, v)(A,B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(A).subs({A*B : vN(A,B)}).doit()

display(dN_dX_times_dS_dN)

display(dN_dX_times_dS_dN.subs({B:W})) # replace won't work here

# Carrying out the multplication: 
display(dN_dX_times_dS_dN.subs({B:W}).doit()) # replace won't work here



# %% markdown
# ### COMPARE: Symbolic form vs. Direct form vs. Step by Step form (which goes from symbolic to direct form by replacing)
# #### Symbolic Abstract Form (with respect to W):
# %% codecell
Lc = compose(lambd, sigmaApply, v)(A, B)
symb = Lc.replace(v, v_).replace(sigmaApply, sigmaApply_).diff(B)
symb
# %% markdown
# #### Direct form: (after the symbolic form)
# %% codecell
Lc.replace(v, vN).replace(sigmaApply, sigmaApply_).replace(lambd, lambd_).subs(elemToSpecD).diff(W).subs(specToElemD)
# %% markdown
# Just placing the "n" values right in place of the "epsilons" using the "doit" function:
# %% codecell
direct = Lc.replace(v, vN).replace(sigmaApply, sigmaApply_).replace(lambd, lambd_).subs(elemToSpecD).diff(W).subs(specToElemD).doit()
direct





# %% codecell
# Now verifying the above rule by applying the composition thing piece by piece via multiplication:
L.replace(v,vL).replace(sigmaApply, sigmaApply_).diff(B)
# %% codecell
L.replace(v,vL).replace(sigmaApply,sigmaApply_)#.diff()
# %% codecell
L.replace(v,vL)
# %% codecell
L.replace(v,vL).diff(sigmaApply(A*B))
# %% codecell
#L.replace(n,vL).diff(sigmaApply(A*B)).replace(sigmaApply,sigmaApply_)
## ERROR cannot do that
# %% codecell

#L.replace(n,vL).diff(sigmaApply(A*B)).subs(sigmaApply,sigmaApply_L) ## ERROR

nL = Lambda((A,B), v(A,B)); nL




#compose(lambd, sigmaApply, n)(A,B).diff(lambd)
display( diff(compose(lambd, sigmaApply, v)(A,B), compose(lambd, sigmaApply, v)(A,B)) )


display( diff(L, v(A,B)) )


display( L.replace(v, v_).replace(sigmaApply, sigmaApply_).diff(B) )




# %% codecell
# THis seems right:
dL_dS = lambd(Selem).replace(lambd, lambd_L).diff(Selem)
# THIS SEEMS WRONG : ??? how to tell for sure?
#lambd(Selem).diff(Selem).replace(lambd, lambd_L).doit()

display(dL_dS)


# %% codecell
# This is the X^T * dS/dN part
display(compose(sigmaApply, v)(A,B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(B).subs({A*B : vN(A,B)}).doit())
# %% codecell

dS_dN = compose(sigmaApply)(N).replace(sigmaApply, sigmaApply_).diff(N).subs({N : vN(A,B)}).doit()

dS_dN_abstract = compose(sigmaApply)(N).replace(sigmaApply, sigmaApply_).diff(N).subs(N, v_(A,B))
# ANOTHER WAY: sigmaApply_L(M).diff(M).subs({M : Nelem}).doit()
# WRONG:
#dS_dN = sigmaApply(Nelem).replace(sigmaApply, sigmaApply_).diff(Matrix(Nelem))
display(dS_dN_abstract)
display(dS_dN)



# %% codecell
from sympy import HadamardProduct

dN_dW = A.transpose()

dS_dW = dN_dW * dS_dN
dS_dW_abstract = compose(sigmaApply, v)(A,B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(B)

dL_dW = HadamardProduct(dL_dS, dS_dW)

display(dS_dW)
display(dS_dW.subs(A, X).doit())

display(dL_dW)


assert dL_dW == HadamardProduct(dL_dS, dN_dW * dS_dN ) 


# %%
dL_dW_hadamard = dL_dW.subs(A,X).doit()
# %%
display(dL_dW_abstract)
display(dL_dW_step)
display(dL_dW)
display(dL_dW_hadamard)

# %% markdown
# One more time as complete symbolic form:
# $$
# \begin{aligned}
# \frac{\partial L}{\partial W} &= \frac{\partial N}{\partial W} \times \frac{\partial S}{\partial N} \odot \frac{\partial L}{\partial S} \\
# &= X^T \times  \frac{\partial S}{\partial N} \odot \frac{\partial L}{\partial S}
# \end{aligned}
# $$
# where $\odot$ signifies the Hadamard product and $\times$ is matrix multiplication.
# %% codecell
HadamardProduct(dN_dW * dS_dN, dL_dS)
# %% codecell
direct
# %% codecell
assert HadamardProduct(dN_dW * dS_dN, dL_dS).equals(direct)
# %% codecell
# too long to see in editor:
symb.subs({A*B : vN(A,B)}).subs({A:X}).doit().replace(lambd, lambd_L)
# %% codecell
symb.subs({lambd: lambd_L})
# %% codecell
print(symb.subs({lambd: lambd_L}))


# %% codecell
LcL = compose(lambd_L, sigmaApply, v)(A, B)
LcL
# %% codecell
symbL = LcL.replace(v, v_).replace(sigmaApply, sigmaApply_)#.diff(A)
symbL
# %% codecell
compose(lambd, sigmaApply, v)(A,B).replace(v,v_).subs({lambd:lambd_L})#.subs({sigmaApply : sigmaApply_L})
# %% codecell
compose(lambd, sigmaApply, v)(A,B).replace(v,v_).replace(sigmaApply, sigmaApply_).replace(lambd, lambd_L)
# %% codecell
compose(lambd, sigmaApply, v)(A,B).replace(v,v_).replace(sigmaApply, sigmaApply_).replace(lambd, lambd_L).doit()
# %% codecell
compose(lambd, sigmaApply, v)(A,B).replace(v,v_).diff(B).doit()#replace(sigmaApply, sigmaApply_)#.replace(lambd, lambd_L).diff(B)
# %% codecell
compose(lambd, sigmaApply, v)(A,B).replace(v,v_).diff(B).replace(lambd, lambd_L)
# %% codecell
compose(lambd, sigmaApply, v)(A,B).replace(lambd, lambd_L)
# %% codecell
compose(lambd, sigmaApply, v)(A,B).replace(lambd, lambd_L).replace(v, v_).replace(sigmaApply, sigmaApply_)
# %% codecell
compose(lambd, sigmaApply, v)(A,B).replace(lambd, lambd_L).replace(v, v_).replace(sigmaApply, sigmaApply_).doit()#.diff(B)
# %% codecell
compose(lambd, sigmaApply, v)(A,B).replace(lambd, lambd_L).replace(v, v_).replace(sigmaApply, sigmaApply_).doit().diff(Matrix(B)).doit()

# %% codecell
sigmaApply = Function("sigma_apply", subscriptable=True)

#compose(lambd, sigmaApply, n)(A,B).replace(n,v).diff(B).replace(lambd, lambd_L).doit()# ERROR sigma apply is not subscriptable

#compose(lambd, sigmaApply, n)(A,B).replace(n,v).diff(B).subs({sigmaApply: sigmaApply_L})









# %% codecell
compose(sigmaApply_L, sigmaApply_L)(A)
# %% codecell
x = Symbol('x', applyfunc=True)
#compose(sigmaApply_, sigmaApply_)(x)##ERROR
compose(sigmaApply_, sigmaApply_)(A)#.replace(A,f(x))
# %% codecell
compose(lambda_L, nL)(A,B)

# %% codecell
VL = Lambda((A,B), Lambda((A,B), MatrixSymbol("V", A.shape[0], B.shape[1])))
VL
# %% codecell
VL(A,B)
# %% codecell
#saL = Lambda(A, Lambda(A, sigma(A)))
saL = Lambda(x, Lambda(x, sigma(x)))
#saL(n(A,B))## ERROR : the ultimate test failed: cannot even make this take an arbitrary function
#saL(n)
#s = lambda x : Lambda(x, sigma(x))
s = lambda x : sigma(x)
s(v(A,B))
# %% codecell
#sL = lambda x : Lambda(x, sigma(x))
#sL = Lambda(x, lambda x: sigma(x))

sL = Lambda(x, Lambda(x, sigma(x)))
sL
#sL(A)
