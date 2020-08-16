# print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

from .text_filter import TextFilter
from .qa_generator import QAGenerator 
from .features_generator import FeaturesGenerator
from .qatoken_filter import TokenFilter
from ..clustering.tfidf_generator import TfidfGenerator
from ..clustering.kmeans_clustering import KmeansCluster 



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

	def get_clusters(self, doc_dict, k_value =2, max_iter=100):
		cluster_gen = KmeansCluster(doc_dict, k_value, max_iter)
		clusters = cluster_gen.get_clusters()
		return clusters 

	def token_filter (self, quest_token, ans_token):
		ques = []
		ans = []
		qafilter = TokenFilter(quest_token, ans_token)
		ques, ans = qafilter.rm_keywords("表情")
		return ques, ans


		

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
	questions = text_preprocessor.get_questions()

	print(len(answers))
	print(len(questions))



# The following chunk of codes checks the correspondance of questions and answers 

	# customer_record = text_preprocessor.qa_generator.customer_record
	# file = open("/Users/ink/Documents/SummerProject/data/test_result.txt", 'w')

	# for i in range (max(len(answers), len(questions))):
		# if i in customer_record.keys():
			# file.write(customer_record[i]+"\n")
		# if i < len(questions):
			# file.write("Q: " + questions[i]+'\n')
		# if i < len(answers):
			# file.write("A: " + answers[i]+'\n')
		# print("\n")
	# file.close()

	# print(len(answers))
	# print("\n")
	# print(len(questions))
	# print("\n")
	# print(text_preprocessor.qa_generator.track_dict)
	# print(len(text_preprocessor.qa_generator.track_dict))

# The following chunk of codes checks the effectiveness of the text_processor functions 	


	ans_tokens = text_preprocessor.get_tokens(answers)
	quest_tokens = text_preprocessor.get_tokens(questions)
	quest_tokens, ans_tokens = text_preprocessor.token_filter(quest_tokens, ans_tokens)

	# The following comments make two lists have equal length 

	# tokens_length = min(len(ans_tokens), len(quest_tokens))
	# ans_tokens = ans_tokens[:tokens_length]
	# quest_tokens = quest_tokens[:tokens_length]

	doc_dict = {'questions': quest_tokens, 'answers':ans_tokens}
	clusters = text_preprocessor.get_clusters(doc_dict, k_value=20)


	with open('/Users/ink/Documents/SummerProject/data/cluster_result.txt', 'w') as f:
		for i in range(len(clusters)):
			f.write("This is {} th cluster!\n".format(i+1))
			for lines in clusters[i]:
				f.write('%s\n'%lines)
			f.write('\n')


	# ans_pinyin = text_preprocessor.get_pinyin(ans_tokens)
	# quest_pinyin = text_preprocessor.get_pinyin(quest_tokens)

	# ans_clusters = text_preprocessor.get_clusters(ans_tokens,k_value = 20)
	# quest_clusters = text_preprocessor.get_clusters(quest_tokens, k_value = 3)
	

main()


