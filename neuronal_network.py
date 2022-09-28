import numpy as np

class NeuronalNetwork():  # The goal of this network is to process data, not to store any kind of weights of biases, but it does anyways
	def __init__(self, data):
		self.weights = data.weights[0]
		self.biases = data.biases
		self.ReLU = Activation_ReLU()
		self.Softmax = Activation_Softmax()

	def forward(self, inputs):
		x = inputs
		for i in range(len(self.weights) - 1):
			x = np.dot(x, self.weights[i]) + self.biases[i]
			x = self.ReLU.forward(x)
		x = np.dot(x, self.weights[-1]) + self.biases[-1]
		x = self.Softmax.forward(x)
		return x

class Activation_ReLU():
	def forward(self, inputs):
		return np.maximum(0, inputs)

class Activation_Softmax():
	def forward(self, inputs):
		exp_values = np.exp(inputs - np.max(inputs))
		probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
		return probabilities