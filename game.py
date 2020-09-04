import pygame
import random
import time
import numpy as np
import sys

height, width = 600, 600
block_size = 15
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

class Snake:
	def __init__(self):
		self.reset()
		self.color = (0, 255, 15)

	def reset(self):
		self.score = 0
		self.length = 1
		self.positions = [((width / 2), (height / 4))]
		self.direction = random.choice([up, right, down, left])

	def get_head_pos(self):
		return self.positions[0]

	def move(self):
		head_pos = self.get_head_pos()
		x, y = self.direction
		new_head_pos = ((head_pos[0] + x*block_size), (head_pos[1] + y*block_size))
		#check for body collision
		if len(self.positions) > 2 and new_head_pos in self.positions[2:]:
			self.reset()
		else:
			self.positions.insert(0, new_head_pos)
			#since head is moving forward, tail moving backward so pop the last value
			if len(self.positions) > self.length:
				self.positions.pop()

	def controls(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					self.turn(up)
				elif event.key == pygame.K_DOWN:
					self.turn(down)
				elif event.key == pygame.K_LEFT:
					self.turn(left)
				elif event.key == pygame.K_RIGHT:
					self.turn(right)
				elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
					pygame.quit()
					sys.exit()
			elif event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

	def turn(self, direction):
		if self.direction != direction:
			self.direction = direction

	def draw(self, surface):
		for pos in self.positions:
			snake_block = pygame.Rect((pos[0], pos[1]), (block_size, block_size))
			pygame.draw.rect(surface, self.color, snake_block)


class Food:
	def __init__(self):
		self.position = (0, 0)
		self.color = (255, 0, 0)
		self.generate_food_position()

	def generate_food_position(self):
		self.position = (random.randint(0, width-1), random.randint(0, height-1))

	def draw(self, surface):
		food = pygame.Rect((self.position[0], self.position[1]), (block_size, block_size))
		pygame.draw.rect(surface, self.color, food)


if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((width, height))
	surface = pygame.Surface(screen.get_size())
	surface = surface.convert()
	clock = pygame.time.Clock()

	snake = Snake()
	food = Food()

	while True:
		clock.tick(50)
		snake.controls()
		snake.move()
		if snake.get_head_pos() == food.position:
			snake.length += 1
			snake.score += 1
			food.generate_food_position()
		
		snake.draw(surface)
		food.draw(surface)
		screen.blit(surface, (0, 0))
		pygame.display.update()