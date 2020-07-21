from sklearn.feature_extraction.text import TfidfVectorizer 

class tfidfgenerator:
	def __init__(self):
		self.shape = 0

	def get_tfidf(self, text):
		vectorizer = TfidfVectorizer()
		X = vectorizer.fit_transform(text)
		self.shape = X.shape
		return X, X.shape