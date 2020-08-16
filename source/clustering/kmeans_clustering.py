from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer 
from sklearn.pipeline import Pipeline, FeatureUnion 
from sklearn.cluster import KMeans 
from sklearn.metrics import adjusted_rand_score 
from .pinyin_vectorizer import PyTfidfVectorizer
from .item_selector import ItemSelector 

class KmeansCluster:

	def __init__(self, doc_dict, k_value = 2, max_iter = 100):
		'''
		doc_dict is a dictionary which has two keys: 'questions' and 'answers',
		both keys map to a data list of strings containing questions and answers correspondingly
		'''
		
		self.doc_dict = doc_dict
		self.prediction = []
		self.k_value = k_value
		self.max_iter = max_iter 
		self.feature_names = []
		self.tfidf_matrix = []
		self.labels = []
		self.kmeans = KMeans(n_clusters = self.k_value, init='k-means++', max_iter=self.max_iter, n_init=1)
		# self.vectorizer = TfidfVectorizer()
		# self.tfidf_matrix = self.get_tfidf()
		self.tfidf_matrix = self.process(self.doc_dict)

	'''
	def get_tfidf(self):
		X = self.vectorizer.fit_transform(self.doc_list)
		self.feature_names = self.vectorizer.get_feature_names()
		return X
	'''

	def process(self, doc_dict):

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
		# feature_names

	def get_feature_names(self):
		return self.feature_names

	def get_clusters(self):
		'key is the key in the doc_dict'

		clusters= []
		quest_doc = self.doc_dict["questions"]
		ans_doc = self.doc_dict["answers"]
		doc_len = len(quest_doc)

		for i in range(self.k_value):
			clusters.append([])

		self.kmeans.fit(self.tfidf_matrix)
		self.labels = self.kmeans.labels_
		for i in range(doc_len):
			Q = "Q: " + quest_doc[i]
			A = "A: " + ans_doc[i]
			QA = " ".join([Q,A])
			clusters[self.labels[i]].append(QA)

		return clusters

	def top_10_terms(self):

		centroids = self.kmeans.cluster_centers_.argsort()

		for i in range(self.k_value):
			subcluster = []
			for j in centroids[i,:10]:
				subcluster.append(self.feature_names[j])
			clusters.append(subcluster)
		return clusters

	def get_predictions(self, new_doc_dict):
		Y = self.process(new_doc_dict)
		return self.kmeans.predict(Y)









