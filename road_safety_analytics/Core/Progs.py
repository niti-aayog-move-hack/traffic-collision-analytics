import datetime
import importlib.machinery
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import PunktSentenceTokenizer
import json
import collections
from operator import itemgetter
import re
#import POS

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\LifeAnalytics\SaaS\La v0.2 - With Core\pyt\Core\modifications.py')
modifications = loader.load_module('report')

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\LifeAnalytics\SaaS\La v0.2 - With Core\pyt\Core\FetchTwitterData.py')
FetchTwitterData = loader.load_module('report')

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\LifeAnalytics\SaaS\La v0.2 - With Core\pyt\Core\POS.py')
POS = loader.load_module('report')

#----------------------------------------------------------component 2--------------------------------------------------------------------------------------


#Produces the final outout for the co-occurance map
def get_co_words_graph(w1,freq_words,CoOccurenceMap):
	graph = []
	
	for w2 in freq_words:
		if w2 != w1:
			if w2 in CoOccurenceMap[w1]:
				graph.append({"word":w2, "frequency":CoOccurenceMap[w1][w2]})

	return graph

def top30_td(text,delim,orig_name):		#Top 30, text and delimiter
	line_list = text.split(delim)
	top30_ll(line_list,orig_name)

def top30_ll(line_list,orig_name):		#Top 30, line list
	f = open(r"../data/uselessWords.txt", "r",encoding="utf-8")
	useless_words = []

	for line in f.readlines():
		line = line.strip()
		useless_words.append(line.upper())

	sid = SentimentIntensityAnalyzer()
	FreqMap = {}
	WordSentMap = {}
	year_list = []
	CoOccurenceMap = {}

	for line in line_list:
#		try:
		line = line.strip()
		line = line.split("\t")
		text = line[4].strip()
		text = modifications.modify(text)

		word_list = text.split(" ")	#Getting a list of words in the tweet

		created_at = line[5].strip()
		date = created_at.split(" ")[0]	
		date = date.split("-")

		year = int(date[0].strip())		#year of creation for the tweet
		if year not in year_list:
			year_list.append(year)		#Update the yearlist

		month = int(date[1].strip())	#month of creation for the tweet

#		except:
#			continue

		#----------------------Converting all words in wordlist to upper case-----------------------
		for i in range(len(word_list)):
			word_list[i] = word_list[i].strip().upper()	
		#-------------------------------------------------------------------------------------------*

		#-------------------Updating Dict for words and their frequencies---------------------------
		for word in word_list :
			if (word not in FreqMap):
				FreqMap[word] = 0

			FreqMap[word] = FreqMap[word] + 1
		#-------------------------------------------------------------------------------------------*

		sent_scores = sid.polarity_scores(text)	#Getting sentiment scores for the tweet text
		
		# Find the Co-occurance Matrix
		for word1 in word_list :
			if word1 not in CoOccurenceMap :
				CoOccurenceMap[word1] = {}

			for word2 in word_list :
				if word2 not in CoOccurenceMap[word1] :
					CoOccurenceMap[word1][word2] = 0

				CoOccurenceMap[word1][word2] = CoOccurenceMap[word1][word2] + 1

		#-----Adding sentiments score of the tweet text to each word in the tweet (wordlist)--------
		for word in word_list:
			if word not in WordSentMap:
				WordSentMap[word] = {"compound":0,"neg":0,"neu":0,"pos":0}

			WordSentMap[word]["compound"] = WordSentMap[word]["compound"] + sent_scores["compound"]
			WordSentMap[word]["neg"] = WordSentMap[word]["neg"] + sent_scores["neg"]
			WordSentMap[word]["neu"] = WordSentMap[word]["neu"] + sent_scores["neu"]
			WordSentMap[word]["pos"] = WordSentMap[word]["pos"] + sent_scores["pos"]

	frequencies = []

	
	#Make a list of all UNIQUE frequencies 
	for word in FreqMap :
		if word not in useless_words and word != "" and word != "RT":
			if FreqMap[word] not in frequencies :
				frequencies.append(FreqMap[word])

	frequencies.sort(reverse=True)

	#Find the Threshold frequency
	try:
		thresh = frequencies[30]

	except:	#If 30 different frequencies are unavailable, the median frequency is the threshold frequency
		thresh = frequencies[int(len(frequencies)/2)]
	

	freq_words = []
	cnt = 0
	for i in range(len(frequencies)):
		if frequencies[i] < thresh:
			break

		for word in FreqMap:
			if cnt == 40:
				break

			elif FreqMap[word] == frequencies[i] and FreqMap[word] >= thresh and FreqMap[word] > 1 and word != "" and word != "RT" and word not in useless_words:
				freq_words.append(word)
				cnt = cnt + 1

	opdic = []

	for w1 in freq_words:
		co_words_graph = get_co_words_graph(w1,freq_words,CoOccurenceMap)
		opdic.append({"frequency":FreqMap[w1],"name":orig_name, "word":w1, "compound":round(WordSentMap[w1]["compound"]/FreqMap[w1],2),"neg":round(WordSentMap[w1]["neg"]/FreqMap[w1],2),"neu":round(WordSentMap[w1]["neu"]/FreqMap[w1],2),"pos":round(WordSentMap[w1]["pos"]/FreqMap[w1],2), "graph":co_words_graph})

	print(json.dumps(opdic))

