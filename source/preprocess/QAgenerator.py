import re 

class QAgenerator:
	'''This class aims to obtain the questions and answers from the original data!'''

	def __init__(self, orig_data):

		self.orig_data = orig_data
		self.question = []
		self.answer = []
		self.ans = False


	def processData(self):
		answer_list = []
		question_list = []
		shift = False

		for line in self.orig_data:

			if line[0] == '-':
				self.ans = False
				if shift != self.ans:
					self.answer.append(' '.join([i.strip() for i in answer_list]))
					answer_list = []
					shift = self.ans
				continue
			else:
				m = re.search(r"\((\d+)-(\d+)-(\d+)\s+(\d+):(\d+):(\d+)\):", line)

				if m != None:
					line = re.split(r"\):\s+", line)
					if line[0][0:5] == "佩爱旗舰店":
						self.ans = True
						answer_list.append(line[-1])
					else:
						self.ans = False
						question_list.append(line[-1])
				else:
					if self.ans == True:
						answer_list.append(line)
					else:
						question_list.append(line)
			if shift != self.ans:
				if self.ans == True:
					if len(question_list) != 0:
						self.question.append(' '.join([i.strip() for i in question_list]))
						question_list = []
				else:
					if len(answer_list) != 0:
						self.answer.append(' '.join([i.strip() for i in answer_list]))
						answer_list = []
				shift = self.ans

	def get_answers(self):
		return self.answer

	def get_questions(self):
		return self.question

