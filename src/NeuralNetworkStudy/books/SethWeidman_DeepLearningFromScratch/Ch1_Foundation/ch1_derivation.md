# Derivations For Matrix Derivative Rule of $L = \lambda( \sigma_{\text{apply}}( \nu(X, W) ) )$

```python
from sympy import Matrix, Symbol, derive_by_array, Lambda, Function, MatrixSymbol, Identity, Derivative, symbols, diff
from sympy.abc import x, i, j, a, b
```

```python
from functools import reduce
import itertools 

from typing import *
import sys
import os

PATH: str = '/development/projects/statisticallyfit/github/learningmathstat/PythonNeuralNetNLP'

UTIL_DISPLAY_PATH: str = PATH + "/src/utils/GeneralUtil/"

NEURALNET_PATH: str = PATH + '/src/NeuralNetworkStudy/books/SethWeidman_DeepLearningFromScratch'

#os.chdir(PATH)
#assert os.getcwd() == NEURALNET_PATH

sys.path.append(PATH)
#assert PATH in sys.path

sys.path.append(UTIL_DISPLAY_PATH)
#assert UTIL_DISPLAY_PATH in sys.path

sys.path.append(NEURALNET_PATH)#
#assert NEURALNET_PATH in sys.path


```

```python title="codecell"
from src.utils.GeneralUtil import *
from src.MatrixCalculusStudy.MatrixDerivLib.symbols import Deriv
from src.MatrixCalculusStudy.MatrixDerivLib.diff import diffMatrix
from src.MatrixCalculusStudy.MatrixDerivLib.printingLatex import myLatexPrinter

from IPython.display import display, Math
from sympy.interactive import printing
printing.init_printing(use_latex='mathjax', latex_printer= lambda e, **kw: myLatexPrinter.doprint(e))
```

```python
import itertools

from functools import reduce

from typing import *
```

```python title="codecell"
n,m,p = 3,3,2


xi  = Symbol('xi')
xi_1  = Symbol('xi_1')
beta = Symbol('beta')


X = Matrix(n, m, lambda i,j : var_ij('x', i, j))
W = Matrix(m, p, lambda i,j : var_ij('w', i, j))

A = MatrixSymbol('X',n,m)
B = MatrixSymbol('W',m,p)

# matrix variable for sympy Lambda function arguments
M = MatrixSymbol('M', i, j)# abstract shape
```
```python title="codecell"
#compose(sigmaApply)(N).replace(sigmaApply, sigmaApply_).diff(N).subs({N : vN(A,B)}).doit()
```
```python title="codecell"
###N = MatrixSymbol("N", n, p)# shape of A*B### use Nelem below


showGroup([
    X, W, Matrix(A)
])
```

```python title="codecell"
v = Function("nu",applyfunc=True)
v_ = lambda a,b: a*b
vL = Lambda((a,b), a*b)
VL = Lambda((A,B), MatrixSymbol('V', A.shape[0], B.shape[1]))
vN = lambda mat1, mat2: Matrix(mat1.shape[0], mat2.shape[1], lambda i, j: Symbol("n_{}{}".format(i+1, j+1))); vN

Nelem = vN(X, W)
Nspec = v_(X,W)
N = v(A,B)


showGroup([
    Nelem, Nspec, N, VL
])
```


```python
sigma = Function('sigma')
sigmaApply = Function("sigma_apply") #lambda matrix:  matrix.applyfunc(sigma)
sigmaApply_ = lambda matrix: matrix.applyfunc(sigma)
sigmaApply_L = Lambda(M, M.applyfunc(sigma))


S = sigmaApply(N)
Sspec = S.subs({A:X, B:W}).replace(v, v_).replace(sigmaApply, sigmaApply_)
Selem = S.replace(v, vN).replace(sigmaApply, sigmaApply_)


showGroup([
    S, Sspec, Selem
])
```


```python
lambd = Function("lambda")
lambd_ = lambda matrix : sum(matrix)
#lambda_L = Lambda(M, sum(M))

ABres = MatrixSymbol("R", A.shape[0], B.shape[1])
lambd_L = Lambda(ABres, sum(ABres))

#L = lambd(sigmaApply(v(A,B)))
L = compose(lambd, sigmaApply, v)(A, B)
L


```