#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------component 3---------------------------------------------------------------------------------------

def IssueFiles_get_the_graph(FreqDic,thresh,useless_words,RelFreqDic):
	the_graph = []
	for word in FreqDic:
		if (FreqDic[word] >= thresh) and (FreqDic[word] > 1) and (word not in useless_words) and (word != "") and (word != "RT"):
			the_graph.append({"word":word, "mentions":FreqDic[word], "frequency":round(RelFreqDic[word],2)})

	return the_graph


def IssueFiles_analyze(issue, useless_words, issuesTweetsDic, DefIssWords, NewIssWords,name, IssueSentOutput, IssueRelFreqMap, orig_name, opdic):
	thresh = 0		
	FreqDic = {}		#Frequencies of words for each word present in the texts for that issue
	RelFreqDic = {}		#Relative Frequencies of words

	#--------------------------------------------------------------------------------------------------
	for line in issuesTweetsDic[issue]:		#For each text for that issue
		line = line.strip()
		l = line.split(" ")		# l = words in the text
		
		for word in l :		#For each word in l
			word = word.strip()
			if (word not in FreqDic) :
				FreqDic[word] = 0

			FreqDic[word] = FreqDic[word] + 1		#Updating frequency values for words

	frequencies = []		#List containing the different frequencies of words, used later for calculating the threshold frequency
	for word in FreqDic:
		if (word not in useless_words) and (word != "RT") and (word != "") and (FreqDic[word] not in frequencies):
			frequencies.append(FreqDic[word])

	frequencies.sort(reverse=True)

	try:
		thresh = frequencies[30]

	except:
		thresh = frequencies[int(len(frequencies)/2)]

	if thresh < 2:
		thresh = 2		

	#Threshold value for frequency is set beyond this point in the variable "thresh"

	s = 0
	d = 0


	for word in FreqDic:		#For each word present in the texts for the issue
		if word not in useless_words and word != "RT" and word != "" and FreqDic[word] >= thresh:		#If the word is valid and its frequency is more than the threshold frequency
			s = s + FreqDic[word]		#Add it's frequency to the sum
			d = d + 1		#Incremeent the denominator

	try:
		m = s/d
	except ZeroDivisionError:
		m = 0

	for word in FreqDic:
		try:
			RelFreqDic[word] = FreqDic[word]/m
		except ZeroDivisionError:
			RelFreqDic[word] = 0

	the_graph = IssueFiles_get_the_graph(FreqDic,thresh,useless_words,RelFreqDic)
	opdic.append({"name":orig_name, "word":issue, "mentions":IssueSentOutput[issue]["freq"], "frequency":round(IssueRelFreqMap[issue],2), "compound":round(IssueSentOutput[issue]["compound"],2), "neg":round(IssueSentOutput[issue]["neg"],2), "neu":round(IssueSentOutput[issue]["neu"],2), "pos":round(IssueSentOutput[issue]["pos"],2), "graph":the_graph})

	temp_list = []		#List of new words to be added for that issue
	issue_words = []		#List of all existing (default and otherwise) words for that issue as present in "DefIssWords.txt" and "NewIssWords.txt" files

	for word in DefIssWords[issue]:		#Adding each default word for that issue in the list of words for that issue
		issue_words.append(word)

	for word in NewIssWords[issue]:		#Adding each New word for that issue in the list of words for that issue
		issue_words.append(word)

	for word in FreqDic:		#For each word in the list of words for that issue as present in FreqDic
		if (FreqDic[word] >= 10 or RelFreqDic[word] >= 2) and (word not in useless_words) and (word != "") and (word != "RT") and ("@" not in word) and (word not in issue_words):		#If the word is valid AND it has a frequency greater than the threshold AND is not already present in the list of words for that issue
			temp_list.append(word)		#Add the word to the list of new words for that issue

	output = ""		#Output to be written into the "NewIssWords.txt" file

	for word in NewIssWords[issue]:		#For each word already present in the "NewIssWords.txt" file
		output = output + word + "," +str(round(NewIssWords[issue][word],2)) + ";"		#Add the word and it's score to the output

	if(len(temp_list) > 0):		#If there are some new words to be added
		new_word_list = POS.main(temp_list)		#List of only valid (common or proper nouns) words
		for word in new_word_list:		#For each word in list valid words
			if word not in issue_words:		#If the word is not already present for the issue and 
				output = output + word.strip() + ",0.98;"		#Add it to the output

	return output[:-1]		#Return the output with the last ";" removed

