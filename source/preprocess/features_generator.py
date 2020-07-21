import jieba 
from pypinyin import pinyin 

class features_generator:

	def __init__(self):
		self.tokens = []
		self.pin_yin = []

	def get_tokens(self, data):
		self.tokens = []
		for line in data:
			seg = jieba.cut(line, cut_all=False)
			seg = [i.strip() for i in list(seg)]
			self.tokens += seg 
		return self.tokens

	def get_pinyin(self, tokens):
		self.pin_yin = []
		for token in tokens:
			py = pinyin(token)
			for element in py:
				self.pin_yin += element
		return self.pin_yin