```python title="codecell"
elemToSpecD = dict(itertools.chain(*[[(Nelem[i, j], Nspec[i, j]) for j in range(p)] for i in range(n)]))
elemToSpec = list(elemToSpecD.items())

specToElemD = {val:key for key, val in elemToSpecD.items()}
specToElem = list(specToElemD.items())

Matrix(elemToSpec)
```

```python title="codecell"

elemToSpecFuncD = dict(itertools.chain(*[[(Nelem[i, j], Function("n_{}{}".format(i + 1, j + 1))(Nspec[i, j])) for j in range(p)] for i in range(n)]))

elemToSpecFunc = list(elemToSpecFuncD.items())

specFuncToElemD = {val : key for key , val in elemToSpecFuncD.items()}
specFuncToElem = list(specFuncToElemD.items())

Matrix(elemToSpecFunc)


```

```python title="codecell"
elemToNFuncD = dict(itertools.chain(*[[(Nelem[i, j], Function("n_{}{}".format(i + 1, j + 1))(*X,*W)) for j in range(p)] for i in range(n)]))

elemToNFunc = list(elemToNFuncD.items())

nfuncToElemD = {val: key for key, val in elemToNFuncD.items()}
nfuncToElem = list(nfuncToElemD.items())

Matrix(elemToNFunc)


```

```python title="codecell"
elemToNmatfuncD = dict(itertools.chain(*[[(Nelem[i, j], Function("n_{}{}".format(i+1,j+1))(A,B) ) for j in range(p)] for i in range(n)]))

elemToNmatfunc = list(elemToNmatfuncD.items())

nmatfuncToElemD = {val: key for key, val in elemToNmatfuncD.items()}
nmatfuncToElem = list(nmatfuncToElemD.items())

Matrix(elemToNmatfunc)


```

```python title="codecell"
nmatfuncToSpecD = dict(zip(elemToNmatfuncD.values(), elemToSpecD.values()))

nmatfuncToSpec = list(nmatfuncToSpecD.items())

Matrix(nmatfuncToSpec)
```


```python

# Overall abstract
dL_dX_overallAbstract = compose(lambd, sigmaApply)(VL).diff(A).replace(VL, v(A, B))

dL_dW_overallAbstract = compose(lambd, sigmaApply)(VL).diff(B).replace(VL, v(A, B))

showGroup([
    dL_dX_overallAbstract, 
    dL_dW_overallAbstract
])
```

```python title="codecell"
dL_dW_abstract = compose(lambd, sigmaApply, v)(A, B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(B)
#L.replace(v,v_).replace(sigmaApply, sigmaApply_).diff(B)

showGroup([
    dL_dW_abstract,
    dL_dW_abstract.subs({lambd : lambd_L})
])
```

```python
dL_dX_abstract = compose(lambd, sigmaApply, v)(A, B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(A)
#L.replace(v, v_).replace(sigmaApply, sigmaApply_).diff(A)

dL_dX_abstract
```


```python title="codecell"
dL_dW_direct = L.replace(v, vN).replace(sigmaApply, sigmaApply_).replace(lambd, lambd_).subs(elemToSpecD).diff(W).subs(specToElemD)

dL_dW_direct = dL_dW_direct.doit()

dL_dW_direct
```
```python
dL_dX_direct = L.replace(v, vN).replace(sigmaApply, sigmaApply_).replace(lambd, lambd_).subs(elemToSpecD).diff(X).subs(specToElemD)

dL_dX_direct = dL_dX_direct.doit()

dL_dX_direct
```

```python
unapplied = sigmaApply_L(vN(A,B))
unapplied
# Also works: same as above:
#compose(sigmaApply, v)(A,B).replace(v, vN).replace(sigmaApply , sigmaApply_L)
```
```python
applied = unapplied.doit()
applied
```

```python
dL_dW_step = compose(lambd, sigmaApply, v)(A,B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(B).subs({A*B : vN(A,B)}).doit()

showGroup([
    dL_dW_step,
    dL_dW_step.replace(unapplied, applied),
    # Carrying out the multplication:
    dL_dW_step.subs({A:X}).doit(), # replace won't work here
    dL_dW_step.subs({A:X}).doit().replace(unapplied, applied)
])


```

