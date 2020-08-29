
from sklearn.model_selection import StratifiedKFold
from sklearn.base import clone 
from source.clustering.tfidf_generator import TfidfGenerator
from source.preprocess.qa_processor import QAProcessor 

import numpy as np
import random


class ModelSelector:

	def __init__(self):

		self.tfidf_gen = TfidfGenerator()
		self.qa_prep = QAProcessor()
		self.cross_test = []
		self.cross_pred_result = []
		self.test = []
		self.pred_result = []
		self.val_test = []
		self.val_pred = []

	def cross_val_score(self, classifier, n_split, doc):
		''' a list of strings with the format: label Q: xxxx A: xxx. The lable is from 0 to 9.
		'''

		scores = []
		skfolds = StratifiedKFold

		X_doc_dict, y_train = self.qa_prep.process_train_data(doc)
		X_train = self.tfidf_gen.get_tfidf_matrix(X_doc_dict)
		y_train = np.array(y_train)
		self.cross_test = []
		self.cross_pred_result = []

		skfolds = StratifiedKFold(n_splits = n_split)


		for train_index, test_index in skfolds.split(X_train, y_train):
			clone_clf = clone(classifier)
			X_train_folds = X_train[train_index]
			y_train_folds = y_train[train_index]
			X_test_fold = X_train[test_index]
			y_test_fold = y_train[test_index]
			self.cross_test.append(X_test_fold)


			clone_clf.fit(X_train_folds, y_train_folds)
			y_pred = clone_clf.predict(X_test_fold)
			self.cross_pred_result.append(y_pred)
			n_correct = sum(y_pred == y_test_fold)
			scores.append(n_correct/len(y_pred))

		return scores

	def get_cross_val_result(self):
		return self.cross_test, self.cross_pred_result

	def score(self, classifier, n_split, doc, strat = None):
		'''If you want to make it stratified, then provide strat as a labeling list for classification. 
		'''
		self.test = []
		self.pred_result = []

		doc_orig = np.array(doc)

		X_doc_dict, y_train = self.qa_prep.process_train_data(doc)
		X = self.tfidf_gen.get_tfidf_matrix(X_doc_dict)
		y = np.array(y_train)

		train_index, test_index = self.split_train_test(len(doc), 1/n_split, stratified=strat)
		X_train, y_train, X_test, y_test= X[train_index], y[train_index], X[test_index], y[test_index]

		clf = classifier 
		clf.fit(X_train, y_train)
		y_pred = clf.predict(X_test)
		n_correct = sum(y_pred == y_test)
		score = n_correct/len(y_pred)

		doc_array = np.array(doc)
		self.test = doc_array[test_index]
		self.pred_result = y_pred

		return score

	def get_score_result(self):

		return self.test, self.pred_result


	def train_test_val_score(self, classifier, doc, weight = [8,1,1],  strat=None):

		self.val_test = []
		self.val_pred = []

		doc_orig = np.array(doc)

		X_doc_dict, y_train = self.qa_prep.process_train_data(doc)
		X = self.tfidf_gen.get_tfidf_matrix(X_doc_dict)
		y = np.array(y_train)

		train_index, test_index, val_index = self.split_train_test_val(y, weight = weight, Stratified=strat)
		X_train, y_train, X_test, y_test, X_val, y_val= X[train_index], y[train_index], X[test_index], y[test_index], X[val_index], y[val_index]

		score = []

		clf = classifier 
		clf.fit(X_train, y_train)
		y_test_pred = clf.predict(X_test)
		n_correct = sum(y_test_pred == y_test)
		score.append(n_correct/len(y_test_pred))

		y_val_pred = clf.predict(X_val)
		n_correct = sum(y_val_pred == y_val)
		score.append(n_correct/len(y_val_pred))

		doc_array = np.array(doc)
		self.test = doc_array[test_index]
		self.pred_result = y_test_pred

		self.val_test =doc_array[val_index]
		self.val_pred = y_val_pred

		return score 

	def get_val_result(self):
		return self.val_test, self.val_pred 


	def split_train_test(self, y,test_ratio, Stratified=None):


		if Stratified != None:
			cat_dict = {}
			for cat in Stratified:
				cat_dict[cat] = []

			for i in range(len(y)):
				cat_dict[y[i]].append(i)

			train_indices = []
			test_indices = []

			for key in cat_dict:
				l = len(cat_dict[key])
				shuffled_indices = random.sample(cat_dict[key], l)
				test_set_size = int(l*test_ratio)
				test_indices += shuffle_indices[:test_set_size]
				train_indices += shuffle_indices[test_set_size:]
		else: 
			shuffled_indices = np.random.permutation(len(y))
			test_set_size = int((len(y))*test_ratio)
			test_indices = shuffled_indices[:test_set_size]
			train_indices = shuffled_indices[test_set_size:]

		return train_indices, test_indices



	def split_train_test_val(self, y, weight, Stratified = None):
		'''weight list is a list of integers containing three numbers,
		weight of train set, weight of test set, weight of validation set. 
		'''

		if Stratified != None:
			cat_dict = {}
			for cat in Stratified:
				cat_dict[cat] = []

			for i in range(len(y)):
				cat_dict[y[i]].append(i)

			train_indices = []
			test_indices = []
			val_indices = []
			train_ratio = weight[0]/sum(weight)
			test_ratio = weight[1]/sum(weight)

			for key in cat_dict:
				l = len(cat_dict[key])
				train_set_size = int(l*train_ratio)
				test_train_set_size = int(l*(train_ratio + test_ratio))
				shuffled_indices = random.sample(cat_dict[key],l)
				train_indices += shuffled_indices[:train_set_size]
				test_indices += shuffled_indices[train_set_size:test_train_set_size]
				val_indices += shuffled_indices[test_train_set_size:]

		else:
			shuffled_indices = np.random.permutation(len(y))
			train_ratio = weight[0]/sum(weight)
			eval_ratio = weight[2]/sum(weight)
			train_set_size = int(len(y)*train_ratio)
			second_split = int(len(y)*(1-eval_ratio))

			train_indices = shuffled_indices[:train_set_size]
			test_indeces = shuffled_indices[train_set_size:second_split]
			val_indices = shuffled_indices[second_split:]

		return train_indices, test_indices, val_indices

























