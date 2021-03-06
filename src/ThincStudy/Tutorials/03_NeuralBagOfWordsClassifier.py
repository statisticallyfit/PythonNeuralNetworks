# %% markdown
# Source: https://github.com/explosion/thinc/blob/master/examples/03_textcat_basic_neural_bow.ipynb

# # Basic Neural Bag-Of-Words Text Classifier with Thinc
# Goal: show how to implement a neural text classification model in Thinc.
#
# For simple and standalone tokenization, use the [`syntok`](https://github.com/fnl/syntok) package and the following function:
# %% codecell
from syntok.tokenizer import Tokenizer
from typing import List, Optional


# todo: return type?
def tokenizeTexts(texts: List[str]) -> List[List[str]]:
    tok: Tokenizer = Tokenizer()

    return [[token.value for token in tok.tokenize(currText)] for currText in texts]


# %% markdown
# ## 1. Setting up the Data
# The `loadData` function loads the DBPedia Ontology dataset from `ml_datasets.dbpedia`, converts and tokenizes the data, and generates a simple vocabulary mapping. (Option: to try `ml_datasets.imdb` for the IMDB review dataset, instead).
# %% codecell
import ml_datasets
import numpy

def loadData():
    print("Loading data ...")

    trainData, devData = ml_datasets.dbpedia(limit = 200)

    # Separate into texts and cats (??)
    trainTexts, trainCats = zip(*trainData)
    devTexts, devCats = zip(*devData)
    # todo: type
    uniqueCats = list(numpy.unique(numpy.concatenate((trainCats, devCats))))
    numClasses: int = len(uniqueCats)

    print(f"{len(trainData)} training / {len(devData)} dev\n{numClasses} classes")

    # todo: type?
    trainY = numpy.zeros((len(trainCats), numClasses), dtype="f")
    devY = numpy.zeros((len(devCats), numClasses), dtype="f")

    # todo: what does this do here?
    for i, cat in enumerate(trainCats):
        trainY[i][uniqueCats.index(cat)] = 1

    for i, cat in enumerate(devCats):
        devY[i][uniqueCats.index(cat)] = 1

    # Tokenizing the data:
    # todo type?
    trainTokenized: List[List[str]] = tokenizeTexts(texts = trainTexts)
    devTokenized: List[List[str]] = tokenizeTexts(texts = devTexts)

    # Generate simple vocabulary mapping
    vocab = {}
    indexCounter = 1 # used to make vocab float type not int

    for tokText in trainTokenized:
        for tok in tokText:
            if tok not in vocab:
                vocab[tok] = indexCounter
                indexCounter += 1

    # Map texts using vocab for the training data:
    trainX = [] # the training data from which we predict
    for tokText in trainTokenized:
        trainX.append(numpy.array([vocab.get(tok, 0) for tok in tokText]))
    # making float type:
    trainX = map(float, trainX)

    # Map texts using vocab for the dev data:
    devX = []
    for tokText in devTokenized:
        devX.append(numpy.array([vocab.get(tok, 0) for tok in tokText]))
    # making float type
    devX = map(float, devX)

    return (trainX, trainY), (devX, devY), vocab

# %% markdown
# ## 2. Defining the Model and Config
# ### Defining the Code Model:
# The model takes a list of $2$-dimensional arrays (the tokenized texts mapped to vocabulary IDs) and outputs a $2$d array.
#
# Because the embedding layer's `nV` dimension (the number of entries in the lookup table) depends on the `vocab` and training data, it is poassed in as argument and registered as a **reference**, making it easier to retrieve it later via `model.get_ref("embed")`, to set its `nV dimension.`

# %% codecell
from typing import List
import thinc
from thinc.api import Model, chain, list2ragged, with_array, reduce_mean, Softmax
from thinc.types import Array2d

@thinc.registry.layers("EmbedPoolTextcat.v1")
def EmbedPoolTextcat(embed: Model[Array2d, Array2d]) -> Model[List[Array2d], Array2d]:

    with Model.define_operators({">>": chain}):
        model: Model = list2ragged() \
                       >> with_array(layer = embed) \
                       >> reduce_mean() \
                       >> Softmax()

        # Embedding layer's nV dimension depends on vocab and training data, so it is registered as a reference here (can later retrieve it and set its nV dimension only when we need to)
        model.set_ref(name = "embed", value = embed)

        return model

