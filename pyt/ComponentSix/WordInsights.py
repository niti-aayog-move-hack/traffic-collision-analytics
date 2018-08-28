import importlib.machinery
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import sys
import json

loader = importlib.machinery.SourceFileLoader('report', '/home/bhargav/Desktop/KAnOE/Platform/pyt/Core/FetchTwitterData.py')
FetchTwitterData = loader.load_module('report')


name = sys.argv[1].strip()
name = re.sub(" ", "", name)
word = sys.argv[2].strip()

def main(word,name):
	sid = SentimentIntensityAnalyzer()
	dic = {"freq" : 0, "comp" : 0, "neg" : 0, "neu" : 0, "pos" : 0}

	line_list = FetchTwitterData.main(name)

	cnt = 0

	for line in line_list:
		line = line.strip()
		try:
			txt = line.split("\t")[4].strip()
			if word.upper() in txt.upper():
				cnt = cnt + len(re.findall(word.upper(), txt.upper()))
				dic["freq"] = dic["freq"] + 1
				sent_scores = sid.polarity_scores(txt)
				dic["comp"] = dic["comp"] + sent_scores['compound']
				dic["neg"] = dic["neg"] + sent_scores['neg']
				dic["neu"] = dic["neu"] + sent_scores['neu']
				dic["pos"] = dic["pos"] + sent_scores['pos']
		except:
			pass


	for field in dic:
		if field != "freq":
			if dic["freq"] != 0:
				dic[field] = dic[field] / dic["freq"]
			else:
				no_result = {"no_result": True}
				print(json.dumps(no_result))
				return 0

	opdic = {"word":word, "mentions":cnt, "compound":round(dic['comp'],2), "neg":round(dic['neg'],2), "neu":round(dic['neu'],2), "pos":round(dic['pos'],2)}
	print(json.dumps(opdic))

main(word,name)