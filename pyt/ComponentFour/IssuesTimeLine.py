import importlib.machinery
import datetime
import re
import sys
import json
import collections

loader = importlib.machinery.SourceFileLoader('report', '/home/bhargav/Desktop/KAnOE/Platform/pyt/Core/modifications.py')
modifications = loader.load_module('report')

loader = importlib.machinery.SourceFileLoader('report', '/home/bhargav/Desktop/KAnOE/Platform/pyt/Core/FetchTwitterData.py')
FetchTwitterData = loader.load_module('report')

loader = importlib.machinery.SourceFileLoader('report', '/home/bhargav/Desktop/KAnOE/Platform/pyt/Core/Progs.py')
TimeLine = loader.load_module('report')

loader = importlib.machinery.SourceFileLoader('report', '/home/bhargav/Desktop/KAnOE/Platform/pyt/Core/FetchTwitterData.py')
FetchTwitterData = loader.load_module('report')

name = sys.argv[1].strip()
orig_name = name
name = re.sub(" ", "", name)

def get_interval(d1,d2):
	return (d2 - d1).days

def analyze(d,text_list,n,issuesDic,issue_list,words,name):
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


def get_most_frequent_words(name):
	#-------------------------Creating list of useless words------------------------------------
	f = open("../data/uselessWords.txt", "r", encoding="utf-8")

	useless_words = []

	for line in f.readlines():
		line = line.strip()
		useless_words.append(line.upper())
	#-------------------------------------------------------------------------------------------

	FreqMap = {}		#Dict for frequencies of each word

	line_list = FetchTwitterData.main(name)

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

	line_list = FetchTwitterData.main(name)

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

def main():	#words contains the most frequently used words as obtained from WFnGF.py program
	
	line_list = FetchTwitterData.main(name)
	#TimeLine.TimeLine_main(name,line_list,orig_name)
	#global name
	
	words = get_most_frequent_words(name)
	words.sort()

	issuesDic = {}		#Dict containing the issues and their words, as stored in IssueWords.txt file

	issue_list = []		#List containing the different issue headings

#-----------------Reading the issues and their words from IssueWords.txt file to store in issuesDic-----------

	f = open("../data/DefIssueWords.txt", "r", encoding="utf-8")
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

	f = open("../data/NewIssueWords.txt", "r", encoding="utf-8")
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

	line_list = FetchTwitterData.main(name)

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
	
	#arrange the tweets in old-new chronological order, as opposed to new-old order as stored in the Twitter data file

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

				if get_interval(curr_date,new_date) >15 :		#If the interval between two dates is 16 days
					temp_list.pop()		#Reduce the interval to an interval of 15 days
					text_list.pop()		#Remove the last tweet (which was included for an interval of 16 days)
					op_dic["actual"].append(analyze(curr_date,text_list,n,issuesDic,issue_list,words,name))
					break

		else:
			continue

	
	print(json.dumps(op_dic))

main()