def IssueFiles_remove_non_cs_words(dic,NewIssWords,issuesTweetsDic,useless_words):
	common_words = []		#List of words that are not particular to that issue
	IssueWordsRelFreqDic = {}		#Dictionary containing words for each of the issues and their relative frequencies

	for issue in dic:		#For each issue in the "dic" dictionary
		IssueWordsRelFreqDic[issue] = {}
		for line in issuesTweetsDic[issue]:		#For each text in the list of texts for that issue
			line = modifications.modify(line)		#Modify the text as in "modifciations.modify()"
			word_list = line.split(" ")		#Get the list of words in the text
		
			for word in word_list:		#For each word
				if word not in useless_words:		#If the word is not in uselesswords
					if word not in IssueWordsRelFreqDic[issue]:
						IssueWordsRelFreqDic[issue][word] = 0

					IssueWordsRelFreqDic[issue][word] = IssueWordsRelFreqDic[issue][word] + 1		#Update the frequency

	for issue in IssueWordsRelFreqDic:
		s = 0		#s = Sum of frequencies of all the words in tempDic (dic) for that particular issue
		d = 0		#d = Number of words for that particular issue
		for word in IssueWordsRelFreqDic[issue]:		#For each word in for that issue in tempDic (dic)
			s = s + IssueWordsRelFreqDic[issue][word]		#Add the frequency of that word to s
			d = d + 1		#Increment the counter for number of words

		avg = s/d		#Average Frequency of all the words for that particular issue

		for word in IssueWordsRelFreqDic[issue]:
			IssueWordsRelFreqDic[issue][word] = round(IssueWordsRelFreqDic[issue][word] / avg,2)		#Transform frequency to relative frequency

	for issue1 in dic:		#For each issue in tempDic (dic)
		for word in dic[issue1]:		#For each word in that particular issue
			cnt = 0
			for issue2 in NewIssWords:		#For each issue other than issue1
				if issue1 != issue2:
					try:
						if IssueWordsRelFreqDic[issue2][word] > 1 :
							cnt = cnt + 1

					except KeyError:
						continue

			if cnt >= 2:
				common_words.append(word)

	return common_words


