from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer 
from sklearn.pipeline import Pipeline, FeatureUnion 
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import adjusted_rand_score 
from source.clustering.pinyin_vectorizer import PyTfidfVectorizer
from source.clustering.item_selector import ItemSelector 

class SoftmaxClassifier:

	def __init__(self, max_iter = 100):
		'''
		doc_dict is a dictionary which has two keys: 'questions' and 'answers',
		both keys map to a data list of strings containing questions and answers correspondingly
		'''
		
		self.create_clf_pipe()


	def create_clf_pipe(self):

		transformer_weight = {
		'quest_ngram_tfidf':1,
		'quest_py_tfidf':0.5,
		'ans_ngram_tfidf':1,
		'ans_py_tfidf':0.5
		}

		self.pipe = Pipeline([
			('feats', FeatureUnion([
				('quest_tokens', 
					Pipeline([
						('quest_selector', ItemSelector(key='questions')),
						('quest_ngram_tfidf', TfidfVectorizer(ngram_range=(1,3)))])),
				('quest_pinyin',
					Pipeline([
						('quest_selector', ItemSelector(key='questions')),
						('quest_py_tfidf', PyTfidfVectorizer(ngram_range=(1,3)))])),
				('ans_tokens',
					Pipeline([
						('ans_selector', ItemSelector(key='answers')),
						('ans_ngram_tfidf', PyTfidfVectorizer(ngram_range=(1,3)))])),
				('ans_pinyin',
					Pipeline([
						('ans_selector', ItemSelector(key='answers')),
						('ans_py_tfidf', PyTfidfVectorizer(ngram_range=(1,3)))]))
				], transformer_weights = transformer_weight)),
			('sm_clf', LogisticRegressionCV(cv=5, multi_class='multinomial', solver='lbfgs'))
			])


	def train(self, doc):
		labels = []
		quest_train = []
		ans_train = []
		
		for line in doc:
			line = line.split(" ", 1)
			labels.append(line[0])
			line = line[1]
			line = line.split("Q: ")[1]
			line = line.split(" A: ")
			quest_train.append(line[0])
			ans_train.append(line[1])

		data_train = {'questions': quest_train, 'answers': ans_train}

		self.pipe.fit(data_train, labels)

	def process_predict_data (self, doc):

		quest_train = []
		ans_train = []
		for line in doc:
			line = line.split("Q: ")[1]
			line = line.split(" A: ")
			quest_train.append(line[0])
			ans_train.append(line[1])

		data_train = {"questions": quest_train, "answers": ans_train}
		return data_train

	def predict(self, doc):

		data_train = self.process_predict_data(doc)
		return self.pipe.predict(data_train)

	def score(self, doc, sample_weight = None): 

		data_train = self.process_predict_data(doc)
		return self.pipe.score(doc)


def main():

	# obtain the training data from the labeled_clusters file.
	f = open("/Users/ink/Documents/MLE/NLP_Project/data/labeled_clusters.txt", "r")
	train_data = f.readlines()
	f.close()

	# start training 

	sfm_clf = SoftmaxClassifier()

	test_data = ["Q: 新生儿 穿 多 大 的 A: 恭喜 恭喜 宝宝 已经 出生 了 吗",
	"Q: 六七个 月 穿 那个 码 A: 请问 咱家 宝宝 身高 、 体重 是 多少 呢 ， 我 给 您 推荐 合适 的 尺码 [ 表情 ]",
	"Q: 那 这款 的 尺码 呢 我家 宝 适合 多大 的 A: 宝宝 身高 多少 了 呢",
	"Q: 那 哪天 还有 活动 ？ A: 暂时 还 没有 活动 通知 您 需要的话 可以 关注 一下 我们 噢",
	"Q: 一件 退货 ， 一件 换货 ， 可以 么 ？ A: 可以"]

	sfm_clf.train(train_data)


	print(sfm_clf.predict(test_data))
	print(sfm_clf.score(train_data))



main()










	