```python
dL_dX_step = compose(lambd, sigmaApply, v)(A,B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(A).subs({A*B : vN(A,B)}).doit()


showGroup([
    dL_dX_step,
    dL_dX_step.replace(unapplied, applied),
    dL_dX_step.subs({B:W}).doit(),
    dL_dX_step.subs({B:W}).doit().replace(unapplied, applied)
])


```

Trying to replace further to get the ones matrix for the deriv of lambda expression, but doesn't work, see code below for why (hadamard is not present, just matrix multiplication. Chain rule in this form doesn't know there should be hadamard product between deriv of $\lambda$ expression and $\frac{dS}{dX}$ expression)
```python
dle = lambd(xi).diff(xi)
dle_repl = lambd(xi).diff(xi).subs(xi, applied).replace(lambd, lambd_L)

showGroup([
    dle,
    dle_repl
])
```
```python
showGroup([
    dL_dW_abstract.replace(sigmaApply_L(A*B), xi),
    dL_dW_abstract.replace(sigmaApply_L(A*B), xi).doit(),
    dL_dW_abstract.replace(sigmaApply_L(A*B), xi).doit().replace(dle, dle_repl) #.doit())
])

# NOTE here it says the matrices are not aligned if we execute doit() to reveal the ones matrix that is dL_dS. True since assumption here is matrix multplication with dL_dS and right hand side, but in fact it is hadamard multiplication.


```

The first part: $\frac{dL}{dS}$

Direct substitution way:
```python
showGroup([
    lambd(xi).diff(xi).subs(xi, applied),
    lambd(xi).diff(xi).subs(xi, applied).replace(lambd, lambd_L),
    lambd(xi).diff(xi).subs(xi, applied).replace(lambd, lambd_L).doit()
])
```

The substitute into derivative way:
```python
showGroup([
    lambd(xi).diff(xi).subs(xi, unapplied),
    lambd(xi).diff(xi).subs(xi, unapplied).replace(unapplied, applied),
    # gives same expression as in dldx
    lambd(xi).diff(xi).subs(xi, unapplied).replace(unapplied, applied).replace(lambd, lambd_L)
])


```

The second part: $\frac{\partial N}{\partial X} \times \frac{\partial S}{\partial N}$


```python title="codecell"
dN_dW_times_dS_dN = compose(sigmaApply, v)(A,B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(B).subs({A*B : vN(A,B)}).doit()

showGroup([
    dN_dW_times_dS_dN,
    dN_dW_times_dS_dN.subs({A:X}), # replace won't work here
    # Carrying out the multplication:
    dN_dW_times_dS_dN.subs({A:X}).doit() # replace won't work here
])
```

```python
dN_dX_times_dS_dN = compose(sigmaApply, v)(A,B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(A).subs({A*B : vN(A,B)}).doit()

showGroup([
    dN_dX_times_dS_dN,
    dN_dX_times_dS_dN.subs({B:W}), # replace won't work here
    # Carrying out the multplication:
    dN_dX_times_dS_dN.subs({B:W}).doit() # replace won't work here
])



```

```python title="codecell"
# THis seems right:
dL_dS = lambd(Selem).replace(lambd, lambd_L).diff(Selem)
# ANOTHER WAY: lambd(xi).diff(xi).subs(xi, applied).replace(lambd, lambd_L).doit()

# THIS SEEMS WRONG : ??? how to tell for sure?
#lambd(Selem).diff(Selem).replace(lambd, lambd_L).doit()

dL_dS
```


```python title="codecell"

dS_dN = compose(sigmaApply)(M).replace(sigmaApply, sigmaApply_).diff(M).subs({M : vN(A,B)}).doit()

dS_dN_abstract = compose(sigmaApply)(M).replace(sigmaApply, sigmaApply_).diff(M).subs(M, v_(A,B))
# ANOTHER WAY: sigmaApply_L(M).diff(M).subs({M : Nelem}).doit()
# WRONG:
#dS_dN = sigmaApply(Nelem).replace(sigmaApply, sigmaApply_).diff(Matrix(Nelem))
showGroup([
    dS_dN,
    dS_dN_abstract
])
```


