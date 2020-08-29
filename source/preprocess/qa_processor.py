
class QAProcessor():

	def __init__(self):
		pass


	def process_train_data (self, doc):

		'''a list of strings with the format: label Q: xxxx A: xxx. The lable is from 0 to 9.
		Output: labels: a list of integers rangine from 0 to 9, representing 10 labeled classes;
		data_train: a dictionary with two keys: questions and answers, each maps to a list of strings'''

		labels = []
		quest_train = []
		ans_train = []

		for line in doc:
			line = line.split(" ", 1)
			labels.append(int(line[0]))
			line = line[1]
			line = line.split("Q: ")[1]
			line = line.split(" A: ")
			quest_train.append(line[0])
			ans_train.append(line[1])

		data_train = {"questions": quest_train, "answers": ans_train} # data used for scoring or training 
		return data_train, labels

	def process_predict_data(self, doc):

		quest_train = []
		ans_train = []

		for line in doc:
			line = line.split("Q: ")[1]
			line = line.split(" A: ")
			quest_train.append(line[0])
			ans_train.append(line[1])

		data_predict = {"questions": quest_train, "answers": ans_train} # data used for prediction and test
		return data_predict