from preprocess.textfilter import textfilter
from preprocess.QAgenerator import QAgenerator 
from preprocess.features_generator import features_generator
from preprocess.tfidfgenerator import tfidfgenerator  

def main():
	file_route = "/Users/ink/Documents/testbot.txt"
	text_filter = textfilter(file_route)
	orig_data = text_filter.remove_url() # remove the url from the data

	qa_generator = QAgenerator(orig_data)
	qa_generator.processData()

	answers = qa_generator.get_answers()
	questions = qa_generator.get_questions()

	feature_gen = features_generator()
	ans_tokens = feature_gen.get_tokens(answers)
	ques_tokens = feature_gen.get_tokens(questions)

	print(ans_tokens)
	print(ques_tokens)

	ans_pinyin = feature_gen.get_pinyin(ans_tokens)
	ques_pinyin = feature_gen.get_pinyin(ques_tokens)

	print(ans_pinyin)
	print(ques_pinyin)

	tfidf_gen = tfidfgenerator()

	ans_tfidf, ans_shape = tfidf_gen.get_tfidf(answers)
	quest_tfidf, quest_shape = tfidf_gen.get_tfidf(questions)
	print(ans_shape)
	print(quest_shape)

main()