def IssueFiles_main(name, IssueSentOutput, IssueRelFreqMap, orig_name, DefIssueFile, NewIssueFile, line_list):
	opdic = []

	name = re.sub(" ", "", name)
	
	issuesDic = {}		#Dict containing the various issues and their words

	DefIssWords = {}	#Dict containing issues and their words as appearing in "DefIssueWords.txt" file

	f = open("../data/" + DefIssueFile + ".txt", "r", encoding="utf-8")	#Reading the words for all issues in "DefIssueWords.txt" file

	for line in f.readlines():
		line = line.strip()
		l = line.split("\t")
		issue = l[0].strip()
		DefIssWords[issue] = []
		try:
			word_list = l[1].split(";")
		except:
			exit()

		for word in word_list:
			word = word.strip()
			DefIssWords[issue].append(word.upper())		#Every word is present in upper case

	f.close()

	NewIssWords = {}		#Dict containing the various issues, their words, and their scores as appearing in "NewIssWords.txt" file

	f = open("../data/" + NewIssueFile + ".txt", "r", encoding="utf-8")		#Reading the words for all issues in "NewIssWords.txt" file

	for line in f.readlines():
		line = line.strip()
		l = line.split("\t")
		issue = l[0].strip()
		NewIssWords[issue] = {}
		try:
			word_score_list = l[1].split(";")
		except IndexError:
			continue

		for word_score in word_score_list:
			try:
				word_score = word_score.strip()
				word  = word_score.split(",")[0]
				score = float(word_score.split(",")[1])
				if word not in NewIssWords[issue]:
					NewIssWords[issue][word] = score

			except:
				continue

	f.close()

	changed = {}		#Dict that maintains a record for whether the score of a word should be changed or not, initially, every word in each issue is assigned "False", i.e, no need for change
	for issue in NewIssWords:		#This dict contains all the words read from "NewIssWords.txt" file
		changed[issue] = {}
		for word in NewIssWords[issue]:
			changed[issue][word] = False

	#---------------------------------------------------------------------------------------------*


	#---------------------------------------------List of useless Words--------------------------
	useless_words = []		#List containing all the useless words

	f = open("../data/uselessWords.txt","r",encoding="utf-8")		#Reading the useless words from "uselessWords.txt" file
	for line in f.readlines():
		line = line.strip().upper()
		useless_words.append(line)

	f.close()
	#--------------------------------------------------------------------------------------------
	
	issuesTweetsDic = {}		#Dict containing the various issues and a list of tweets on that issue
	for issue in DefIssWords:
		issuesTweetsDic[issue] = []

	#--------------------------------Reading the Twitter Data File--------------------------------

	
	#line_list = FetchTwitterData.main(name)		#Fetching data from the database

	#------------------Adding texts to the list of texts for each issue-------------------------

	for line in line_list:
		line = line.strip()
		l = line.split("\t")
		
		try:
			txt = modifications.modify(l[4].strip()).upper()		#Convert the text into uppercase
			created_at = l[5].split(" ")[0].strip()

			year = int(created_at.split("-")[0])
			month = int(created_at.split("-")[1])
			date = int(created_at.split("-")[2])

		except:
			continue


		for issue in DefIssWords:		#for each issue present in DefIssWords
			t = False		#This is used to avoid checking for the words in NewIssWords dictionary for a particular issue if one of the words in DefIssWords is already present in the text

			for word in DefIssWords[issue]:		#for each default word for that particular issue
				if word in txt:		#if the word is present in the text, that means the issue is present in the text
					issuesTweetsDic[issue].append(txt)		#Add the text to the list of texts for that issue
					t = True
					break

			if t == False:		#If None of the words in DefIssWords dictionary are present in the text
				for word in NewIssWords[issue]:		#for each word in NewIssWords for that particular issue
					if word in txt:		#if the word is present in the text, that means the issue is present in the text
						issuesTweetsDic[issue].append(txt)		#Add the text to the list of texts for that issue
						break

	#---------------------------------------------------------------------------------------------

	#-------------Modifying the scores for words in NewIssWords-----------------------------------

	for issue in DefIssWords:		#For each issue in DefIssWords (All issues)
		for word in NewIssWords[issue]:		#For each word in NewIssWords for that particular issue
			cnt = 0		#Counter for number of texts in which the particular word is present for that issue
			for text in issuesTweetsDic[issue]:		#For each text for that particular issue
				if word in text:		#If the word is present in the text
					cnt = cnt + 1		#Update count

			if cnt > len(issuesTweetsDic[issue])//2:		#If the word is present in more than half of the texts for that issue
				pass		#Add 0.04 to the earlier score

			else:		#If the word is not present in more than half of the texts for that issue
				NewIssWords[issue][word] = NewIssWords[issue][word] - 0.04		#Subtract 0.04 from the earlier score


		#------------------Removing the words which have a score lower than 0.02------------------------------------
		#for word in NewIssWords[issue]:		#For each word in the NewIssWords dictionary for the issue
		#	if NewIssWords[issue][word] < 0.2:		#if the score for that word is less than 0.02
				#del(NewIssWords[issue][word])		#Remove that particular word for the issue from NewIssWords dictionary

	tempDic = {}		#Dictionary of new words (already existing and new ones) to be added to "NewIssWords.txt" file. Note : This dict consists of both wanted and unwanted words

	for issue in DefIssWords:		#For each issue
		if(len(issuesTweetsDic[issue]) == 0):		#If there is no text for that particular issue
			continue		#Move on to the next issue

		else:		#There is text present for that issue
			words = IssueFiles_analyze(issue, useless_words, issuesTweetsDic, DefIssWords, NewIssWords, name, IssueSentOutput, IssueRelFreqMap, orig_name, opdic)		#Get the string of new words, along with their scores, to be added to "NewIssWords.txt" file for that issue. This list consists of both unwanted and wanted words

		if(words != None):		#If there are new words to be added, or if there already exist some old words in "NewIssWords.txt" file for the issue
			tempDic[issue] = []		#Dictionary for new words (already existing and new additions) for each issue

			l = words.split(";")		#Converting the output string back into a list of words
			for i in range(len(l)):
				l[i] = l[i].strip()
				w = l[i].split(",")[0].strip()
				if w != "" and w not in tempDic[issue]:		#If the word is not already added to the list in dic
					tempDic[issue].append(w)		#Add the word

	omit_list = IssueFiles_remove_non_cs_words(tempDic,NewIssWords,issuesTweetsDic,useless_words)		#Get the list of words among new issue words (already existing and new) which are common to all issues, only non common words are to be added to the output

	new_issue_output = ""

	for issue in NewIssWords:
		new_issue_output = new_issue_output + issue +"\t"

		for word in NewIssWords[issue]:
			new_issue_output = new_issue_output + word + "," + str(round(NewIssWords[issue][word],2)) + ";"

		try:
			for word in tempDic[issue]:
				if (word not in omit_list) and (word not in NewIssWords[issue]):
					new_issue_output = new_issue_output + word + ",0.98;"


			new_issue_output = new_issue_output[:-1] + "\n"

		except KeyError:
			new_issue_output = new_issue_output[:-1] + "\n"
			continue


	f = open("../data/" + NewIssueFile + ".txt", "w")
	f.write(new_issue_output)
	f.close()

	print(json.dumps(opdic))

