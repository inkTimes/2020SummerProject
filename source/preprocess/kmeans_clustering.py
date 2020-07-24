from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.cluster import KMeans 
from sklearn.metrics import adjusted_rand_score 

class KmeansCluster:

	def __init__(self, doc_list, k_value = 2, max_iter = 100):
		self.doc_list = doc_list
		self.prediction = []
		self.tfidf_matrix = []
		self.feature_names = []
		self.vectorizer = TfidfVectorizer()
		self.tfidf_matrix = self.get_tfidf()
		self.k_value = k_value
		self.kmeans = KMeans(n_clusters=k_value, init='k-means++', max_iter = max_iter, n_init=1)

	def get_tfidf(self):
		X = self.vectorizer.fit_transform(self.doc_list)
		self.feature_names = self.vectorizer.get_feature_names()
		return X

	def get_clusters(self):

		clusters = []

		self.kmeans.fit(self.tfidf_matrix)

		centroids = self.kmeans.cluster_centers_.argsort()

		for i in range(self.k_value):
			subcluster = []
			for j in centroids[i,:]:
				subcluster.append(self.feature_names[j])
			clusters.append(subcluster)
		return clusters

	def get_predictions(self, new_doc):

		Y = self.vectorizer.transform(new_doc)
		return self.kmeans.predict(Y)












