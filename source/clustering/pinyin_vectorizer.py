from sklearn.feature_extraction.text import TfidfVectorizer 
from ..preprocess.features_generator import FeaturesGenerator 


class PyTfidfVectorizer:

	def __init__(self,ngram_range=(1,1)):
		self.tfidf_matrix = []
		self.vectorizer = TfidfVectorizer(ngram_range)


	def process(self, doc):

		feat_gen = FeaturesGenerator()
		doc_pinyin = feat_gen.get_pinyin(doc)
		return doc_pinyin

	def transform(self, doc, y = None):
		doc_pinyin = self.process(doc)
		return self.vectorizer.transform(doc_pinyin)

	def fit(self, doc, y = None):

		doc_pinyin = self.process(doc)
		return self.vectorizer.fit(doc_pinyin)

	def get_feature_names(self):
		return self.vectorizer.get_feature_names()





