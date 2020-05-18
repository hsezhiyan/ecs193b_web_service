
def process_svm_dict(svm_dict):
	cath_data_list = []

	# These are fields in which the user needs to input a float value (or leave blank)
	float_value_keys = ["Age", "HeightCM", "WeightKG", "ProcOutcomesLMStenosis", 
						"ProcOutcomesLADStenosis", "ProcOutcomesLADDistStenosis", 
						"ProcOutcomesCIRCStenosis", "ProcOutcomesRCAStenosis"]

	for i, key in enumerate(svm_dict):

		# Column S in CleanData.csv
		if key == "DiabetesTherapy":
			if svm_dict[key] == "":
				cath_data_list.append(-1)
			elif svm_dict[key] == "Diet":
				cath_data_list.append(0)
			elif svm_dict[key] == "Insulin":
				cath_data_list.append(1)
			elif svm_dict[key] == "None":
				cath_data_list.append(2)
			else:
				cath_data_list.append(3)

		# Column T in CleanData.csv
		elif key == "StudyStressSPECTMRIResult":
			if svm_dict[key] == "Indeterminant":
				cath_data_list.append(0)
			elif svm_dict[key] == "Negative":
				cath_data_list.append(1)
			elif svm_dict[key] == "Positive":
				cath_data_list.append(2)
			else:
				cath_data_list.append(3)

		# Column U in CleanData.csv
		elif key == "StudyStressSPECTMRIIschemia":
			if svm_dict[key] == "":
				cath_data_list.append(-1)
			elif svm_dict[key] == "High":
				cath_data_list.append(1)
			elif svm_dict[key] == "Intermediate":
				cath_data_list.append(2)
			elif svm_dict[key] == "Low":
				cath_data_list.append(3)
			else:
				cath_data_list.append(4)

		# Column X in CleanData.csv
		elif key == "Scheduling_Type":
			if svm_dict[key] == "":
				cath_data_list.append(-1)
			elif svm_dict[key] == "Elective":
				cath_data_list.append(0)
			elif svm_dict[key] == "Emergency":
				cath_data_list.append(1)
			else:
				cath_data_list.append(2)

		# Column Y in CleanData.csv
		elif key == "PostDiagRxRecommendation":
			if svm_dict[key] == "":
				cath_data_list.append(-1)
			elif svm_dict[key] == "CABG":
				cath_data_list.append(0)
			elif svm_dict[key] == "Medical Therapy/counseling":
				cath_data_list.append(1)
			elif svm_dict[key] == "None":
				cath_data_list.append(2)
			elif svm_dict[key] == "Other Therapy with CABG or PCI":
				cath_data_list.append(3)
			else:
				cath_data_list.append(4)

		# Column Z in CleanData.csv
		elif key == "CoronaryDominance":
			if svm_dict[key] == "":
				cath_data_list.append(-1)
			elif svm_dict[key] == "Codominant":
				cath_data_list.append(0)
			elif svm_dict[key] == "Left":
				cath_data_list.append(1)
			else:
				cath_data_list.append(2)

		elif key in float_value_keys:
			if svm_dict[key] == "": # left empty
				cath_data_list.append(-1)
				continue

			try:
				float_val = float(svm_dict[key])
			except:
				print("Raising float value exception.")
				raise Exception("Form element {} should be a float.".format(key))

			cath_data_list.append(float_val)

		else:
			if svm_dict[key] == "": # left empty
				cath_data_list.append(0)
			elif svm_dict[key] == "No":
				cath_data_list.append(0)
			else:
				cath_data_list.append(1)


	return cath_data_list









		