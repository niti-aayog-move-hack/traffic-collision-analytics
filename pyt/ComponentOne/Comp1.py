import os
import sys
from TweetsFetch import fetch
import x2
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import wiki
import json
import re

def main():
	sid = SentimentIntensityAnalyzer()

	dic = {"freq":0,"neg":0,"neu":0,"pos":0,"comp":0}

	tw_handle = input("Enter twitter handle : ")
	name = input("Enter name : ")
	wiki_search = name

	name = re.sub(" ", "", name)

	news_search_keys = [wiki_search]

	for i in range(len(news_search_keys)):
		news_search_keys[i] = news_search_keys[i].strip()

	f_name,ft = fetch(name,tw_handle)
	x2.main(news_search_keys,f_name,ft)
	
	try:
		summary = wiki.main(wiki_search)
	except:
		summary = None

	f = open(f_name,"r", encoding="utf-8")
	for line in f.readlines():
		if "\t\t" in line:
			continue

		line = line.strip()
		sent_scores = sid.polarity_scores(line.split("\t")[4].strip())
		dic["freq"] = dic["freq"] + 1
		dic["neg"] = dic["neg"] + sent_scores['neg']
		dic["pos"] = dic["pos"] + sent_scores['pos']
		dic["neu"] = dic["neu"] + sent_scores['neu']
		dic["comp"] = dic["comp"] + sent_scores['compound']

	for elem in dic:
		if elem != "freq":
			dic[elem] = round(dic[elem] / dic["freq"],2)

	overall_sent_sum = {"name":wiki_search, "compound":dic['comp'], "neg":dic['neg'], "neu":dic['neu'], "pos":dic['pos'], "summary":summary }
	print(json.dumps(overall_sent_sum))
main()