import tensorflow as tf
import keras
from keras import backend as K
from keras.optimizers import Adam
from keras.layers import Dense
#from keras.models import load_model

import numpy as np

already_loaded = False
loaded_model = None

def mse_loss(y_actual, y_pred):
	return K.mean(K.square(y_pred - y_actual))

def load_model():
    adam = Adam(lr = 0.002, beta_1 = 0.9, beta_2 = 0.999) # a hyperparameter
    # load weights into new model
    model = tf.keras.models.load_model('trained_models/EFmodel.h5')
    print("weights loaded")
    #loaded_model.compile(loss=mse_loss, optimizer=adam, metrics=[mse_loss])
    point_five = model.predict(np.zeros((1, 5)))
    print(point_five)

    return model

def prediction(ef_dict):

    # raw prediction (without any dropout)
    ef_data_list = process_ef_dict(ef_dict)

    # ef_data_list = [0.14,	0.68,	0.66,	0.251869,	0.104164,	0.0272109]
    # ef_data_list = [0.212,	0.486,	0.407,	0.188189,	0.128489,	0.523256]

    global already_loaded
    global loaded_model
    print("loading model")
    if already_loaded is False:
        already_loaded = True
        loaded_model = load_model()
    print("model loaded")
    loaded_model.summary()
    print(ef_data_list)
    prediction = loaded_model.predict([[ef_data_list]])
    print(prediction)
    return prediction[0]

def ef_output_string(pred):

	if pred < 0.35:
		lethality = "LETHAL"
	else:
		lethality = "NOT LETHAL"

	output_string = """The predicted followup EF is {}, which is {}.""".format(pred, lethality)
	return output_string

def process_ef_dict(ef_dict):

	ef_data_list = []

	for i, key in enumerate(ef_dict):

		if ef_dict[key] == "": # left empty
			ef_data_list.append(0.0)
			continue
		else:
			try:
				float_val = float(ef_dict[key])
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




