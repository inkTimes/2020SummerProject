from sklearn.feature_extraction.text import TfidfVectorizer 

class TfidfGenerator:
	def __init__(self):
		self.shape = 0
		self.vectorizer = TfidfVectorizer()

	def get_tfidf(self, text):
		X = self.vectorizer.fit_transform(text)
		self.shape = X.shape
		return X
	def get_feature_names(self, text):
		self.vectorizer.fit_transform(text)
		feature_names = self.vectorizer.get_feature_names()
		return feature_names