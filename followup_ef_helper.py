import keras
from keras import backend as K
from keras.optimizers import Adam
from keras.layers import Dense, Dropout

import numpy as np

already_loaded = False
loaded_model = None

def mse_loss(y_actual, y_pred):
	return K.mean(K.square(y_pred - y_actual))

class StochasticModel(keras.Model):
  def __init__(self):
    super(StochasticModel, self).__init__()

    self.layer_1 = Dense(100, activation='relu')
    self.dropout_1 = Dropout(0.5)

    self.layer_2 = Dense(50, activation='relu')
    self.dropout_2 = Dropout(0.5)
    
    self.layer_3 = Dense(10, activation='relu')
    self.dropout_3 = Dropout(0.5)

    self.output_layer = Dense(1, activation='sigmoid')
  
  def call(self, x):
    x = self.layer_1(x)
    x = self.dropout_1(x, training=True)

    x = self.layer_2(x)
    x = self.dropout_2(x, training=True)

    x = self.layer_3(x)
    x = self.dropout_3(x, training=True)

    output = self.output_layer(x)

    return output

def load_model():
	adam = Adam(lr = 0.002, beta_1 = 0.9, beta_2 = 0.999) # a hyperparameter

	loaded_model = StochasticModel()
	loaded_model.compile(loss=mse_loss, optimizer=adam, metrics=[mse_loss])
	point_five = loaded_model.predict(np.zeros((1, 6)))

	loaded_model.load_weights('trained_models/stochastic_model_weights.tf')

	return loaded_model

def prediction_and_uncertainty(followup_ef_dict):
	
	# raw prediction (without any dropout)
	ef_data_list = process_followup_ef_dict(followup_ef_dict)

	# ef_data_list = [0.14,	0.68,	0.66,	0.251869,	0.104164,	0.0272109]
	# ef_data_list = [0.212,	0.486,	0.407,	0.188189,	0.128489,	0.523256]

	print(ef_data_list)

	global already_loaded
	global loaded_model

	predictions = []
	N = 20	

	if already_loaded is False:
		already_loaded = True
		loaded_model = load_model()

	for i in range(N):
		prediction = loaded_model.predict([[ef_data_list]])
		predictions.append(prediction)

	return np.mean(predictions), np.var(predictions)

def create_output_string(mean, variance):

	if mean < 0.35:
		lethality = "LETHAL"
		if variance > 0.006:
			uncertainty = "Very trustable"
		else:
			uncertainty = "Uncertain"
	else:
		lethality = "NOT LETHAL"
		if variance > 0.006:
			uncertainty = "Very trustable"
		elif variance < 0.002:
			unceratinty = "Very untrustable"
		else:
			uncertainty = "Uncertain"

	output_string = """The predicted followup EF is {}, which is {}. 
					The uncertainty is {}, classifed as {}""".format(mean, lethality, variance, uncertainty)
	return output_string

def process_followup_ef_dict(followup_ef_dict):

	ef_data_list = []

	for i, key in enumerate(followup_ef_dict):

		if followup_ef_dict[key] == "": # left empty
			ef_data_list.append(0.0)
			continue
		else:
			try:
				float_val = float(followup_ef_dict[key])
			except:
				print("Raising float value exception.")
				raise Exception("Form element {} should be a float.".format(key))

		if key  == 'IVS d, 2D':
			float_val = float_val / 5.0
		elif key == 'LV d, 2D':
			float_val = float_val / 10.0
		elif key == 'LV s, 2D':
			float_val = float_val / 10.0
		elif key == 'RVSP (TR)':
			float_val = float_val / 125.0
		elif key == 'LA Vol A/L Volume':
			float_val = float_val / 200.0
		else:
			float_val = float_val / 100.0

		ef_data_list.append(float_val)

	return ef_data_list




