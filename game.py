import pygame
import random
import time
import numpy as np
import sys
import math
from tqdm import tqdm	# for showing the progress bar

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
white = (255, 255, 255)
black = (0, 0, 0)

class Snake:
	def __init__(self):
		self.reset()
		self.moves = 1000
		self.color = (0, 255, 15)
		self.dead = False
		self.reward = 20

	def reset(self):
		self.dead = False
		self.score = 0
		self.length = 3
		self.direction = random.choice([up, right, down, left])
		x = height / 2
		y = width / 2
		self.positions = []
		for i in range(3):
			point = ((x + i*block_size), y)
			self.positions.insert(0, point)
		# self.positions = [((width / 2), (height / 2))]
		# self.positions.append((self.positions[0][0] - (self.direction[0] * block_size), self.positions[0][1] - (self.direction[1] * block_size)))
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
			self.dead = True
		#check for out of bounds
		elif self.colided_with_wall(new_head_pos):
			self.dead = True
		else:
			if new_head_pos == self.food:
				self.score += 1
				self.length += 1
				self.moves += self.reward
				self.generate_food()
			self.positions.insert(0, new_head_pos)
			#since head is moving forward, tail moving backward so pop the last value
			if len(self.positions) > self.length:
				self.positions.pop()
			# self.score += 1


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
			self.moves -= 1
			self.direction = direction


	def current_direction_vector(self):
		return np.array(self.positions[0]) - np.array(self.positions[1])

	def turn_left_vector(self, current_direction_vector):
		return np.array([current_direction_vector[1], -current_direction_vector[0]])

	def turn_right_vector(self, current_direction_vector):
		return np.array([-current_direction_vector[1], current_direction_vector[0]])

	def is_direction_blocked(self, current_direction_vector):
		current_head = self.get_head_pos()
		new_head_pos = (current_head[0]+current_direction_vector[0], current_head[1]+current_direction_vector[1])
		if self.colided_with_body(new_head_pos) or self.colided_with_wall(new_head_pos):
			return 1	
		return 0

	def blocked_directions(self):
		current_direction_vector = self.current_direction_vector()
		is_front_blocked = self.is_direction_blocked(current_direction_vector)
		is_left_blocked = self.is_direction_blocked(self.turn_left_vector(current_direction_vector))
		is_right_blocked = self.is_direction_blocked(self.turn_right_vector(current_direction_vector))

		return current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked

	def food_distance_from_snake(self):
		food_pos = self.food
		head_pos = self.get_head_pos()
		return np.linalg.norm(np.array(food_pos) - np.array(head_pos))

	#if angle > 0; move right, if angle < 0 move left, if angle == 0, keep straight
	def get_angle_with_apple(self):
		# angle = math.atan2(self.food[1] - self.positions[0][1], self.food[0] - self.positions[0][0]) / math.pi
		apple_direction_vector = np.array(self.food) - np.array(self.get_head_pos())
		snake_direction_vector = self.current_direction_vector()

		norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector) 
		norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)

		#to avoid division from 0 when apple is in [0, 0]
		norm_of_apple_direction_vector = norm_of_apple_direction_vector if norm_of_apple_direction_vector != 0 else 1

		apple_direction_vector_normalized = apple_direction_vector / norm_of_apple_direction_vector
		snake_direction_vector_normalized = snake_direction_vector / norm_of_snake_direction_vector

		angle = math.atan2(apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0] - apple_direction_vector_normalized[0] * snake_direction_vector_normalized[1], 
			apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1] + apple_direction_vector_normalized[0] * snake_direction_vector_normalized[0]) / math.pi

		return angle, apple_direction_vector_normalized, snake_direction_vector_normalized

	#go towards apple
	def generate_direction(self, angle_with_apple):
		# print(angle_with_apple)
		direction = 0 	# keep going straight
		if angle_with_apple > 0:	# turn left
			direction = 1
		elif angle_with_apple < 0:	# turn righ
			direction = -1

		return self.direction_vector(direction)

	def direction_vector(self, direction):
		current_direction_vector = self.current_direction_vector()
		new_direction = current_direction_vector 	#keep going straight
		if direction == -1:
			new_direction = self.turn_left_vector(current_direction_vector)
		elif direction == 1:
			new_direction = self.turn_right_vector(current_direction_vector)

		turn_direction = self.generate_turn_direction(new_direction)
		return direction, turn_direction

	# which direction to make a turn / press button
	def generate_turn_direction(self, turn_direction):
		turn = 0
		if turn_direction.tolist() == [block_size, 0]:
			turn = right
		elif turn_direction.tolist() == [-block_size, 0]:
			turn = left
		elif turn_direction.tolist() == [0, block_size]:
			turn = down
		else:
			turn = up

		return turn


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


	def play_game(self, turn_direction_vector, display, clock, clock_tick = 100000):
		while not self.dead:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			display.fill(black)
			self.draw_food(display) #jei neveiks tada bandyt pygame.Surface(display.get_size())
			self.draw(display)		# draw snake

			self.turn(turn_direction_vector)
			self.move()

			pygame.display.set_caption("Score: " + str(self.score))
			pygame.display.update()
			clock.tick(clock_tick)

			return self
		return self


def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont('monospace', size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_border(surface, color, line_width):
	pygame.draw.rect(surface, border_color, [0, 0, width, line_width])
	pygame.draw.rect(surface, border_color, [0, height, width, line_width])
	pygame.draw.rect(surface, border_color, [0, 0, line_width, height])
	pygame.draw.rect(surface, border_color, [width, 0, line_width, height + line_width])

# def play_game(snake, turn_direction_vector, display, clock):
# 	crashed = False
# 	while not snake.dead:
# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT:
# 				snake.dead = True

# 		display.fill(black)
# 		snake.draw_food(display) #jei neveiks tada bandyt pygame.Surface(display.get_size())
# 		snake.draw(display)		# draw snake

# 		snake.turn(turn_direction_vector)
# 		snake.move()

# 		pygame.display.set_caption("Score: " + str(snake.score))
# 		pygame.display.update()
# 		clock.tick(50000)

# 		return snake

# if __name__ == "__main__":
# 	pygame.init()
# 	screen = pygame.display.set_mode((width+line_width, height+line_width), 0, 32)
# 	surface = pygame.Surface(screen.get_size())
# 	#surface = surface.convert()
# 	# font = pygame.font.SysFont("monospace", 30)
# 	clock = pygame.time.Clock()

# 	snake = Snake()

# 	while True:
# 		surface.fill(black)
# 		draw_border(surface, border_color, line_width)

# 		clock.tick(10)
# 		snake.controls()
# 		snake.move()

# 		if snake.dead:
# 			draw_text("Game Over\nScore: {}".format(snake.score), 30, white, 50, height/2)
# 			pygame.display.update()
# 			pygame.time.delay(1500)
# 			snake.reset()
# 			snake.generate_food()
# 			pygame.display.update()
# 			continue
		
# 		# if snake.get_head_pos() == snake.food:
# 		# 	snake.length += 1
# 		# 	snake.score += snake.reward
# 		# 	snake.generate_food()

# 		snake.draw(surface)
# 		snake.draw_food(surface)
# 		screen.blit(surface, (0, 0))
# 		draw_text("Score {}".format(snake.score), 30, white, 5, 10)

# 		pygame.display.update()
