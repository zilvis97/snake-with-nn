from game import *
import h5py
import tensorflow as tf
import tensorflow.compat.v1 as compat
from tensorflow import keras
from keras.models import load_model, model_from_json


# config = tf.compat.v1.ConfigProto()
# config.gpu_options.allow_growth = True
# config.log_device_placement = True
# sess = compat.Session(config=config)
# compat.keras.backend.set_session(sess)

def test_game(model, display, clock):
	max_score = 0
	avg_score = 0
	games = 10
	max_steps = 1000

	for i in tqdm(range(games)):
		snake = Snake()
		score = 0

		while snake.moves and not snake.dead:
		# for _ in range(max_steps):
			angle_with_apple, apple_direction_vector_normalized, snake_direction_vector_normalized = snake.get_angle_with_apple()
			turn_direction, turn_direction_vector = snake.generate_direction(angle_with_apple)
			current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = snake.blocked_directions()

			data = [score, is_left_blocked, is_front_blocked, is_right_blocked, \
				apple_direction_vector_normalized[0], apple_direction_vector_normalized[1], \
				snake_direction_vector_normalized[0], snake_direction_vector_normalized[1]]

			input_data = np.array(data).reshape(-1, 8)
			prediction = model.predict(input_data)
			predicted_direction = np.argmax(prediction) - 1

			new_dir = current_direction_vector
			_, predicted_turn_direction = snake.direction_vector(predicted_direction)


			snake = snake.play_game(predicted_turn_direction, display, clock)
			# if snake.dead:
			# 	break

		score = snake.score
		max_score = max(score, max_score)
		avg_score += score
		print("Average score so far: {}".format(avg_score / (i+1)))

	return max_score, avg_score / games



json_file = open('model.json', 'r')
loaded_json_model = json_file.read()
json_file.close()
model = model_from_json(loaded_json_model)
model.load_weights('model.h5')

print(model.summary())
train_x, train_y = [], []

with open("data_x.txt", 'r') as data_x:
	for line in data_x:
		res = line.strip('][\n').split(', ')
		train_x.append(res)

with open("data_y.txt", 'r') as data_y:
	for line in data_y:
		res = line.strip('][\n').split(', ')
		train_y.append(res)

height, width = 600, 600
line_width = 5

pygame.init()
display = pygame.display.set_mode((width+line_width, height+line_width), 0, 32)
clock = pygame.time.Clock()

max_score, avg_score = test_game(model, display, clock)
print("Maximum score achieved is:  ", max_score)
print("Average score achieved is:  ", avg_score)