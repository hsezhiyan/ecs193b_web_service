from flask import Flask, render_template, request, url_for, redirect
from sklearn.svm import SVC # for the SVM cath prediction model

from svm_helper import process_svm_dict
from ef_helper import prediction, ef_output_string
from followup_ef_helper import prediction_and_uncertainty, create_output_string
from svm_helper import process_svm_dict
from NNprocess_code import process_nn_dict
from keras.models import model_from_json
import numpy as np

import joblib

app = Flask(__name__, static_url_path='', static_folder='')

@app.route("/", methods=["GET"])
def home():
	return render_template("search_page.html")

@app.route("/ef_page", methods=["GET"])
def ef_page():
    return render_template("ef_model.html")

@app.route("/ef_calc", methods=["GET"])
def ef_calc():
	ef_data = request.args.to_dict()

	try:
		result = prediction(ef_data)
	except Exception as error:
		return str(error)

	return_string = ef_output_string(result)
	return render_template('result_page.html', title='EF Prediction Results',result=return_string)

@app.route("/followup_ef_page", methods=["GET"])
def followup_ef_page():
	return render_template("f_ef_model.html")

@app.route("/followup_ef_calc", methods=["GET"])
def followup_ef_calc():
	ef_data = request.args.to_dict()

	try:
		mean, variance = prediction_and_uncertainty(ef_data)
	except Exception as error:
		return str(error)

	return_string = create_output_string(mean, variance)
	return render_template('result_page.html', title='Follow Up EF Prediction Results',result=return_string)

@app.route("/NN_cath_page", methods=["GET"])
def NN_cath_page():
	return render_template("NN_model.html")

@app.route("/NN_cath_calc", methods=["GET"])
def NN_cath_calc():

	# load json and create model
	json_file = open('trained_models/Cath_NNmodel.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model.load_weights("trained_models/CathNNwts.h5")

	print("Loaded model from disk")

	cath_data = request.args.to_dict()

	try:
		cath_data_list = process_nn_dict(cath_data)
	except Exception as error:
		return str(error)

	# print(cath_data_list)

	# cath_data_list = []
	# for key in cath_data:
	# 	try:
	# 		float(cath_data[key])
	# 		float_bool = True
	# 	except:
	# 		float_bool = False

	# 	if float_bool:
	# 		cath_data_list.append(float(cath_data[key]))
	# 	elif cath_data[key] == "":
	# 		cath_data_list.append(-1)

	# should be 1
	# cath_data_list = [66, 1, 1, 0, 0,  0, 0,	0,	0,	175.0,	87.6,	0,	1,	0,	0,	0,	-1,	2,	2,	1,	1,	2,	4,	1,	0,	0.0,	0,	0.0,	0,	0.5,	0,	0.9,	0,	0.0,	1,	1,	1,	1,	1,	1]

	# should be 0
	# cath_data_list = [63,	0,	1,	1,	0,	0,	1,	0,	0,	188.0,	71.0,	0,	0,	0,	0,	0,	-1,	1,	-1,	1,	0,	2,	1,	2,	0,	0.0,	0,	0.0,	0,	0.0,	0,	0.0,	0,	0.0,	1,	1,	1,	1,	1,	1]

	cath_data_list = np.array(cath_data_list)
	cath_prediction = loaded_model.predict(np.array([cath_data_list]))[0][0]
	return_string = f"Cath result is {cath_prediction}"
	return render_template('result_page.html', title='Neural Network Prediction Results',result=return_string)

@app.route("/svm_cath_page", methods=["GET"])
def svm_cath_page():
	return render_template("svm_model.html")

@app.route("/svm_cath_calc", methods=["GET"])
def svm_cath_calc():

	loaded_model = joblib.load("trained_models/svm_cath.sav")
	cath_data = request.args.to_dict()

	try:
		cath_data_list = process_svm_dict(cath_data)
	except Exception as error:
		return str(error)

	# print(cath_data_list)

	# cath_data_list = []
	# for key in cath_data:
	# 	try:
	# 		float(cath_data[key])
	# 		float_bool = True
	# 	except:
	# 		float_bool = False

	# 	if float_bool:
	# 		cath_data_list.append(float(cath_data[key]))
	# 	elif cath_data[key] == "":
	# 		cath_data_list.append(-1)

	# should be 1
	# cath_data_list = [66, 1, 1, 0, 0,  0, 0,	0,	0,	175.0,	87.6,	0,	1,	0,	0,	0,	-1,	2,	2,	1,	1,	2,	4,	1,	0,	0.0,	0,	0.0,	0,	0.5,	0,	0.9,	0,	0.0,	1,	1,	1,	1,	1,	1]

	# should be 0
	# cath_data_list = [63,	0,	1,	1,	0,	0,	1,	0,	0,	188.0,	71.0,	0,	0,	0,	0,	0,	-1,	1,	-1,	1,	0,	2,	1,	2,	0,	0.0,	0,	0.0,	0,	0.0,	0,	0.0,	0,	0.0,	1,	1,	1,	1,	1,	1]

	cath_prediction = loaded_model.predict([cath_data_list])
	return_string = f"Cath result is {cath_prediction}"
	return render_template('result_page.html', title='SVM Prediction Results',result=return_string)

if __name__ == "__main__":
	app.run()