def IssueSent(name,DefIssueFile,NewIssueFile,line_list):
	year_list = []		#List to store the range of years under which tweets are obtained

	issuesDic = {}		#Dict that stores the different issues and words corresponding to those issues

	#-------------------------------Creating the issuesDic Dict------------------------------------
	
	f = open("../data/" + DefIssueFile + ".txt", "r", encoding="utf-8")
	for line in f.readlines():
		line = line.strip()
		l = line.split("\t")
		issue = l[0].strip()
		issuesDic[issue] = []
		word_list = l[1].split(";")
		for i in range(len(word_list)):
			word_list[i] = word_list[i].strip()
			issuesDic[issue].append(word_list[i])

	f.close()

	f = open("../data/" + NewIssueFile + ".txt", "r", encoding="utf-8")
	for line in f.readlines():
		line = line.strip()
		l = line.split("\t")
		issue = l[0].strip()

		try:
			word_score_list = l[1].split(";")

		except:
			continue

		for i in range(len(word_score_list)):
			word = word_score_list[i].split(",")[0].strip()
			if word not in issuesDic[issue]:
				issuesDic[issue].append(word)

	f.close()

	#----------------------------------------------------------------------------------------------*

	#----------------------------Reading file to create a list of useless words--------------------*
	f = open("../data/uselessWords.txt", "r", encoding="utf-8")
	useless_words = []

	for line in f.readlines():
		line = line.strip()
		useless_words.append(line.upper())

	f.close()
	#----------------------------------------------------------------------------------------------*

	sid = SentimentIntensityAnalyzer()


	IssueSentMap = {}		#Dict that total stores Sentiment scores for issues
	IssueRelFreqMap = {}		#Dict that stores the frequency of occurrence for each issue; useful for normalizing sentiment scores

	for issue in issuesDic :
		IssueSentMap[issue] = {"freq" : 0, "compound" : 0, "neg" : 0, "neu" : 0, "pos" : 0}		#Initializing Sentiment scores for all issues


	#--------------------------------Reading the Twitter Data file----------------------------------
	#line_list = FetchTwitterData.main(name)
	#-----------------------------------------------------------------------------------------------

	FreqMap = {}

	for line in line_list:
		#--------getting the various twitter fields and modifying the tweet text--------------------
		try:
			line = line.strip()

			line = line.split("\t")
			text = line[4].strip()

			text = modifications.modify(text)

			word_list = text.split(" ")		#Create a list of all words in the tweet
			created_at = line[5].strip()


			date = created_at.split(" ")[0]
			date = date.split("-")
			year = int(date[0].strip())
			if year not in year_list:
				year_list.append(year)

			month = int(date[1].strip())

		except:
			continue

		#-------------------------------------belly of the beast-------------------------------------
		for i in range(len(word_list)):
			word_list[i] = word_list[i].strip().upper()		#Converts all words in word_list to uppercase

		for word in word_list :
			if word not in FreqMap :
				FreqMap[word] = 0		

			FreqMap[word] = FreqMap[word] + 1		#Update Frequency values for the words

		sent_scores = sid.polarity_scores(text)		#Get sentiment scores for the tweet text
		
		for issue in issuesDic :
			for issue_word in issuesDic[issue]:
				if issue_word.upper() in text.upper() :		#If an issue word matches, i.e, an issue is mentioned in the tweet
					IssueSentMap[issue]["freq"] = IssueSentMap[issue]["freq"] + 1		#Update frequency value for an issue
					IssueSentMap[issue]["compound"] = IssueSentMap[issue]["compound"] + sent_scores['compound']		#Update sentiment scores for the issue
					IssueSentMap[issue]["neg"] = IssueSentMap[issue]["neg"] + sent_scores['neg']
					IssueSentMap[issue]["neu"] = IssueSentMap[issue]["neu"] + sent_scores['neu']
					IssueSentMap[issue]["pos"] = IssueSentMap[issue]["pos"] + sent_scores['pos']

					break

	#--------------------------normalizing sentiment score------------------------------------------

	for issue in IssueSentMap:
		for sent in IssueSentMap[issue]:
			if sent != "freq" :
				try:
					IssueSentMap[issue][sent] = IssueSentMap[issue][sent] / IssueSentMap[issue]["freq"]

				except:
					continue

	#-------------------------Calculating Relative Frequencies---------------------------------------

	s = 0
	for issue in IssueSentMap :
		s = s + IssueSentMap[issue]["freq"]

	m = s/len(issuesDic)

	for issue in IssueSentMap :
		try:
			IssueRelFreqMap[issue] = IssueSentMap[issue]["freq"]/m

		except ZeroDivisionError:
			IssueRelFreqMap[issue] = 0

	return IssueSentMap,IssueRelFreqMap


