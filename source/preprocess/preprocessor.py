from text_filter import TextFilter
from qa_generator import QAGenerator 
from features_generator import FeaturesGenerator
from tfidf_generator import TfidfGenerator  

class Preprocessor:
	def __init__(self, file_route):
		
		myfile = open(file_route, 'r')
		text_filter = TextFilter(myfile)
		self.orig_data = text_filter.remove_url()

		self.qa_generator = QAGenerator(self.orig_data)
		self.qa_generator.processData()
		self.feature_generator = FeaturesGenerator()
		self.tfidf_gen = TfidfGenerator()
	
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



def main():
	file_route = "/Users/ink/Documents/SummerProject/data/testbot1.txt"
	text_preprocessor = Preprocessor(file_route)

	answers = text_preprocessor.get_answers()
	questions = text_preprocessor.get_questions()

	ans_tokens = text_preprocessor.get_tokens(answers)
	quest_tokens = text_preprocessor.get_tokens(questions)
	
	print(ans_tokens)
	print(quest_tokens)

	ans_pinyin = text_preprocessor.get_pinyin(ans_tokens)
	quest_pinyin = text_preprocessor.get_pinyin(quest_tokens)



	ans_tfidf = text_preprocessor.get_tfidf(ans_tokens)
	quest_tfidf = text_preprocessor.get_tfidf(quest_tokens)

	ans_feature_names = text_preprocessor.get_tfidf_feature_names(ans_tokens)
	quest_feature_names = text_preprocessor.get_tfidf_feature_names(quest_tokens)

	


main()


