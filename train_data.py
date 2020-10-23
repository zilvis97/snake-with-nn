# https://towardsdatascience.com/today-im-going-to-talk-about-a-small-practical-example-of-using-neural-networks-training-one-to-6b2cbd6efdb3
# ideas

from game import *

def generate_training_data(display, clock):
	max_score = 0
	avg_score = 0
	training_data_x = []
	training_data_y = [] 	# of strudture [left, front, right]
	games = 200
	max_steps = 2000

	for i in tqdm(range(games)):
		snake = Snake()
		score = snake.score
		# distance_to_apple = food_distance_from_snake(snake.food, snake.get_head_pos())

		while snake.moves and not snake.dead:
		# for _ in range(max_steps):
			angle_with_apple, apple_direction_vector_normalized, snake_direction_vector_normalized = snake.get_angle_with_apple()
			turn_direction, turn_direction_vector = snake.generate_direction(angle_with_apple)	# direction that should be turned next based on apple position
			current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = snake.blocked_directions()

			turn_direction, turn_direction_vector, training_data_y = generate_training_data_y(snake, turn_direction, turn_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked, training_data_y)

			if is_right_blocked and is_left_blocked and is_front_blocked:
				break

			training_data_x.append([score,
				is_left_blocked, is_front_blocked, is_right_blocked, apple_direction_vector_normalized[0], apple_direction_vector_normalized[1], \
				snake_direction_vector_normalized[0], snake_direction_vector_normalized[1]])
			snake = snake.play_game(turn_direction_vector, display, clock)
		score = snake.score
		print("LENGTH = {}, SCORE = {}".format(snake.length, score))
		max_score = max(score, max_score)
		avg_score += score
		print("Avg score so far: {}".format(avg_score / (i+1)))
	print("Final average score: {}".format(avg_score / games))

	return training_data_x, training_data_y



def generate_training_data_y(snake, turn_direction, turn_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked, training_data_y):
	# if should turn to the left
	if turn_direction == -1:
		if is_left_blocked:
			if is_front_blocked and not is_right_blocked:
				turn_direction, turn_direction_vector = snake.direction_vector(1)
				training_data_y.append([0, 0, 1])
			elif not is_front_blocked and is_right_blocked:
				turn_direction, turn_direction_vector = snake.direction_vector(0)
				training_data_y.append([0, 1, 0])
			elif not is_front_blocked and not is_right_blocked:
				turn_direction, turn_direction_vector = snake.direction_vector(1)
				training_data_y.append([0, 0, 1])
		else:
			training_data_y.append([1, 0, 0]) #turn left if left is available

	elif turn_direction == 0:
		if is_front_blocked:
			if is_left_blocked and not is_right_blocked:
				turn_direction, turn_direction_vector = snake.direction_vector(1)
				training_data_y.append([0, 0, 1])
			elif not is_left_blocked and is_right_blocked:
				turn_direction, turn_direction_vector = snake.direction_vector(-1)
				training_data_y.append([1, 0, 0])
			elif not is_left_blocked and not is_right_blocked:
				turn_direction, turn_direction_vector = snake.direction_vector(1)
				training_data_y.append([0, 0, 1])	
		else:
			training_data_y.append([0, 1, 0])				

	elif turn_direction == 1:
		if is_right_blocked:
			if is_front_blocked and not is_left_blocked:
				turn_direction, turn_direction_vector = snake.direction_vector(-1)
				training_data_y.append([1, 0, 0])
			elif not is_front_blocked and is_left_blocked:
				turn_direction, turn_direction_vector = snake.direction_vector(0)
				training_data_y.append([0, 1, 0])
			elif not is_front_blocked and not is_left_blocked:
				turn_direction, turn_direction_vector = snake.direction_vector(-1)
				training_data_y.append([1, 0, 0])
		else:
			training_data_y.append([0, 0, 1])

	return turn_direction, turn_direction_vector, training_data_y