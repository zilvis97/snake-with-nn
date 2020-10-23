from keras.models import Sequential
from keras.layers import Dense

from game import *
from train_data import generate_training_data

height, width = 600, 600
line_width = 5

pygame.init()
display = pygame.display.set_mode((width+line_width, height+line_width), 0, 32)
clock = pygame.time.Clock()

training_data_x, training_data_y = generate_training_data(display, clock)

model = Sequential([
		Dense(9, input_dim=8, name='layer1'),
		Dense(15, activation='relu', name='layer2'),
		Dense(3, activation='softmax', name='layer3')
	])
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.fit(x=np.array(training_data_x), y=np.array(training_data_y), batch_size=128, epochs=5)


model.save_weights('model.h5')
# save model in JOSN file
model_json = model.to_json()
with open('model.json', 'w') as json_file:
	json_file.write(model_json)

with open("data_y.txt", "w") as data:
	for line in training_data_y:
		data.write("{}\n".format(line))

with open("data_x.txt", "w") as data:
	for line in training_data_x:
		data.writelines("{}\n".format(line))

