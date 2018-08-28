import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import datetime
import modifications
import time
from operator import itemgetter

MonthMap = {"Jan" : 1, "Feb" : 2, "Mar":3, "Apr" : 4, "May" : 5, "Jun" : 6, "Jul" : 7, "Aug" : 8, "Sep" : 9, "Oct" : 10, "Nov" : 11, "Dec" : 12}


def get_url(site,query):
	global q1
	qarr = query.split()
	q = [x for x in qarr]
	q1 = site + '+'.join(q)
	if site=="http://www.ndtv.com/topic/":
		q1=q1 + "/news"
	return q1

def get_links(s,query,type,tag,name):
	if s=="http://www.indianexpress.com/?s=":
		return inexp_links(s,query,type,tag,name)
	if s=="http://m.moneycontrol.com/news_search.php?keyword=":
		return mctrl_links(s,query,type,tag,name)

def inexp_links(s,query,type,tag,name):
	global q2
	try:	
		search_url = get_url(s,query)
		s1 = [m.start() for m in re.finditer('/', q1)]
		q2 = q1[s1[1]+1:s1[2]]
		#print("\nCrawling site : "+q2)
		site = urllib.request.urlopen(search_url)
		the_links = []
		i=0		
		while i<3:
			if i>0:
				next = parsed.find('a',{'class':"next page-numbers"})
				if next==None:
					return the_links
				next=str(next)
				url=next[next.find('http'):next.find('>')-1]
				site = urllib.request.urlopen(url)
			data = site.read()			
			parsed = BeautifulSoup(data,"html.parser")			
			for links in parsed.findAll(tag, {type: re.compile(name)}):
					the_links.append(links.a['href'])
			i=i+1
		return the_links
			
	except:
		return

def mctrl_links(s,query,type,tag,name):
	global q2
	try:	
		search_url = get_url(s,query)
		s1 = [m.start() for m in re.finditer('/', q1)]
		q2 = q1[s1[1]+1:s1[2]]
		#print("\nCrawling site : "+q2)
		site = urllib.request.urlopen(search_url)
		the_links = []
		i=0		
		while i<3:
			if i>0:
				next ="http://m.moneycontrol.com/news_search.php?keyword="+query+"&start="+str(i+1)
				if next==None:
					return the_links
				
				site = urllib.request.urlopen(next)
			data = site.read()			
			parsed = BeautifulSoup(data,"html.parser")			
			for links in parsed.findAll(tag, {type: re.compile(name)}):
					the_links.append(links.a['href'])
			i=i+1
		return the_links
			
	except:	
		return
		


def extract_data(text,d):
	finger_print = "n"
	for i in range(0,len(text),10):
		finger_print = finger_print + text[i]
		if(len(finger_print) > 17):
			break

	return finger_print.lower(),text,str(d)

	"""
	print("-----------------------------------------")
	print("TExt : ", text)

	pat = re.compile("\"[^\"]*\"")
	quotes = pat.search(text)
	if quotes != None:
		quotes = quotes.groups()
	print("QUOTES : ", quotes)
	return None
	if(len(quotes) > 0):
		for i in range(len(quotes)):
			quotes[i] = modifications.modify(quotes[i])

		quotes = " ".join(quotes)		#merge all quotes into a single line separated by a space

	#	print("QUOTES : ", quotes)
	#	print("-----------------------------------------")

		return (str(d),quotes)

	else:
		return None
	"""

