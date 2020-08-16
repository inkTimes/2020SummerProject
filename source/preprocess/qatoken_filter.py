import re 

class TokenFilter:

	def __init__(self, quest_token, ans_token):

		self.quest = quest_token 
		self.ans = ans_token 
		self.process()

	def process(self):
		clean_ques = []
		clean_ans = []
		count = 0
		for i in range(len(self.quest)):
			line = self.quest[i].strip()
			if line == '':
				count += 1
				continue
			else:
				clean_ques.append(self.quest[i])
				clean_ans.append(self.ans[i])
		self.quest = clean_ques
		self.ans = clean_ans
		print("{} empty sentences have been removed.".format(count))


	def rm_keywords(self, keyword):
		clean_quest = []
		clean_ans = [] 
		count = 0

		for i in range(len(self.quest)):
			result = re.search(keyword, self.quest[i])
			if result == None:
				clean_quest.append(self.quest[i])
				clean_ans.append(self.ans[i])
			else:
				count += 1

		print("{} sentences have been removed.".format(count))

		self.quest = clean_quest
		self.ans = clean_ans
		return clean_quest, clean_ans