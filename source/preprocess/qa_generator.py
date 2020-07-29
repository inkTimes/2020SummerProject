import re 

class QAGenerator:
	'''This class aims to obtain the questions and answers from the original data!'''

	def __init__(self, orig_data):

		self.orig_data = orig_data
		self.question = []
		self.answer = []
		self.ans = False
		# self.track = 0
		# self.track_dict = {}
		# self.len_track = 0
		# self.customer_record = {}


	def processData(self):
		answer_list = []
		question_list = []
		shift = False
		if_del = False
		is_question = 0

		for line in self.orig_data:

			if line[0] == "-":
				quest_identity = line.replace("-", "")
				if quest_identity[0:5] == '佩爱旗舰店':
					if_del = True
				else:
					if_del = False
			if if_del == True:
				continue 

			if line[0] == '-':

				# self.customer_record[len(self.question)] = line.replace("-", "")
				# self.track += 1
				# Track the length of the answers and questions 

				self.ans = False
				if shift != self.ans:
					if is_question == 0:
						anwser_list = []
					else:
						if len(answer_list) != 0:
							self.answer.append(' '.join([i.strip() for i in answer_list]))
							answer_list = []
				else:
					if len(question_list) != 0:
						question_list = []
						# self.question.append(' '.join(i.strip() for i in question_list))
				shift = self.ans
				is_question = 0

				# if len(self.answer) - len(self.question) != self.len_track:
					
				# 	self.track_dict[self.track] = line.replace("-", "")
				# 	self.len_track = len(self.answer) - len(self.question)

				continue
			else:
				# Identify the questions and answers using the date string in the line 
				m = re.search(r"\((\d+)-(\d+)-(\d+)\s+(\d+):(\d+):(\d+)\):", line)

				if m != None:
					line = re.split(r"\):\s+", line)
					if line[0][0:5] == "佩爱旗舰店":
						self.ans = True
						answer_list.append(line[-1])
					else:
						self.ans = False
						is_question += 1
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
					if is_question == 1:
						answer_list = []
					else:
						if len(answer_list) != 0:
							self.answer.append(' '.join([i.strip() for i in answer_list]))
							answer_list = []
				shift = self.ans

	def get_answers(self):
		return self.answer

	def get_questions(self):
		return self.question

