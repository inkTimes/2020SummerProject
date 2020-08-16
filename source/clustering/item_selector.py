from sklearn.base import BaseEstimator, TransformerMixin

class ItemSelector(BaseEstimator, TransformerMixin):
	def __init__(self, key):
		self.key = key 

	def fit(self, x, y=None):
		return self

	def transform(self, doc_dict):
		return doc_dict[self.key]