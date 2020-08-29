from source.clustering.tfidf_generator import TfidfGenerator
from source.classifier.model_selector import ModelSelector 
from source.preprocess.qa_processor import QAProcessor
from sklearn.linear_model import LogisticRegressionCV

import numpy as np


class SoftmaxClassifier:

	def __init__(self, max_iter = 100):
		'''
		doc_dict is a dictionary which has two keys: 'questions' and 'answers',
		both keys map to a data list of strings containing questions and answers correspondingly
		'''
		self.tfidf_gen = TfidfGenerator()
		self.sfm_clf = LogisticRegressionCV(cv=5, multi_class='multinomial', solver='lbfgs')
		self.md_selector = ModelSelector()
		self.qa_prep = QAProcessor()




	def train(self, doc):

		'''a list of strings with the format: label Q: xxxx A: xxx. The lable is from 0 to 9.'''
		X_doc, y_train = self.qa_prep.process_predict_data(doc)
		X_train = self.tfidf_gen.get_tfidf_matrix(doc)
		y_train = np.array(y_train)
		
		self.sfm_clf.fit(X_train, y_train)

	def predict(self, doc):

		X_doc = self.qa_prep.process_predict_data(doc)
		X_predict = self.tfidf_gen.get_tfidf_matrix(X_doc)
		return self.sfm_clf.predict(data_predict)

	def score(self, doc, n_split, Strat=None): 
		return self.md_selector.score(self.sfm_clf, n_split, doc = doc, strat= Strat)

	def get_score_result(self):
		return self.md_selector.get_score_result()

	def cross_val_score(self, doc, split_n):

		return self.md_selector.cross_val_score(self.sfm_clf, n_split = split_n, doc= doc)

	def get_cross_val_result(self):
		return self.md_selector.get_cross_val_result()

	def train_test_val_score(self,  doc, strat = None, weight = [8,1,1]):
		return self.md_selector.train_test_val_score(self.sfm_clf, doc = doc, weight = weight, strat = strat)

	def get_val_result(self):
		return self.md_selector.get_val_result()



def main():

	# obtain the training data from the labeled_clusters file.
	f = open("/Users/ink/Documents/MLE/NLP_Project/data/labeled_clusters.txt", "r")
	train_data = f.readlines()
	f.close()

	sfm_clf = SoftmaxClassifier()


	# sc = sfm_clf.cross_val_score(train_data, 3)
	# print(sc)


	sc = sfm_clf.train_test_val_score(doc = train_data, strat = [0,1,2,3,4,5,6,7,8,9],weight = [8,1,1],)
	print(sc)

	val_fold, pred_result = sfm_clf.get_val_result()
	print(val_fold)
	print(pred_result)

	
	with open("/Users/ink/Downloads/test_result.txt", "w") as f:
		for i in range(len(val_fold)):
			f.write("{} {}".format(pred_result[i], val_fold[i]))


main()










	