import jieba 
from pypinyin import pinyin 

class FeaturesGenerator:

	def __init__(self):
		self.tokens = []
		self.pin_yin = []
		file_route = "/Users/ink/Documents/SummerProject/data/cn_stopwords.txt"
		self.stopwords = set(line.strip() for line in open(file_route))

	def get_tokens(self, data):
		self.tokens = []
		for line in data:
			seg = jieba.cut(line, cut_all=False)
			seg = [i for i in list(seg) if i.strip()]
			seg = [i for i in seg if (i not in self.stopwords)]
			seg = ' '.join(elem for elem in seg)
			self.tokens.append(seg)
		return self.tokens

	def get_pinyin(self, tokens):
		self.pin_yin = []
		for token in tokens:
			py = pinyin(token)
			for elem in py:
				elem = [i for i in elem if i.strip()]
				self.pin_yin += elem
		return self.pin_yin
