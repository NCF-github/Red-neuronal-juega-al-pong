import random
import sys, os
import pygame

class Screen():
	def __init__(self, width, height, display = False):
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

	def update(self, ball, pallet1):
		if self.display == True:
			self.screen.fill(self.bg_color)
			pygame.draw.rect(self.screen, self.object_color, (pallet1.x, pallet1.y, pallet1.width, pallet1.height))
			pygame.draw.circle(self.screen, self.object_color, (ball.x, ball.y), ball.radius)
			pygame.display.update()
			self.clock.tick(self.fps)

class Pallet():
	def __init__(self, x, screen, some_input):
		self.width = 20
		self.height = 75
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
		self.x = screen.width / 2
		self.y = screen.height / 2
		self.x_speed = 0
		self.y_speed = 0
		self.initial_speed = 10
		self.bounces_on_pallet1 = 0
		self.set_speed()
		self.game_over = False

	def set_speed(self):
		self.x_speed = random.randint(5, 9)
		self.y_speed = int((self.initial_speed ** 2 - self.x_speed ** 2) ** 0.5)

		if random.random() > 0.5:
			self.y_speed = -self.y_speed

	def move(self):
		self.x += self.x_speed
		self.y += self.y_speed

	def bounce(self, screen, pallet1):
		wall_bounce_distance = 50
		if self.y < self.radius + wall_bounce_distance:
			self.y = self.radius + wall_bounce_distance
			self.y_speed = -self.y_speed

		elif self.y > screen.height - self.radius - wall_bounce_distance:
			self.y = screen.height - self.radius - wall_bounce_distance
			self.y_speed = -self.y_speed

		if self.x > screen.width - self.radius:
			self.x_speed = -self.x_speed

		if self.x_speed < 0:
			if abs(self.x - (pallet1.x + pallet1.width)) < self.radius:
				if self.y + self.radius > pallet1.y and self.y - self.radius < pallet1.y + pallet1.height:
					self.x_speed = -self.x_speed
					self.bounces_on_pallet1 += 1
					self.set_speed()

	def is_game_over(self):
		if self.bounces_on_pallet1 >= 100 or self.x + self.radius < 0:
			self.game_over = True

		return self.game_over

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

def calculate_loss(ball, pallet1, screen):
	loss1 = 1 - ball.bounces_on_pallet1/100
	loss = loss1
	return loss

def run_game(neuronal_network, error, display=False):
	screen = Screen(1200, 800, display)
	pallet1 = Pallet(50, screen, Neuronal_Network_Input(neuronal_network))
	ball = Ball(screen)

	while ball.game_over == False:
		pallet1.move(screen, ball)
		ball.move()
		ball.bounce(screen, pallet1)
		screen.update(ball, pallet1)
		ball.is_game_over()

	error.append(calculate_loss(ball, pallet1, screen))

# This is not meant to be executed