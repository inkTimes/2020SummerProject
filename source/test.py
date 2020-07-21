from preprocess.textfilter import textfilter
from preprocess.QAgenerator import QAgenerator 
from preprocess.features_generator import features_generator

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



main()




