from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf
import tensorflow.compat.v1 as compat
from game import *
# from train_data import generate_training_data
from new_train_data import *

sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(
      allow_soft_placement=True, log_device_placement=True))


height, width = 600, 600
line_width = 5

def get_training_data():
	training_data_x = np.genfromtxt("data_x.txt", delimiter=',][', dtype=str)
	data_x = []
	for x in training_data_x:
		data_x.append(np.array(x.strip('][').replace(",", "").split()).astype(float).tolist())

	training_data_y = np.genfromtxt("data_y.txt", delimiter=',][', dtype=str)
	data_y = []
	for y in training_data_y:
		data_y.append(np.array(y.strip('][').split()).astype(int).tolist())

	data_x = np.array(data_x).reshape(-1, 5)
	data_y = np.array(data_y).reshape(-1, 1)

	return data_x, data_y

def save_training_data(filename, data):
	with open(filename, 'w') as file:
		for line in data:
			file.write("{}\n".format(line))


# pygame.init()
# display = pygame.display.set_mode((width+line_width, height+line_width), 0, 32)
# clock = pygame.time.Clock()

# data_x, data_y = generate_training_data(display, clock)
# save_training_data('data_x.txt', data_x)
# save_training_data('data_y.txt', data_y)


# get training data from file
data_x, data_y = get_training_data()

model = Sequential([
		Dense(9, activation='sigmoid', input_dim=5, name='layer1'),
		Dense(16, activation='relu', name='layer2'),
		Dense(23, activation='relu', name='layer3'),
		Dense(1, activation='linear', name='layer4')	# changed from 3 layers into 1 and from softmax to sigmoid
	])
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.fit(x=np.array(data_x), y=np.array(data_y), batch_size=256, epochs=3)


model.save_weights('model.h5')
# save model in JOSN file
model_json = model.to_json()
with open('model.json', 'w') as json_file:
	json_file.write(model_json)