def get_data(qry,u, i):
	global MonthMap

	try:
		theurl = Request(u, headers = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' })
		html=urllib.request.urlopen(theurl)		#Fetches the website along with html tags
		data = html.read().decode('utf-8', 'ignore')
		soup=BeautifulSoup(data, 'html.parser')		#Creates a beautifulsoup object of the html page

		if "moneycontrol" in u :		#If the website is moneycontrol
			try:
				d = soup.find("div", {"class" : "gl10 PT5 PB10"}).text		#Date
				day = int(d.split(" ")[0].strip())		#date
				month = int(MonthMap[d.split(" ")[1].strip()])		#month
				year = int(d.split(" ")[2].strip())		#year

			except:		#Error in fetching data from moneycontrol website
				return

		elif "indianexpress" in u :		#If the website is indianexpress
			try:
				d = soup.find("span", {"itemprop" : "dateModified"}).text.strip()		#Date
				d = re.sub(":", " ", d)		#Removing the time part of "d"
				d = re.sub(r" [ ]+", " ", d)		#Removing unwanted spaces from the date
				month = MonthMap[d.split(" ")[1].strip()]		#month
				day = int(re.sub(",", "", d.split(" ")[2].strip()).strip())		#date
				year = int(d.split(",")[1].strip())		#year

			except:		#Error in fetching data from indianexpress website
				return

		date = datetime.date(year,month,day)		#Creating the datetime object

		try:
			res = [j.text.replace('\n', ' ').strip() for j in soup.find_all('p')]		#res = text of news article
			return(res[0],date)		#Return (news_text,date)
		
		except:
			return

	except:
		return

def insert_into_file(elem,f_line_list):
	pass
	"""
	date = elem[0]		#date of news article(a datetime object)
	quotes = elem[1]		#quotes present in the news article
	temp_list = []		#Consists of the tweets + news article in appropriate position
	val = False

	for line in f_line_list:
		line = line.strip()
		l = line.split("\t")
		if(len(l) != 14):
			continue

		for i in range(len(l)):
			l[i] = l[i].strip()

		try:
			f_tid = int(l[3])		#fetch the twitter id and convert it into int

		except:		#if the twitter id is not present in the correct place, add it to the temp_list and move on to the next line.
			temp_list.append(line)
			continue

		f_date = l[5].split(" ")[0].strip()		#date of the tweet
		f_date_y = int(f_date.split("-")[0].strip())		#year of the date of the tweet
		f_date_m = int(f_date.split("-")[1].strip())		#month of the date of the tweet
		f_date_d = int(f_date.split("-")[2].strip())		#day of the date of the tweet
		f_date = datetime.date(f_date_y,f_date_m,f_date_d)		#create a datetime object

		if(val == False and f_date < date):		#found the appropriate position for the news article. This happens when we find a tweet older than the news article. The news article is added before the tweet as contents in the file are in decreasing order of dates from top to bottom.
			date = str(date)		#converting the news article date back to a string
			for i in range(len(l)):
				l[i] = "-"
			l[4] = quotes.strip() + "bhenchod"
			l[5] = date + " -"
			text = "\t".join(l)		#Create a new line for the news article with all places filled with a "-" except the text and date part

			temp_list.append(text.strip())		#Add the news article 
			temp_list.append(line.strip())		#Add the tweet line
			val = True		#The news article has been added

		else:		#Haven't found the appropriate position. This happens when we're looking at tweets more recent than the news article.
			temp_list.append(line)		#add the tweet line to temp_list

	if i == len(f_line_list) and val == False:		#If we reach the end of file without finding a proper position for the news article, i.e, the news article is older than any of the existing tweets or news articles
		line = temp_list[-1]
		l = line.split("\t")
		l[4] = quotes
		
		temp = l[5].split(" ")
		temp[0] = str(date)
		l[5] = " ".join(temp)
		new_text = "\t".join(l)

		temp_list.append(new_text)
	"""


def get_most_recent_news(f_name):
	f = open(f_name, "r",encoding="utf-8")
	temp_list = []
	for line in f.readlines():
		temp_list.append(line.split("\t"))

	for i in range(len(temp_list)):
		dt = int(temp_list[i][5].split("-")[2])
		mt = int(temp_list[i][5].split("-")[1])
		yr = int(temp_list[i][5].split("-")[0])
		temp_list[i][5] = datetime.date(yr,mt,dt)

	news_art = None

	temp_list.sort(reverse=True, key=itemgetter(5))
	for i in range(len(temp_list)):
		if "-" in temp_list[i][0] and "-" in temp_list[i][1]:
			news_art = temp_list[i][3]
			break

	return news_art


def already_exists(news_search_keys, f_name):
	print("In already exists")
	most_recent_news = get_most_recent_news(f_name)		#Get the most recent news article
	if(most_recent_news) == None:		#If no recent tweets were found, it's the same case as first time.
		first_time(news_search_keys,f_name)

	done = False

	data_list = []
	text_date_list = []
	s_file = open("test_site.txt",'r')
	d_file = open("test_details.txt",'r')
	sites = s_file.read().split("\n")
	details = d_file.read().split("\n")
	type = [];tag = [];name = []
	for item in details:
		details_split = item.split(",")
		type.append(details_split[0])
		tag.append(details_split[1])
		name.append(details_split[2])
	queries = news_search_keys

	cnt = 0

	if queries:
		for iter in range(len(queries)):
			query = queries[iter]
			for j in range(len(sites)):
				url = get_links(sites[j],query,type[j],tag[j],name[j])
				if url:				
					for i in range(len(url)):
						gdr = get_data(query, url[i], i)		#gdr = news_text,date
						if gdr != None:
							edr = extract_data(gdr[0],gdr[1])		#edr = date,quotes(separated by spaces and symbol(") removed)
							if edr != None :
								print("News Count : ", cnt)
								cnt = cnt + 1
								#if difflib.SequenceMatcher(None,most_recent_news,edr[0]).ratio() > 0.95:
								if most_recent_news == edr[0] :
									done = True
									print("No new news articles")
									break

								if done == True:
									break
									
								data_list.append(edr)		#most recent news articles from multiple sources, fix this thing.

				else:		#No website in that source
					continue		#Move on to the next source

		if(len(data_list)>0):		#If There was some data extracted
			f = open(f_name, "r",encoding="utf-8")		#Read the lines from The already existing file with only tweets to line_list, which will ultimately contain the news articles and tweets merged together in the right order.
			lines_list = f.readlines()		#Add the lines (tweets) to lines_list

			for elem in data_list:		#For each (date,quotes_text) extracted from news articles, insert it into the file at appropriate position. The news article is present in the appropriate position in lines_list
				lines_list.append("-\t-\t-\t" + elem[0] + "\t" + elem[1] + "\t" + elem[2] + "\t-\t-\t-\t-\t-\t-\t-\t-\n")

			op = ""
			for line in lines_list:
				op = op + line

			f = open(f_name, "w")
			f.write(op)

		else:
			return

	else:
		return



def first_time(news_search_keys,f_name):
	print("In first time")
	data_list = []
	text_date_list = []
	s_file = open("test_site.txt",'r')
	d_file = open("test_details.txt",'r')
	sites = s_file.read().split("\n")
	details = d_file.read().split("\n")
	type = [];tag = [];name = []
	for item in details:
		details_split = item.split(",")
		type.append(details_split[0])
		tag.append(details_split[1])
		name.append(details_split[2])
	queries = news_search_keys

	print("Atleast i reached here")

	cnt = 0

	if queries:
		for iter in range(len(queries)):
			query = queries[iter]
			for j in range(len(sites)):
				url = get_links(sites[j],query,type[j],tag[j],name[j])
				if url:
					print("And maybe here")	
					for i in range(len(url)):
						gdr = get_data(query, url[i], i)		#gdr = news_text,date
						if gdr != None:
							edr = extract_data(gdr[0],gdr[1])		#edr = fingerprint,text,date removed)
							if edr != None :
								print("News Count : ", cnt)
								cnt = cnt + 1
							if cnt <= 10 :
								print("Not Appended!")
								continue
							else:
								data_list.append(edr)

							if cnt >= 20:
								break

				else:		#No website in that source
					continue		#Move on to the next source

		if(len(data_list)>0):		#If There was some data extracted
			f = open(f_name, "r",encoding="utf-8")		#Read the lines from The already existing file with only tweets to line_list, which will ultimately contain the news articles and tweets merged together in the right order.
			lines_list = f.readlines()		#Add the lines (tweets) to lines_list

			for elem in data_list:		#For each (date,quotes_text) extracted from news articles, insert it into the file at appropriate position. The news article is present in the appropriate position in lines_list
				lines_list.append("-\t-\t-\t" + elem[0] + "\t" + elem[1] + "\t" + elem[2] + "\t-\t-\t-\t-\t-\t-\t-\t-\n")

			op = ""
			for line in lines_list:
				op = op + line

			f = open(f_name, "w")
			f.write(op)

		else:
			return

	else:
		return



def main(news_search_keys,f_name,ft):
	if(ft == True):
		first_time(news_search_keys,f_name)

	else:
		already_exists(news_search_keys,f_name)