def IssueSent_main(name,orig_name,DefIssueFile,NewIssueFile,line_list):
	IssueSentOutput,IssueRelFreqMap = IssueSent(name,DefIssueFile,NewIssueFile,line_list)
	IssueFiles_main(name, IssueSentOutput, IssueRelFreqMap, orig_name, DefIssueFile, NewIssueFile, line_list)

#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------component 4--------------------------------------------------------------------------------------

def TimeLine_get_interval(d1,d2):
	return (d2 - d1).days

def TimeLine_analyze(d,text_list,n,issuesDic,issue_list,words,name):
	if(len(text_list) > 0):
		IssueFreqMap = {}
		IssueRelFreqMap = {}
		WordFreqMap = {}
		WordRelFreqMap = {}

		for issue in issue_list:
			IssueFreqMap[issue] = 0
			IssueRelFreqMap[issue] = 0

		for word in words:
			WordFreqMap[word] = 0
			WordRelFreqMap[word] = 0

		#---------------------------Calculating frequencies for issues---------
		for tweet in text_list:
			for issue in issue_list:
				for word in issuesDic[issue]:
					if word.upper() in tweet.upper():
						IssueFreqMap[issue] = IssueFreqMap[issue] + 1
						break

		#---Calculating frequencies for words (as sent by WFnGF.py)------------
		for tweet in text_list:
			tweet = tweet.upper()
			for word in words:
				word = word.upper()
				if word in tweet:
					WordFreqMap[word] = WordFreqMap[word] + 1

		#-----------------Calculating Relative Frequencies for issues----------
		s = 0

		for issue in issue_list:
			s = s + IssueFreqMap[issue]

		m = s/len(IssueFreqMap)

		for issue in issue_list:
			try:
				IssueRelFreqMap[issue] = IssueFreqMap[issue] / m
			except ZeroDivisionError:
				continue

		#---------------------------------------------------------------------*

		#-----------------Calculating Relative Frequencies for words----------
		s = 0

		for word in words:
			s = s + WordFreqMap[word]

		m = s/len(WordFreqMap)

		for word in words:
			try:
				WordRelFreqMap[word] = WordFreqMap[word] / m
			except ZeroDivisionError:
				continue
		#--------------------------------------------------------------------*


		op_dic = collections.OrderedDict({"date":"{}{}{}".format(str(d.year).zfill(4),str(d.month).zfill(2),str(d.day).zfill(2)), "Tweets":str(round(len(text_list)*100/n,2))})

		for issue in issue_list:
			op_dic[issue] = str(round(IssueRelFreqMap[issue],2))

		for word in words:
			op_dic[word] = str(round(WordRelFreqMap[word],2))

		return op_dic


	else:
		op_dic = collections.OrderedDict({"date":"{}{}{}".format(str(d.year).zfill(4),str(d.month).zfill(2),str(d.day).zfill(2)), "Tweets":str(0)})

		for issue in issue_list:
			op_dic[issue] = str(0)

		for word in words:
			op_dic[word] = str(0)

		return op_dic

