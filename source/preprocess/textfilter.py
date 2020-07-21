import re

class textfilter:
	''' The purpose of this class is to convert the text file into a list,
		and get rid of the url links in the file'''

	def __init__(self, file_route):
		self.myfile = open(file_route, 'r')
		self.orig_data = []

	def remove_url(self):

		lines = (line.strip() for line in self.myfile)
		for line in lines:
			line = re.sub(r'http\S+', '链接', line)
			if line != '':
				self.orig_data.append(line)

		return self.orig_data


