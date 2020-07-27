from text_filter import TextFilter
from qa_generator import QAGenerator 
from features_generator import FeaturesGenerator
from tfidf_generator import TfidfGenerator
from kmeans_clustering import KmeansCluster 

class Preprocessor:
	def __init__(self, file_route):
		
		myfile = open(file_route, 'r')
		text_filter = TextFilter(myfile)
		self.orig_data = text_filter.remove_url()

		self.qa_generator = QAGenerator(self.orig_data)
		self.qa_generator.processData()
		self.feature_generator = FeaturesGenerator()
		self.tfidg_gen = TfidfGenerator()
	
	def get_answers(self):
		
		answers = self.qa_generator.get_answers()
		return answers 

	def get_questions(self):
		questions = self.qa_generator.get_questions()
		return questions 

	def get_tokens (self, file):
		"file should be a list of strings"
		tokens = self.feature_generator.get_tokens(file)
		return tokens 

	def get_pinyin(self, file):
		"file shoudl be a list of strings"
		py = self.feature_generator.get_pinyin(file)
		return py 

	def get_tfidf (self, file):
		"file should be a list of strings, retunr a sparse matrix"
		tfidf = self.tfidf_gen.get_tfidf(file)
		return tfidf 

	def get_tfidf_feature_names(self, file):
		feature_names = self.tfidf_gen.get_feature_names(file)
		return feature_names 

	def get_clusters(self, doc_list, k_value =2, max_iter=100):
		cluster_gen = KmeansCluster(doc_list, k_value, max_iter)
		clusters = cluster_gen.get_clusters()
		print(clusters)

'''
	def get_predictions(self, orig_doc, new_doc, k_value =2, max_iter=100):
		cluster_gen = KmeansCluster(orig_doc, k_value, max_iter)
		Y = cluster_gen.vectorizer(new_doc)
		return cluster_gen.predict(Y)
'''




def main():
	file_route = "/Users/ink/Documents/SummerProject/data/chatbot.txt"
	text_preprocessor = Preprocessor(file_route)

	answers = text_preprocessor.get_answers()
	# questions = text_preprocessor.get_questions()

	ans_tokens = text_preprocessor.get_tokens(answers)
	# quest_tokens = text_preprocessor.get_tokens(questions)

	# print(ans_tokens)
	# print(quest_tokens)

	# ans_pinyin = text_preprocessor.get_pinyin(ans_tokens)
	# quest_pinyin = text_preprocessor.get_pinyin(quest_tokens)

	ans_clusters = text_preprocessor.get_clusters(ans_tokens,k_value = 20)
	# quest_clusters = text_preprocessor.get_clusters(quest_tokens, k_value = 3)
	

main()


