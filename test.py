from game import *
import tensorflow as tf
import tensorflow.compat.v1 as compat
from tensorflow import keras
from keras.models import load_model, model_from_json

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
config.log_device_placement = True
sess = compat.Session(config=config)
compat.keras.backend.set_session(sess)

sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(
      allow_soft_placement=True, log_device_placement=True))


def test_game(model, display, clock):
	max_score = 0
	avg_score = 0
	games = 10
	max_steps = 1000

	for i in tqdm(range(games)):
		snake = Snake()
		score = 0

		while snake.moves and not snake.dead:
			angle_with_apple, apple_direction_vector_normalized, snake_direction_vector_normalized = snake.get_angle_with_apple()
			# turn_direction, turn_direction_vector = snake.generate_direction(angle_with_apple)
			current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = snake.blocked_directions()

			data = [is_left_blocked, is_front_blocked, is_right_blocked, angle_with_apple]

			predictions = []
			# try out all the possible actions [left, straight, right] and choose one with the highest possiblity
			for action in range(-1, 2):
				prediction_data = np.array(data + [action]).reshape(-1, 5)
				predictions.append(model.predict(prediction_data))
			action = np.argmax(predictions)
			turn_action = action - 1

			_, predicted_turn_direction = snake.direction_vector(turn_action)
			snake = snake.play_game(predicted_turn_direction, display, clock, 1000)
			
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
# train_x, train_y = get_train_data()
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

height, width = 600, 600
line_width = 5

pygame.init()
display = pygame.display.set_mode((width+line_width, height+line_width), 0, 32)
clock = pygame.time.Clock()

max_score, avg_score = test_game(model, display, clock)
print("Maximum score achieved is:  ", max_score)
print("Average score achieved is:  ", avg_score)