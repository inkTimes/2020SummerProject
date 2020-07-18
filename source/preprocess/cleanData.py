import re 
import jieba 
from pypinyin import pinyin 
from sklearn.feature_extraction.text import TfidfVectorizer


def get_QA (file_route):
	'''
	This function require a input of a text file with conversations distributed in each line.
	Then it removes url links and separate the question and answers into two lists, which are returned by this function.  

	'''
	# open the designated file 
	question = []
	answer = []
	ans = False
	myfile = open(file_route, 'r')
	lines = (line.strip() for line in myfile)
	for line in lines: 
		# remove the url 
		line = re.sub(r'http\S+', '链接', line)
		if line == '':
			continue
		# evaluate whether that is a questino or an answer 
		if line[0] == '-':
			ans = False
			continue
		else:
			m = re.search(r"\((\d+)-(\d+)-(\d+)\s+(\d+):(\d+):(\d+)\):", line)

			if m != None:
				line = re.split(r"\):\s+", line)
				if line[0][0:5] == '佩爱旗舰店':
					ans = True
					answer.append(line[-1])
				else: 
					ans = False
					question.append(line[-1])
			else:
				if ans == True:
					answer.append(line)
				else:
					question.append(line)
	myfile.close()

	return answer, question

def get_token(file):
	tokens = []
	for line in file:
		seg = jieba.cut(line, cut_all=False) 
		for element in seg:
			if element != ' ': # how to improve this iteration 
				tokens.append(element)
	return tokens

def get_pinyin(file):
	pin_yin = []
	for tokens in file: 
		py = pinyin(tokens)
		for element in py:
			pin_yin += element
	return pin_yin 

def get_tfidf(corpus):
	vectorizer = TfidfVectorizer()
	X = vectorizer.fit_transform(corpus)
	return X



def main():
	file_route = "/Users/ink/Downloads/testbot.txt"
	answer, question = get_QA(file_route)
	print("The answer list is: ")
	print(answer)
	answer_token = get_token(answer)
	print("The tokens of answers are: ")
	print(answer_token)
	answer_pinyin = get_pinyin(answer_token)
	print("The pinyins of answer tokens are: ")
	print(answer_pinyin)
	answer_tfidf = get_tfidf(answer)
	print("The tfidf array shape of the answer tokens is: ")
	print(answer_tfidf.shape)
	# obtain tfidf array using X.toarray()


	print("The question list is: ")
	print(question)
	question_token = get_token(question)
	print("The tokens of questions are: ")
	print(question_token)
	question_pinyin = get_pinyin(question_token)
	print("The pinyins of question tokens are: ")
	print(question_pinyin)
	question_tfidf = get_tfidf(question)
	print("The tfidf array shape of the answer tokens is: ")
	print(question_tfidf.shape)



main()

				






