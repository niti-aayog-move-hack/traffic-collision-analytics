import importlib.machinery
import sys
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import POS
import Adjectives
import json
import re

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\LifeAnalytics\SaaS\La v0.2 - With Core\pyt\Core\modifications.py')
modifications = loader.load_module('report')

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\LifeAnalytics\SaaS\La v0.2 - With Core\pyt\Core\FetchTwitterData.py')
FetchTwitterData = loader.load_module('report')

sid = SentimentIntensityAnalyzer()

name = sys.argv[1].strip()
name = re.sub(" ", "", name)

text = sys.argv[2].strip()

line_list = text.split(".")
line_count = 0

for i in range(len(line_list)):
	line_count = line_count + 1
	line_list[i] = line_list[i].strip()

Dic = {"pos":0, "neg":0, "freq":0}

if_any_nouns = []

	
for l1 in line_list:

	Line_Dic = {"pos":0, "neg":0, "freq":0}

	noun_list = POS.main(l1.split(" "))

	for noun in noun_list:
		if_any_nouns.append(noun)

	adjective_list = Adjectives.main(l1.split(" "))


	#------------------CALCULATING THE TOTAL COMPOUND SENT SCORE FOR ALL ADJECTIVES IN THE LINE---------------------
	s = 0
	cnt = 0

	for adj in adjective_list:
		sent_score = sid.polarity_scores(adj)
		cnt = cnt + 1
		s = s + sent_score['compound']

	#-----------------AVERAGING THE COMPOUND SENT SCORE FOR THE ADJECTIVES-----------------------------------------
	try:
		avg_adj_sent = s/cnt
		if avg_adj_sent == 0:
			avg_adj_sent = 1


	except ZeroDivisionError:
		avg_adj_sent = 1

	#-----------------CALCULATING THE TOTAL SENT SCORE FOR ALL THE NOUNS IN THE TEXT USING TWITTER & NEWS DATASET-------------
	line_list = FetchTwitterData.main(name)

	for line in line_list:
		line = line.strip()
		line = modifications.modify(line)
		line = line.split("\t")[4].strip()
		cnt = 0
		try:
			for noun in noun_list:
				if noun.upper() in line.upper():
					cnt = cnt + 1

				if cnt > 0 :
					sent_scores = sid.polarity_scores(line)
					Dic["freq"] = Dic["freq"] + 1
					Line_Dic["freq"] = Line_Dic["freq"] + 1
					Line_Dic["pos"] = Line_Dic["pos"] + (sent_scores['pos'] * (2**cnt))
					Line_Dic["neg"] = Line_Dic["neg"] + (sent_scores['neg'] * (2**cnt))

		except:
			pass

	#------------------------AVERAGING THE SENTIMENT SCORES FOR NOUNS----------------------------------
	try:
		Line_Dic["pos"] = round(Line_Dic["pos"] / Line_Dic["freq"],2)
		Line_Dic["neg"] = round(Line_Dic["neg"] / Line_Dic["freq"],2)

	except ZeroDivisionError:
		continue

	#------------------------AMPLIFYING THE SENTIMENT SCORES USING THE ADJECTIVE COMPOUND SCORE------------------------

	Line_Dic["pos"] = Line_Dic["pos"] * abs(avg_adj_sent)
	Line_Dic["neg"] = Line_Dic["neg"] * abs(avg_adj_sent)

	if(avg_adj_sent < 0):
		Line_Dic["pos"], Line_Dic["neg"] = Line_Dic["neg"], Line_Dic["pos"]

	#----------------------ADDING THE SENTIMENT SCORES TO THE GLOBAL TOTAL---------------------------
	Dic["pos"] = Dic["pos"] + Line_Dic["pos"]
	Dic["neg"] = Dic["neg"] + Line_Dic["neg"]
	Dic["freq"] = Dic["freq"] + 1


if len(if_any_nouns) > 0:
	try:
		Dic["pos"] = round(Dic["pos"] / line_count,2)
		Dic["neg"] = round(Dic["neg"] / line_count,2)
		print(json.dumps(Dic))

	except ZeroDivisionError:
		no_result = {"no_result": True}
		print(json.dumps(no_result))
		
else:
	no_result = {"no_result": True}
	print(json.dumps(no_result))