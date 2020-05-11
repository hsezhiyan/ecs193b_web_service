from flask import Flask, render_template, request, url_for, redirect
from sklearn.svm import SVC # for the SVM cath prediction model

import joblib 

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
	return render_template("search_page.html")

@app.route("/svm_cath_page", methods=["GET"])
def svm_cath_page():
	return render_template("svm_cath.html")

@app.route("/svm_cath_calc", methods=["GET"])
def svm_cath_calc():
	loaded_model = joblib.load("svm_cath.sav")
	cath_data = request.args.to_dict()

	print(cath_data)

	cath_data_list = []
	for key in cath_data:
		try:
			float(cath_data[key])
			float_bool = True
		except:
			float_bool = False

		if float_bool:
			cath_data_list.append(float(cath_data[key]))
		elif cath_data[key] == "":
			cath_data_list.append(-1)

	print((cath_data_list))
	cath_prediction = loaded_model.predict([cath_data_list])
	return_string = f"Cath result is {cath_prediction}"
	return return_string

if __name__ == "__main__":
	app.run()