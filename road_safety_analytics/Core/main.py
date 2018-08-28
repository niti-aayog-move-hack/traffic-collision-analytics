import importlib.machinery
import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys
import json
import re

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\LifeAnalytics\SaaS\La v0.2 - With Core\pyt\Core\modifications.py')
modifications = loader.load_module('report')

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\LifeAnalytics\SaaS\La v0.2 - With Core\pyt\Core\FetchTwitterData.py')
FetchTwitterData = loader.load_module('report')

name = sys.argv[1].strip()
orig_name = name
name = re.sub(" ", "", name)



LocCoords = {}

f = open("LocCoord.txt", "r", encoding="utf-8")
for line in f.readlines():
	line = line.strip()
	l = line.split("\t")
	for i in range(len(l)):
		l[i] = l[i].strip()

	try:
		LocCoords[l[0]] = (l[1],l[2])
	except:
		continue

f.close()

f = open("../data/uselessWords.txt","r", encoding="utf-8")
useless_words = []
for line in f.readlines():
	line = line.strip()
	useless_words.append(line.upper())
f.close()


f1 = open("../data/narendramodiTwitterData.txt", 'r', encoding="utf-8")
x = f1.readlines()
train_text = ""
for i in x:
	train_text = train_text + i
f1.close()

#----------------------------------------------------------
line_list = FetchTwitterData.main(name)
#----------------------------------------------------------

y = line_list
sample_text = ""
for i in y:
	sample_text = sample_text + i

custom_sent_tokenizer  = PunktSentenceTokenizer(train_text)

tokenized = custom_sent_tokenizer.tokenize(sample_text)

LocDic = {}

def top_words(Dic):
	cnt = 0
	frequencies = []
	for word in Dic:
		if Dic[word] not in frequencies:
			frequencies.append(Dic[word])

	frequencies.sort(reverse=True)
	
	thresh = frequencies[len(frequencies)//2]

	word_list = []

	for i in range(len(frequencies)):
		thresh = frequencies[i]
		if cnt < 6:
			for word in Dic:
				if cnt < 6:
					if(Dic[word] == thresh):
						cnt = cnt + 1
						word_list.append(word)

	return word_list

def process_content():
	global LocDic
	global LocCoords
	sid = SentimentIntensityAnalyzer()

	new_locations = []

	#try:
	for i in tokenized:
		text_list = []
		line_list = i.split("\n")
		for line in line_list:
			try:
				text_list.append(line.split("\t")[4].strip())
			except:
				text_list.append(line.strip())

		words = nltk.word_tokenize(i)
		tagged = nltk.pos_tag(words)
		
		namedEnt = nltk.ne_chunk(tagged)
		for elem in namedEnt:
			if(isinstance(elem,nltk.tree.Tree)):
				if(elem.label() == "GPE"):
					for e in elem.leaves():
						loc = e[0].strip()
						if loc in LocCoords:
							loc_lat,loc_long = LocCoords[loc][0], LocCoords[loc][1]

						else:
							continue

						if loc not in LocDic:
							LocDic[loc] = {"lat":loc_lat, "long":loc_long, "freq":0, "comp":0, "neg":0, "neu":0, "pos":0, "word_freq":{}}

						for text in text_list:
							sent_scores = sid.polarity_scores(text)
							LocDic[loc]["freq"] = LocDic[loc]["freq"] + 1
							LocDic[loc]["comp"] = LocDic[loc]["comp"] + sent_scores['compound']
							LocDic[loc]["neg"] = LocDic[loc]["neg"] + sent_scores['neg']
							LocDic[loc]["pos"] = LocDic[loc]["pos"] + sent_scores['pos']
							LocDic[loc]["neu"] = LocDic[loc]["neu"] + sent_scores['neu']

							text = modifications.modify(text)
							word_list = text.split(" ")

							for word in word_list:
								word = word.upper()
								if word not in useless_words and word != "RT":
									if word not in LocDic[loc]["word_freq"]:
										LocDic[loc]["word_freq"][word] = 0

									LocDic[loc]["word_freq"][word] = LocDic[loc]["word_freq"][word] + 1



	for loc in LocDic:
		for field in LocDic[loc]:
			if field != "freq" and field != "lat" and field != "long" and field and field != "word_freq":
				LocDic[loc][field] = round(LocDic[loc][field] / LocDic[loc]["freq"],2)

	opdic = []
	for loc in LocDic:
		word_list = top_words(LocDic[loc]["word_freq"])
		opdic.append({"pol_name":orig_name, "name":loc, "compound":LocDic[loc]["comp"], "frequency":LocDic[loc]["freq"], "position":{"lat":LocDic[loc]["lat"], "lng":LocDic[loc]["long"]}, "words":word_list})

	print(json.dumps(opdic))


process_content()
