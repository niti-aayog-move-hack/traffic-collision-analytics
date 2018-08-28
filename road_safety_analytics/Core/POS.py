import nltk
from nltk.tokenize import word_tokenize


def main(word_list):
	try:
		#words = "my name is Bhargav".split(" ")
		tagged = nltk.pos_tag(word_list)
		NNWordList = []
		for elem in tagged:
			if elem[1] == "NN":
				NNWordList.append(elem[0])
		for i in range(len(NNWordList)):
			NNWordList[i] = NNWordList[i].strip()

		return NNWordList

	except Exception as e:
		print(e)
		
