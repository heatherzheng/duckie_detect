import os
import random
import numpy as np
import math
import torch
from torch import nn
from torch.nn import init
from torch import optim

class model(nn.Module):

    def __init__(self, hidden_dim=8):
        super(model, self).__init__()
        self.hidden_dim = hidden_dim
        self.first = nn.Linear(4,hidden_dim)
        self.last = nn.Linear(hidden_dim,1)
        self.loss = nn.MSELoss(reduction='sum')

    def compute_Loss(self, pred_vec, gold_seq):
        return self.loss(pred_vec, gold_seq)

    def forward(self, input_seq):
        input_seq = torch.tensor(input_seq)
        prediction = self.first(input_seq)
        prediction = self.last(prediction)
        prediction = prediction.squeeze()
        return prediction
