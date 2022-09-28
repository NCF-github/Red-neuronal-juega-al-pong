import json
import pygame
import numpy as np
import os, sys
import copy
from datetime import datetime
from neuronal_network import NeuronalNetwork
from pong_de_prueba import run_game

class Data():  # This creates a class with weights and biases
	def __init__(self):
		self.weights = [0.1 * np.random.randn(5, 4), 0.1 * np.random.randn(4, 4), 0.1 * np.random.randn(4, 3)],
		self.biases = [np.zeros((1, 4)), np.zeros((1, 4)), np.zeros((1, 3))]

	def mix_it_up(self, error):
		for array in self.weights[0]:
			shape = array.shape
			array += error * 0.04 * np.random.randn(shape[0], shape[1])
		for arry in self.biases[0]:
			shape = array.shape
			array += error * 0.04 * np.random.randn(shape[0], shape[1])

	def load(self, filename):
		with open(filename) as read_data:
			data = json.load(read_data)
			self.weights = np.array(data["weights"])

def save_current_data(data):
	save_weights = [[[[n for n in x] for x in inputs] for inputs in array] for array in data.weights]
	save_biases = [[[n for n in inputs] for inputs in array] for array in data.biases]

	save_data = {
	"weights":save_weights,
	"biases":save_biases
	}

	now = datetime.now()
	dt_string = now.strftime("%d-%m-%Y--%H-%M-%S")
	filename = "./save_files/" + dt_string + ".txt"

	with open(filename, "w") as test_file:
		json.dump(save_data, test_file)

def training_method_1_max_loss(max_loss, population, games_per_individual):
	population = population
	games_per_individual = games_per_individual

	data_sets = [Data() for i in range(population)]  # Intial data set
	losses = [None for i in range(population)]

	best_data_loss = 1
	best_data = Data()

	n = max_loss
	iteration = 0
	while best_data_loss > n:

		for idx, data in enumerate(data_sets):

			neuronal_network = NeuronalNetwork(data)

			error = []
			for i in range(games_per_individual):
				run_game(neuronal_network, error)

			losses[idx] = round(sum(error)/games_per_individual, 2)

		best_data_loss = min(losses)
		best_data = copy.deepcopy(data_sets[losses.index(min(losses))])
		new_data_sets = []


		still_stay_with_current_data = False
		if best_data_loss >= 0.99 and still_stay_with_current_data == False:
			new_data_sets = [Data() for i in range(len(data_sets))]
		else:
			best_ones = []
			for i, loss in enumerate(losses):
				if loss == min(losses):
					best_ones.append(i)

			if len(best_ones) < population:
				new_data_sets.append(Data())

			for i in best_ones:
				new_data_sets.append(copy.deepcopy(data_sets[i]))

			for i in range(population - len(new_data_sets)):
				idx = i % len(best_ones)
				idx = best_ones[idx]
				new_data_sets.append(copy.deepcopy(data_sets[idx]))
				new_data_sets[-1].mix_it_up(best_data_loss)

			if best_data_loss <= 0.9:
				still_stay_with_current_data = True
			elif best_data_loss >= 0.99:
				still_stay_with_current_data = False

		data_sets = copy.deepcopy(new_data_sets)

		iteration += 1

		if best_data_loss != 1:
			print(f"{iteration}: {best_data_loss}")
		else:
			print(f"{iteration}: 1.00")

	save_current_data(best_data)

if __name__ == "__main__":
	pygame.init()

	population = 10
	games_per_individual = 2

	training_method_1_max_loss(0.05, population, games_per_individual)

	pygame.quit()

# Executing this will create a json file that contains the weights and biases of a neuronal network