$$
\begin{aligned}
\frac{\partial L}{\partial W} &= \frac{\partial L}{\partial S} \odot \bigg( \frac{\partial N}{\partial W} \times \frac{\partial S}{\partial N} \bigg) \\
&= \frac{\partial L}{\partial S} \odot \bigg( X^T \times  \frac{\partial S}{\partial N} \bigg)
\end{aligned}
$$
where $\odot$ signifies the Hadamard product and $\times$ is matrix multiplication.



```python title="codecell"
from sympy import HadamardProduct

dN_dW = A.transpose()

dS_dW = dN_dW * dS_dN
dS_dW_abstract = compose(sigmaApply, v)(A,B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(B)

dL_dW = HadamardProduct(dL_dS, dS_dW)
dL_dW_hadamard = dL_dW.subs(A,X).doit()

assert dL_dW == HadamardProduct(dL_dS, dN_dW * dS_dN )

showGroup([
    dS_dW, 
    dS_dW_abstract, 
    dS_dW.subs(A, X).doit(), 
    dL_dW, 
    dL_dW_hadamard
])


```

$$
\begin{aligned}
\frac{\partial L}{\partial X} &= \bigg( \frac{\partial L}{\partial S} \odot  \frac{\partial S}{\partial N} \bigg) \times \frac{\partial N}{\partial X}  \\
&= \bigg( \frac{\partial L}{\partial S} \odot \frac{\partial S}{\partial N} \bigg) \times W^T 
\end{aligned}
$$
where $\odot$ signifies the Hadamard product and $\times$ is matrix multiplication.

```python
dN_dX = B.transpose()

dS_dX = dS_dN * dN_dX
dS_dX_abstract = compose(sigmaApply, v)(A,B).replace(v, v_).replace(sigmaApply, sigmaApply_).diff(A)

dL_dN = HadamardProduct(dL_dS, dS_dN)

dL_dX = dL_dN * dN_dX #).subs(B, W).doit()
dL_dX_hadamard = dL_dX.subs(B, W).doit()

assert dL_dX == HadamardProduct(dL_dS, dS_dN) * dN_dX

showGroup([
    dS_dX, 
    dS_dX.subs(B, W),
    dS_dX_abstract, 
    dL_dN, 
#    dS_dX.subs(B, W).doit(), 
    dL_dX, 
    dL_dX_hadamard
])
```


```python
showGroup([
    dL_dX_abstract, 
    dL_dX_step, 
    dL_dX, 
    dL_dX_hadamard
])
```

```python
showGroup([
    dL_dW_abstract, 
    dL_dW_step, 
    dL_dW, 
    dL_dW_hadamard
])
```

```python title="codecell"
compose(lambd, sigmaApply, v)(A,B).replace(lambd, lambd_L)
```
```python title="codecell"
compose(lambd, sigmaApply, v)(A,B).replace(v,v_).subs({lambd:lambd_L})#.subs({sigmaApply : sigmaApply_L})
```
```python title="codecell"
compose(lambd, sigmaApply, v)(A,B).replace(v,v_).replace(sigmaApply, sigmaApply_).replace(lambd, lambd_L)
```
```python title="codecell"
compose(lambd, sigmaApply, v)(A,B).replace(lambd, lambd_L).replace(v, v_).replace(sigmaApply, sigmaApply_)
```

```python title="codecell"

compose(lambd, sigmaApply, v)(A,B).replace(v,v_).replace(sigmaApply, sigmaApply_).replace(lambd, lambd_L).doit()
```

```python
# Alternative to the above: using the lower case matrix element names rather than upper case (from MatrixSymbol)
compose(lambd, sigmaApply, v)(A, B).replace(v, vN).replace(sigmaApply, sigmaApply_).replace(lambd, lambd_).subs(elemToSpecD)
```


```python title="codecell"
compose(lambd, sigmaApply, v)(A,B).replace(v,v_).diff(B).doit()#replace(sigmaApply, sigmaApply_)#.replace(lambd, lambd_L).diff(B)
```
```python title="codecell"
compose(lambd, sigmaApply, v)(A,B).replace(v,v_).diff(B).replace(lambd, lambd_L)


```