# %% markdown
# ### Defining the Config:
# The config defines the top-level model using the registered `EmbedPoolTestcat` function and the `embed` argument, referencing the `Embed` layer.
# %% codecell
CONFIG_STR: str = """
[hyper_params]
width = 64

[model]
@layers = "EmbedPoolTextcat.v1"

[model.embed]
@layers = "Embed.v1"
nO = ${hyper_params:width}

[optimizer]
@optimizers = "Adam.v1"
learn_rate = 0.001

[training]
batch_size = 8
n_iter = 10
"""
# %% markdown
# ## 3. Training Setup
# When the config is loaded, it's first parsed as a dictionary and all references to values from other sections, e.g. `${hyper_params:width}` are replaced. The result is a nested dictionary describing the objects defined in the config. `registry.make_from_config` then creates the objects and calls the functions **bottom-up**.
# %% codecell
from thinc.api import registry, Config
CONFIG: Config = registry.make_from_config(Config().from_str(CONFIG_STR))
CONFIG

# %% markdown
# Training the model now: once the data is loaded, we will know the vocabulary size and can set the dimension of the embedding layer `nV`:
#
# * `model.get_ref("embed")` returns the layer defined as the ref "`embed`"
# * `set_dim` sets a value for the dimension.
# * use `model.initialize` with input and output data to fill in the other missing shapes.
# %% codecell
from thinc.optimizers import Optimizer

(trainX, trainY), (devX, devY), vocab = loadData()
# %% codecell
batchSize: int = CONFIG["training"]["batch_size"]
optimizer: Optimizer = CONFIG["optimizer"]
# %% codecell
model: Model = CONFIG["model"]
model.get_ref(name = "embed").set_dim(name = "nV", value = len(vocab))

model



# %% codecell
# TODO ERROR HERE
model.initialize(X = trainX, Y = trainY)


# %% codecell
def evaluateModel(model: Model, devX, devY, batchSize: int) -> float:

    numCorrect = 0.0
    total = 0.0

    for X, Y in model.ops.multibatch(batchSize, devX, devY):
        Yh = model.predict(X)

        for j in range(len(Yh)):
            numCorrect += Yh[j].argmax(axis=0) == Y[j].argmax(axis=0)
        total += len(Y)

    return float(numCorrect / total)

# %% markdown
# ## 3. Training the Model
# %% codecell
from tqdm.notebook import tqdm
from thinc.api import fix_random_seed, Model
from thinc.optimizers import Optimizer

from thinc.types import Array2d
from typing import Optional, List


# todo types?
def trainModel(model: Model, trainX, trainY, optimizer: Optimizer, numIters: int, batchSize: int):

    for epoch in range(numIters):
        loss: float = 0.0
        # todo: type??
        batches = model.ops.multibatch(batchSize, trainX, trainY, shuffle=True)

        for X, Y in tqdm(batches, leave = False):
            Yh, backprop = model.begin_update(X = X)
            # todo type ??
            dLoss = []

            for i in range(len(Yh)):
                dLoss.append(Yh[i] - Y[i])
                loss += ((Yh[i] - Y[i]) ** 2).sum()

            backprop(numpy.array(dLoss)) # TODO: why here convert to  numpy array? in tut3 there was no need??
            model.finish_update(optimizer = optimizer)

        # todo type?
        score = evaluateModel(model = model, devX = devX, devY = devY, batchSize = batchSize)
        #print(f"{i}\t{loss:.2f}\t{score:.3f}")

        print("Epoch: {} | Loss: {} | Score: {}".format(epoch, loss, score))


# %% codecell
fix_random_seed(0)

trainModel(model = model,
           trainX = trainX, trainY = trainY,
           optimizer = optimizer,
           numIters = range(CONFIG["training"]["n_iter"]),
           batchSize = batchSize)
