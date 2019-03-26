import numpy as np
import torch
import torch.nn as nn
from torch.nn import init
import torch.optim as optim
import math
import random
import os
from pathlib import Path
from model import model as m
import least_square

### read train & test input and output
def read_input():
	data_inputs = []
	data_outputs = []
	with open("../data/data.txt") as f:
		content = f.readlines()
		for i in content:
			i = i.strip("\n")
			i = i.split()
			i = [float(x) for x in i]
			temp = []
			temp_box_x = int(i[4])-int(i[2])
			temp_box_y = int(i[5])-int(i[3])
			temp.append(i[0])
			temp.append(min(temp_box_x,temp_box_y))
			data_outputs.append(i[1:2])
			data_inputs.append(temp)
	return data_inputs,data_outputs

if __name__ == '__main__':
    m = m()
    m.load_state_dict(torch.load('model_1.pt'))
    train_inputs, train_outputs= read_input()
    for i in range(len(train_inputs)):
        print(m(train_inputs[i]))
        print(train_outputs[i])
        print("****")
