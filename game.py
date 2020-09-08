import pygame
import random
import time
import numpy as np
import sys

height, width = 600, 600
block_size = 20
num_blocks = height / block_size
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)
line_width = 5
border_color = (200, 0, 100)
food_color = (255, 0, 0)

class Snake:
	def __init__(self):
		self.reset()
		self.color = (0, 255, 15)
		self.dead = False
		self.reward = 10

	def reset(self):
		self.dead = False
		self.score = 0
		self.length = 2
		self.positions = [((width / 2), (height / 2))]
		self.direction = random.choice([up, right, down, left])
		self.generate_food()

	def get_head_pos(self):
		return self.positions[0]

	def colided_with_body(self, new_head_pos):
		return len(self.positions) > 2 and new_head_pos in self.positions[1:]

	def colided_with_wall(self, new_head_pos):
		return new_head_pos[0] < 0 or new_head_pos[0] >= width or new_head_pos[1] < 0 or new_head_pos[1] >= height

	def move(self):
		head_pos = self.get_head_pos()
		x, y = self.direction
		new_head_pos = ((head_pos[0] + (x * block_size)), (head_pos[1] + (y * block_size)))
		#check for body collision
		if self.colided_with_body(new_head_pos):
			print("Game over")	
			self.dead = True
		#check for out of bounds
		elif self.colided_with_wall(new_head_pos):
			print("Game over")
			self.dead = True
		else:
			self.positions.insert(0, new_head_pos)
			#since head is moving forward, tail moving backward so pop the last value
			if len(self.positions) > self.length:
				self.positions.pop()
			self.score += 1

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
		#if selection direction is opposite of current moving directon
		if self.direction == (direction[0] * -1, direction[1] * -1):
			return
		else:
			self.direction = direction


	def current_direction_vector(self):
		return np.array(self.positions[0]) - np.array(self.positions[1])

	def turn_left_vector(self, current_direction_vector):
		return np.array([-current_direction_vector[1], current_direction_vector[0]])

	def turn_right_vector(self, current_direction_vector):
		return np.array([current_direction_vector[1], -current_direction_vector[0]])

	def is_direction_blocked(self, current_direction_vector):
		new_head_pos = self.get_head_pos() + current_direction_vector
		if self.colided_with_body(new_head_pos) or self.colided_with_wall(new_head_pos):
			return 1	
		return 0

	def blocked_directions(self):
		current_direction_vector = self.self.current_direction_vector()
		is_front_blocked = self.is_direction_blocked(current_direction_vector)
		is_left_blocked = self.is_direction_blocked(current_direction_vector)
		is_right_blocked = self.is_direction_blocked(current_direction_vector)

		return is_front_blocked, is_left_blocked, is_right_blocked

	def food_distance_from_snake(food_pos, snake_head_pos):
		return np.linalg.norm(np.array(food_pos) - np.array(snake_head_pos))




	def draw(self, surface):
		for pos in self.positions:
			snake_block = pygame.Rect((pos[0], pos[1]), (block_size, block_size))
			pygame.draw.rect(surface, self.color, snake_block)


	def generate_food(self):
		food = []
		while food == []:
			food = (random.randint(0, num_blocks-1) * block_size, random.randint(0, num_blocks-1) * block_size)
			if food in self.positions:
				food = []
		self.food = food

	def draw_food(self, surface):
		food = pygame.Rect((self.food[0], self.food[1]), (block_size, block_size))
		pygame.draw.rect(surface, food_color, food)




def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont('monospace', size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_border(surface, color, line_width):
	pygame.draw.rect(surface, border_color, [0, 0, width, line_width])
	pygame.draw.rect(surface, border_color, [0, height, width, line_width])
	pygame.draw.rect(surface, border_color, [0, 0, line_width, height])
	pygame.draw.rect(surface, border_color, [width, 0, line_width, height + line_width])


if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((width+line_width, height+line_width), 0, 32)
	surface = pygame.Surface(screen.get_size())
	#surface = surface.convert()

	# font = pygame.font.SysFont("monospace", 30)
	clock = pygame.time.Clock()

	snake = Snake()

	while True:
		surface.fill((0, 0, 0)) #fill black
		draw_border(surface, border_color, line_width)

		clock.tick(10)
		snake.controls()
		snake.move()

		if snake.dead:
			draw_text("Game Over\nScore: {}".format(snake.score), 30, (255, 255, 255), width/2, height/2)
			pygame.time.delay(1500)
			snake.reset()
			food.generate_food_position()
			continue
		
		if snake.get_head_pos() == snake.food:
			snake.length += 1
			snake.score += snake.reward
			snake.generate_food()

		snake.draw(surface)
		snake.draw_food(surface)
		screen.blit(surface, (0, 0))
		draw_text("Score {}".format(snake.score), 30, (255, 255, 255), 5, 10)

		pygame.display.update()
