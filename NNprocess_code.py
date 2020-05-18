import pickle
import numpy
def process_nn_dict(nn_dict):
	cath_data_list = []

	# These are fields in which the user needs to input a float value (or leave blank)
	float_value_keys = ["Age", "HeightCM", "WeightKG", "ProcOutcomesLMStenosis", 
						"ProcOutcomesLADStenosis", "ProcOutcomesLADDistStenosis", 
						"ProcOutcomesCIRCStenosis", "ProcOutcomesRCAStenosis"]

	count1 = 0
	count2 = 0
	count3 = 0

	print(nn_dict)

	# need to normalize these float_value_keys

	for i, key in enumerate(nn_dict):

		print(i)

		# Column S in CleanData.csv
		if key == "DiabetesTherapy":
			if nn_dict[key] == "":
				cath_data_list.append(-1)
			elif nn_dict[key] == "Diet":
				cath_data_list.append(0)
			elif nn_dict[key] == "Insulin":
				cath_data_list.append(1)
			elif nn_dict[key] == "None":
				cath_data_list.append(2)
			else:
				cath_data_list.append(3)

		# Column T in CleanData.csv
		elif key == "StudyStressSPECTMRIResult":
			if nn_dict[key] == "Indeterminant":
				cath_data_list.append(0)
			elif nn_dict[key] == "Negative":
				cath_data_list.append(1)
			elif nn_dict[key] == "Positive":
				cath_data_list.append(2)
			else:
				cath_data_list.append(3)

		# Column U in CleanData.csv
		elif key == "StudyStressSPECTMRIIschemia":
			if nn_dict[key] == "":
				cath_data_list.append(-1)
			elif nn_dict[key] == "High":
				cath_data_list.append(1)
			elif nn_dict[key] == "Intermediate":
				cath_data_list.append(2)
			elif nn_dict[key] == "Low":
				cath_data_list.append(3)
			else:
				cath_data_list.append(4)

		# Column X in CleanData.csv
		elif key == "Scheduling_Type":
			if nn_dict[key] == "":
				cath_data_list.append(-1)
			elif nn_dict[key] == "Elective":
				cath_data_list.append(0)
			elif nn_dict[key] == "Emergency":
				cath_data_list.append(1)
			else:
				cath_data_list.append(2)

		# Column Y in CleanData.csv
		elif key == "PostDiagRxRecommendation":
			if nn_dict[key] == "":
				cath_data_list.append(-1)
			elif nn_dict[key] == "CABG":
				cath_data_list.append(0)
			elif nn_dict[key] == "Medical Therapy/counseling":
				cath_data_list.append(1)
			elif nn_dict[key] == "None":
				cath_data_list.append(2)
			elif nn_dict[key] == "Other Therapy with CABG or PCI":
				cath_data_list.append(3)
			else:
				cath_data_list.append(4)

		# Column Z in CleanData.csv
		elif key == "CoronaryDominance":
			if nn_dict[key] == "":
				cath_data_list.append(-1)
			elif nn_dict[key] == "Codominant":
				cath_data_list.append(0)
			elif nn_dict[key] == "Left":
				cath_data_list.append(1)
			else:
				cath_data_list.append(2)

		elif key in float_value_keys:
			if nn_dict[key] == "": # left empty
				cath_data_list.append(-1)
				continue

			try:

				float_val = float(nn_dict[key])
				if key == "Age":
					agescaler = pickle.load(open("trained_models/age_scaler.pkl",'rb'))
					float_val = agescaler.transform(numpy.array(nn_dict[key]).reshape(-1,1))[0][0]
					#normalize on the age scaler

				elif key == "HeightCM":
					htscaler = pickle.load(open("trained_models/ht_scaler.pkl",'rb'))
					float_val = htscaler.transform(numpy.array(nn_dict[key]).reshape(-1,1))[0][0]
					#normalize on the height scaler

				elif key == "WeightKG":
					wtscaler = pickle.load(open("trained_models/wt_scaler.pkl",'rb'))
					float_val = wtscaler.transform(numpy.array(nn_dict[key]).reshape(-1,1))[0][0]
					#normalize on the weight scaler

				else:
					float_val /= 100.00 

			except:
				print("Raising float value exception.")
				raise Exception("Form element {} should be a float.".format(key))

			cath_data_list.append(float_val)

		else:
			if nn_dict[key] == "": # left empty
				cath_data_list.append(0)
			elif nn_dict[key] == "No":
				cath_data_list.append(0)
			else:
				cath_data_list.append(1)


	return cath_data_list
