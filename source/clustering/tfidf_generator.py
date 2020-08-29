from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.pipeline import Pipeline, FeatureUnion 
from source.clustering.item_selector import ItemSelector 
from source.clustering.pinyin_vectorizer import PyTfidfVectorizer

class TfidfGenerator:
	def __init__(self):
		self.shape = 0
		self.vectorizer = TfidfVectorizer()

	def get_tfidf(self, text):
		'''text is a list of strings'''
		X = self.vectorizer.fit_transform(text)
		self.shape = X.shape
		return X

	def get_feature_names(self, text):
		self.vectorizer.fit_transform(text)
		feature_names = self.vectorizer.get_feature_names()
		return feature_names

	def get_tfidf_matrix(self, doc_dict):
		'''doc_dict is a dictionary with two keys: questions and answers, each maps to a list of strings containing questions and answers respectively'''

		transformer_weight = {
		'quest_ngram_tfidf':1,
		'quest_py_tfidf':0.5,
		'ans_ngram_tfidf':1,
		'ans_py_tfidf':0.5
		}


		feats = FeatureUnion([
			('quest_tokens', 
				Pipeline([
					('quest_selector', ItemSelector(key='questions')),
					('quest_ngram_tfidf', TfidfVectorizer(ngram_range=(1,3)))])),
			('quest_pinyin',
				Pipeline([
					('quest_selector', ItemSelector(key='questions')),
					('quest_py_tfidf', PyTfidfVectorizer(ngram_range=(1,3)))])),
			('ans_tokens',
				Pipeline([
					('ans_selector', ItemSelector(key='answers')),
					('ans_ngram_tfidf', PyTfidfVectorizer(ngram_range=(1,3)))])),
			('ans_pinyin',
				Pipeline([
					('ans_selector', ItemSelector(key='answers')),
					('ans_py_tfidf', PyTfidfVectorizer(ngram_range=(1,3)))]))
							], transformer_weights = transformer_weight)


		tfidf_matrix = feats.fit_transform(doc_dict)
		# feature_names = feats.get_feature_names()
		return tfidf_matrix

