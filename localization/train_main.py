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
import time
from tqdm import tqdm

def change(lst):
	list = []
	for e in lst:
		list.append(float(e))
	return list

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
			data_outputs.append(i[1:2])
			data_inputs.append(i[2:])
	return data_inputs,data_outputs
## add more data: velocity , omega, past position
if __name__ == '__main__':
	train_inputs, train_outputs= read_input()
	m = m()
	m.load_state_dict(torch.load('model_1.pt'))
	optimizer = optim.Adam(m.parameters(),lr=0.001)
	minibatch_size = 3
	num_minibatches = len(train_inputs) // minibatch_size

	for epoch in (range(30)):
		# Training
		print("Training")
		# Put the model in training mode
		m.train()
		start_train = time.time()

		for group in tqdm(range(num_minibatches)):
			total_loss = None
			optimizer.zero_grad()
			for i in range(group * minibatch_size, (group + 1) * minibatch_size):
				input_seq = train_inputs[i]
				gold_seq = torch.tensor(train_outputs[i])
				prediction = m(input_seq)
				loss = m.compute_Loss(prediction, gold_seq)
				# On the first gradient update
				if total_loss is None:
					total_loss = loss
				else:
					total_loss += loss
			total_loss = total_loss / 3
			total_loss.backward()
			optimizer.step()
		print("Training time: {} for epoch {}".format(time.time() - start_train, epoch))

	torch.save(m.state_dict(), 'model_1.pt')
