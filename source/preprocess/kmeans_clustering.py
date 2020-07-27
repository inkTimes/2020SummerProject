from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer 
from sklearn.pipeline import Pipeline, FeatureUnion 
from sklearn.cluster import KMeans 
from sklearn.metrics import adjusted_rand_score 
from pinyin_vectorizer import PyTfidfVectorizer

class KmeansCluster:

	def __init__(self, token_doc, k_value = 2, max_iter = 100):
		
		self.token_doc = token_doc
		self.prediction = []
		self.k_value = k_value
		self.max_iter = max_iter 
		self.feature_names = []
		self.tfidf_matrix = []
		self.labels = []
		self.kmeans = KMeans(n_clusters = self.k_value, init='k-means++', max_iter=self.max_iter, n_init=1)
		# self.vectorizer = TfidfVectorizer()
		# self.tfidf_matrix = self.get_tfidf()
		self.tfidf_matrix, self.feature_names = self.process(self.token_doc)

	'''
	def get_tfidf(self):
		X = self.vectorizer.fit_transform(self.doc_list)
		self.feature_names = self.vectorizer.get_feature_names()
		return X
	'''

	def process(self, doc):

		feats = FeatureUnion([
			('n_gram_tfidf', TfidfVectorizer(ngram_range=(1,3))),
			('py_tfidf', PyTfidfVectorizer())])
		tfidf_matrix = feats.fit_transform(doc)
		feature_names = feats.get_feature_names()
		return tfidf_matrix, feature_names

	def get_feature_names(self):
		return self.feature_names

	def get_clusters(self):

		clusters= []
		for i in range(self.k_value):
			clusters.append([])

		self.kmeans.fit(self.tfidf_matrix)
		self.labels = self.kmeans.labels_
		for i in range(len(self.token_doc)):
			clusters[self.labels[i]].append(self.token_doc[i])
		return clusters

	def top_10_terms(self):

		centroids = self.kmeans.cluster_centers_.argsort()

		for i in range(self.k_value):
			subcluster = []
			for j in centroids[i,:10]:
				subcluster.append(self.feature_names[j])
			clusters.append(subcluster)
		return clusters

	def get_predictions(self, new_doc):
		Y, features = self.process(new_doc)
		return self.kmeans.predict(Y)