def TimeLine_GetMostFrequentWords(line_list):
	f = open("../data/uselessWords.txt", "r", encoding="utf-8")

	useless_words = []

	for line in f.readlines():
		line = line.strip()
		useless_words.append(line.upper())
	#-------------------------------------------------------------------------------------------

	FreqMap = {}		#Dict for frequencies of each word

	#line_list = FetchTwitterData.main(name)

	#for line in line_list:
	#	print(line)

	#--------------------Getting Required Fields from the tweet data----------
	for line in line_list:
		try:
			line = line.strip()
			line = line.split("\t")
			text = line[4].strip()
			text = modifications.modify(text)

			word_list = text.split(" ")	#Getting a list of words in the tweet

			created_at = line[5].strip()
			date = created_at.split(" ")[0]
			date = date.split("-")

			year = int(date[0].strip())		#year of creation for the tweet

			month = int(date[1].strip())	#month of creation for the tweet

		except:
			continue

		#----------------------Converting all words in wordlist to upper case-----------------------
		for i in range(len(word_list)):
			word_list[i] = word_list[i].strip().upper()	
		#-------------------------------------------------------------------------------------------*

		#-------------------Updating Dict for words and their frequencies---------------------------
		for word in word_list :
			if (word not in FreqMap):
				FreqMap[word] = 0

			FreqMap[word] = FreqMap[word] + 1
		#-------------------------------------------------------------------------------------------*

	#----------Getting a list of different frequencies and calculating the threshold frequency------
	frequencies = []

	for word in FreqMap :
		if word not in useless_words and word != "" and word != "RT":
			if FreqMap[word] not in frequencies :
				frequencies.append(FreqMap[word])

	frequencies.sort(reverse=True)

	try:
		thresh = frequencies[30]

	except:	#If 30 different frequencies are unavailable, the median frequency is the threshold frequency
		thresh = frequencies[int(len(frequencies)/2)]

	#-----------------------------------------------------------------------------------------------*

	#-----------Writing the output of most frequent words with normalized sentiment scores----------

	freq_words = []
	cnt = 0
	for i in range(len(frequencies)):
		if frequencies[i] < thresh:
			break
			
		for word in FreqMap:
			if cnt == 40 :
				break

			elif FreqMap[word] == frequencies[i] and FreqMap[word] >= thresh and FreqMap[word] > 1 and word != "" and word != "RT" and word not in useless_words:
				freq_words.append(word)
				cnt = cnt + 1

	return freq_words


