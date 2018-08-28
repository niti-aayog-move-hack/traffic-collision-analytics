import importlib.machinery
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys
import json
import re

loader = importlib.machinery.SourceFileLoader('report', '/home/bhargav/Desktop/KAnOE/Platform/pyt/Core/FetchTwitterData.py')
FetchTwitterData = loader.load_module('report')

name = sys.argv[1].strip()
name = re.sub(" ", "", name)
word1 = sys.argv[2].strip()
word2 = sys.argv[3].strip()

def main(word1,word2,name):

	word1_tot = 0
	word1_word2 = 0

	word2_tot = 0
	word2_word1 = 0

	tot = 0

	sid = SentimentIntensityAnalyzer()

	line_list = FetchTwitterData.main(name)

	for line in line_list:
		line = line.strip()
		txt = line.split("\t")[4].strip().upper()
		if word1.upper() in txt.upper():
			word1_tot = word1_tot + 1
			if word2.upper() in txt.upper():
				word1_word2 = word1_word2 + 1

		if word2.upper() in txt.upper():
			word2_tot = word2_tot + 1
			if word1.upper() in txt.upper():
				word2_word1 = word2_word1 + 1

	try:
		opdic = {"word1":word1, "word2":word2, "associated_mentions":word2_word1, "percassoc1":round(word1_word2*100/word1_tot,2), "percassoc2":round(word2_word1*100/word2_tot,2)}
		print(json.dumps(opdic))

	except ZeroDivisionError:
		print("No Results")

main(word1,word2,name)