import numpy as np

import torch
import torch.nn as nn
import torch.tensor as Tensor
from torch import Size, Tensor, FloatTensor
from torch.nn.parameter import Parameter
from torch.nn import Dropout, LayerNorm, Linear, Sequential, ReLU, Embedding, ModuleList, CrossEntropyLoss


from typing import *

from src.ModelStudy.TransformerXL.PositionwiseFeedForward import PositionwiseFeedForward
from src.ModelStudy.TransformerXL.MaskedMultiHeadAttention import MaskedMultiHeadAttention


class TransXLDecoderBlock(nn.Module):
    def __init__(self,
                 numHeads: int,
                 embedDim: int,
                 mhaInnerDim: int, ffInnerDim: int,
                 dropoutO: float, dropoutA: float = 0.):

        super().__init__()
        self.maskedMultiHeadAttention: MaskedMultiHeadAttention = \
            MaskedMultiHeadAttention(embedDim = embedDim,
                                     innerDim = mhaInnerDim,
                                     numHeads = numHeads,
                                     dropoutO= dropoutO,
                                     dropoutA = dropoutA)

        self.poswiseFeedForward: PositionwiseFeedForward = \
            PositionwiseFeedForward(embedDim = embedDim,
                                    innerDim = ffInnerDim,
                                    dropoutO= dropoutO)


    def forward(self,
                inputDec: FloatTensor,
                posEmbeddings: FloatTensor,
                u: FloatTensor,
                v: FloatTensor,
                mask = None, memories = None) -> Tensor:
        """
        Decoder block is made of masked multi-head attention and positionwise feed forward layer. The forward function applies the layers to the embedding input and positional embeddings.

        Arguments:
            inputDec: the input for the decoder block
                ---> shape == (S, B, E)
            posEmbeddings: the positional embeddings
                ---> shape == (P+S, E)
            u: the global (query-independent) bias towards certain keys / values = words
                ---> shape == (H, I)
            v: the global (query-independent) bias towards certain positions
                ---> shape == (H, I)
            mask: attention mask
                ---> shape TODO
            mems: TODO
                ---> shape TODO

        Returns:
              output after masked multi-head attention is passed through pos-wise feed forward layer
                ---> shape == (S, B, E)
        """
        return self.poswiseFeedForward(
            inputFF = self.maskedMultiHeadAttention(inputMHA = inputDec,
                                                    posEmbeddings = posEmbeddings,
                                                    memory = memories,
                                                    u = u, v = v,
                                                    mask = mask
                                                    )
        )