def TimeLine_main(name,line_list,orig_name,DefIssueFile,NewIssueFile):	#words contains the most frequently used words as obtained from WFnGF.py program

	words = TimeLine_GetMostFrequentWords(line_list)
	words.sort()

	issuesDic = {}		#Dict containing the issues and their words, as stored in IssueWords.txt file

	issue_list = []		#List containing the different issue headings

	#-----------------Reading the issues and their words from IssueWords.txt file to store in issuesDic-----------

	f = open("../data/" + DefIssueFile + ".txt", "r", encoding="utf-8")
	for line in f.readlines():
		line = line.strip()
		l = line.split("\t")
		issue = l[0].strip()
		issue_list.append(issue)
		issuesDic[issue] = []
		word_list = l[1].split(";")
		for i in range(len(word_list)):
			word_list[i] = word_list[i].strip()
			issuesDic[issue].append(word_list[i])

	f.close()

	f = open("../data/" + NewIssueFile + ".txt", "r", encoding="utf-8")
	for line in f.readlines():
		line = line.strip()
		l = line.split("\t")
		issue = l[0].strip()

		try:
			word_list = l[1].split(";")

		except:
			continue

		for i in range(len(word_list)):
			word = word_list[i].split(",")[0].strip()
			issuesDic[issue].append(word)

	f.close()


	issue_list.sort()

	f.close()
	#-------------------------------------------------------------------------------------------------------------*

	#line_list = FetchTwitterData.main(name)

	#--------------------------------------------Twitter Data File------------------------------------------------


	td_tuplist = []		#List of tuples in the following format: td_tuplist = [(tweet_text,tweet_year,tweet_month,tweet_date),...]

	for line in line_list:
		l = line.split("\t")
		for i in range(len(l)):
			l[i] = l[i].strip()

		try:
			txt = modifications.modify(l[4].strip())
			ca = l[5].split(" ")[0]

		except IndexError:
			continue

		if ca == "None":
			continue

		year = int(ca.split("-")[0].strip())		#year of creating of the tweet
		month = int(ca.split("-")[1].strip())		#month of creation of the tweet
		date = int(ca.split("-")[2].strip())		#date of creation of the tweet

		if txt == "":
			continue

		td_tuplist.append((txt,year,month,date))

	n = len(td_tuplist)

	curr_date = datetime.date(2005,1,1)

	op_dic = {"name":orig_name, "actual":[]}

	for i in range(len(td_tuplist)):
		elem = td_tuplist[i]

		if(datetime.date(elem[1],elem[2],elem[3]) > curr_date):
			curr_date = datetime.date(elem[1],elem[2],elem[3])
			temp_list = []
			text_list = []

			for j in range(i,len(td_tuplist)):
				new_date = datetime.date(td_tuplist[j][1],td_tuplist[j][2],td_tuplist[j][3])
				if new_date not in temp_list:		# and get_interval(curr_date,new_date) < 16 :
					temp_list.append(new_date)

				text_list.append(td_tuplist[j][0])

				if TimeLine_get_interval(curr_date,new_date) >15 :		#If the interval between two dates is 16 days
					temp_list.pop()		#Reduce the interval to an interval of 15 days
					text_list.pop()		#Remove the last tweet (which was included for an interval of 16 days)
					op_dic["actual"].append(TimeLine_analyze(curr_date,text_list,n,issuesDic,issue_list,words,name))
					break

		else:
			continue

	
	print(json.dumps(op_dic))

#------------------------------------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------component 5--------------------------------------------------------------------------------------

def Map_top_words(Dic):
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


def Map_main(name,orig_name,line_list):
	LocCoords = {}

	f = open("../pyt/Core/LocCoord.txt", "r", encoding="utf-8")
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
	#line_list = FetchTwitterData.main(name)
	#----------------------------------------------------------

	y = line_list
	sample_text = ""
	for i in y:
		sample_text = sample_text + i

	custom_sent_tokenizer  = PunktSentenceTokenizer(train_text)
	tokenized = custom_sent_tokenizer.tokenize(sample_text)
	LocDic = {}

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
		word_list = Map_top_words(LocDic[loc]["word_freq"])
		opdic.append({"pol_name":orig_name, "name":loc, "compound":LocDic[loc]["comp"], "frequency":LocDic[loc]["freq"], "position":{"lat":LocDic[loc]["lat"], "lng":LocDic[loc]["long"]}, "words":word_list})

	print(json.dumps(opdic))



#------------------------------------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------component 6--------------------------------------------------------------------------------------

def WordInsights(line_list,word,name):
	sid = SentimentIntensityAnalyzer()
	dic = {"freq" : 0, "comp" : 0, "neg" : 0, "neu" : 0, "pos" : 0}

	#line_list = FetchTwitterData.main(name)

	cnt = 0

	for line in line_list:
		line = line.strip()
#		try:
		txt = line.split("\t")[4].strip()
		if word.upper() in txt.upper():
			cnt = cnt + len(re.findall(word.upper(), txt.upper()))
			dic["freq"] = dic["freq"] + 1
			sent_scores = sid.polarity_scores(txt)
			dic["comp"] = dic["comp"] + sent_scores['compound']
			dic["neg"] = dic["neg"] + sent_scores['neg']
			dic["neu"] = dic["neu"] + sent_scores['neu']
			dic["pos"] = dic["pos"] + sent_scores['pos']
#		except:
#			pass


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

#------------------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------component 7--------------------------------------------------------------------------------------

def WordAssoc(line_list,word1,word2,name):
	word1_tot = 0
	word1_word2 = 0

	word2_tot = 0
	word2_word1 = 0

	tot = 0

	sid = SentimentIntensityAnalyzer()

	#line_list = FetchTwitterData.main(name)

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
		no_result = {"no_result": True}
		print(json.dumps(no_result))

#------------------------------------------------------------------------------------------------------------------------------------------------------------