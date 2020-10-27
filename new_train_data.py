# https://towardsdatascience.com/today-im-going-to-talk-about-a-small-practical-example-of-using-neural-networks-training-one-to-6b2cbd6efdb3
# ideas

from game import *
from random import randint

def generate_training_data(display, clock):
	max_score = 0
	avg_score = 0
	training_data_x = []
	training_data_y = [] 	# of strudture [left, front, right]
	games = 5000
	max_steps = 2000

	for i in tqdm(range(games)):
		snake = Snake()
		score = snake.score

		while snake.moves and not snake.dead:
			random_action = generate_random_action()
			initial_distance_to_apple = snake.food_distance_from_snake()
			angle_with_apple, apple_direction_vector_normalized, snake_direction_vector_normalized = snake.get_angle_with_apple()
			turn_direction, turn_direction_vector = snake.direction_vector(random_action)
			current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = snake.blocked_directions()

			snake = snake.play_game(turn_direction_vector, display, clock)

			# new input training data sample
			training_data_x.append([is_left_blocked, is_front_blocked, is_right_blocked, angle_with_apple, turn_direction])

			distance_to_apple = snake.food_distance_from_snake()
			if snake.dead or snake.moves == 0 or (is_right_blocked and is_front_blocked and is_left_blocked):
				training_data_y.append([-1])
			else:
				if distance_to_apple < initial_distance_to_apple or snake.score > score:
					training_data_y.append([1])
				else:
					training_data_y.append([0])

			score = snake.score

		# print("LENGTH = {}, SCORE = {}".format(snake.length, score))
		max_score = max(score, max_score)
		avg_score += score
		print("Avg score so far: {}".format(avg_score / (i+1)))
	print("Final average score: {}".format(avg_score / games))

	return training_data_x, training_data_y


def generate_random_action():
	action = randint(0, 2) - 1
	return action