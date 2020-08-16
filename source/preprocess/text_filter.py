import re

class TextFilter:
	''' The purpose of this class is to convert the text file into a list,
		and get rid of the url links in the file'''

	def __init__(self, file):
		self.myfile = file
		self.orig_data = []

	def remove_url(self):

		lines = (text.strip() for text in self.myfile)
		for line in lines:
			line = re.sub(r'http\S+', '链接', line)
			if line != '':
				self.orig_data.append(line)

		return self.orig_data


