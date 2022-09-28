import random
import sys, os
import pygame
import json
import math
from neuronal_network import NeuronalNetwork
from main_training import Data

class Screen():
	def __init__(self, width, height, display = True):
		self.width = width
		self.height = height
		self.display = display

		if self.display == True:
			pygame.init()
			self.screen = pygame.display.set_mode((self.width, self.height))
			self.fps = 60
			self.clock = pygame.time.Clock()
			self.bg_color = (0, 0, 0)
			self.object_color = (255, 255, 255)

	def update(self, ball, pallet1, pallet2):
		if self.display == True:
			self.screen.fill(self.bg_color)
			pygame.draw.rect(self.screen, self.object_color, (int(pallet1.x), int(pallet1.y), pallet1.width, pallet1.height))
			pygame.draw.rect(self.screen, self.object_color, (int(pallet2.x), int(pallet2.y), pallet2.width, pallet2.height))
			pygame.draw.circle(self.screen, self.object_color, (ball.x, ball.y), ball.radius)
			pygame.display.update()
			self.clock.tick(self.fps)

class Pallet():
	def __init__(self, x, screen, some_input):
		self.width = 20
		self.height = 100
		self.x = x
		self.y = int(screen.height / 2 - self.height / 2)
		self.speed = 10
		self.input = some_input

	def move(self, screen, ball):
		X = [self.y, self.height, ball.y, ball.y_speed, screen.height]
		self.input.update(X)
		if self.input.up == True:
			self.y -= self.speed
			if self.y < 0:
				self.y = 0
		if self.input.down == True:
			self.y += self.speed
			if self.y + self.height > screen.height:
				self.y = screen.height - self.height
		if self.input.still == True:
			pass

class Ball():
	def __init__(self, screen):
		self.radius = 10
		self.x = float(screen.width / 2)
		self.y = float(screen.height / 2)
		self.x_speed = 0
		self.y_speed = 0
		self.speed = 10
		self.set_initial_speed()
		self.game_over = False
		self.bounces = 0

	def set_initial_speed(self):
		self.x_speed = float(random.randint(5, 9))
		self.y_speed = float((self.speed ** 2 - self.x_speed ** 2) ** 0.5)
		self.x_proportion = self.x_speed / (self.x_speed + self.y_speed)
		self.y_proportion = self.y_speed / (self.x_speed + self.y_speed)

		if random.random() < 0.5:
			self.x_speed = -self.x_speed
		if random.random() < 0.5:
			self.y_speed = -self.y_speed

	def move(self):
		for i in range(self.bounces):
			if self.x_speed > 0:
				self.x_speed += self.bounces * self.x_proportion
			else:
				self.x_speed -= self.bounces * self.x_proportion

			if self.y_speed > 0:
				self.y_speed += self.bounces * self.y_proportion
			else:
				self.y_speed -= self.bounces * self.y_proportion
		self.bounces = 0

		self.x += self.x_speed
		self.y += self.y_speed

	def bounce(self, screen, pallet1, pallet2):
		if self.y < self.radius:
			self.y = self.radius
			self.y_speed = -self.y_speed

		elif self.y > screen.height - self.radius:
			self.y = screen.height - self.radius
			self.y_speed = -self.y_speed


		if self.x_speed > 0:
			if abs(self.x - pallet1.x) < self.radius:
				if self.y + self.radius > pallet1.y and self.y - self.radius < pallet1.y + pallet1.height:
					self.x_speed = -self.x_speed
					self.bounces += 1

		if self.x_speed < 0:
			if abs(self.x - pallet2.x - pallet2.width) < self.radius:
				if self.y + self.radius > pallet2.y:
					self.x_speed = -self.x_speed
					self.bounces += 1

	def is_game_over(self, screen):
		if self.x + self.radius < 0:
			self.game_over = True
			print("Human player wins")
		elif self.x - self.radius > screen.width:
			self.game_over = True
			print("Neuronal network wins")

class Keys_Input():
	def __init__(self):
		self.up = False
		self.down = False
		self.still = False

	def update(self, inputs=None):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					self.up = True
				if event.key == pygame.K_DOWN:
					self.down = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					self.up = False
				if event.key == pygame.K_DOWN:
					self.down = False
		if self.up == False and self.down == False:
			self.still = True
		else:
			self.still = False

class Neuronal_Network_Input():
	def __init__(self, neuronal_network):
		self.neuronal_network = neuronal_network
		self.up = False
		self.down = False
		self.still = True

	def update(self, inputs):
		results = self.neuronal_network.forward(inputs)[0]

		self.up = False
		self.down = False
		self.still = False

		if results[0] > results[1]:
			if results[0] > results[2]:
				self.up = True
			else:
				self.still == True
		else:
			if results[1] > results[2]:
				self.down = True
			else:
				self.still = True

def run_game(filename):
	data = Data()
	data.load(filename)
	neuronal_network = NeuronalNetwork(data)
	screen = Screen(1200, 800)
	pallet1 = Pallet(screen.width - 70, screen, Keys_Input())
	pallet2 = Pallet(50, screen, Neuronal_Network_Input(neuronal_network))
	ball = Ball(screen)

	while not ball.game_over:
		pallet1.move(screen, ball)
		pallet2.move(screen, ball)
		ball.move()
		ball.bounce(screen, pallet1, pallet2)
		ball.is_game_over(screen)
		screen.update(ball, pallet1, pallet2)

pygame.init()

run_game("./save_files/01-02-2022--19-00-47.txt")

pygame.quit()
