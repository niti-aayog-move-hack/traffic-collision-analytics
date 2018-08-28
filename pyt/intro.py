import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
from difflib import SequenceMatcher
from urllib.parse import urlparse
import sys
import json

file = open("politicians.txt", "r")
opdic = []

partyList = {
			'BJP' : ['BJP', 'Bharatiya Janata'], 
			'INC' : ['INC', 'National Congress'], 
			'CPI-M' : ['CPI-M', 'Marxist'],
			'CPI' : ['CPI', 'Communist Party Of India'], 
			'BSP' : ['BSP', "Bahujan Samajwadi Party"],
			'NCP' : ['NCP', "Nationalist Congress Party"],
			'AAP' : ['AAP', "Aam Aadmi Party"],
			'AIADMK' : ['AIADMK', 'All India Anna Dravida Munnetra Kazhagam'],
			'AIFB' : ['AIFB', '	All India Forward Bloc'],
			'AIMIM' : ['AIMIM', 'All India Majlis-e-Ittehadul Muslimeen'],
			'AINRC' : ['AINRC', 'All India N.R. Congress'],
			'AITC' : ['AITC', 'All India Trinamool Congress', 'Trinamool'],
			'AIUDF' : ['AIUDF', 'All India United Democratic Front'],
			'AJSU' : ['AJSU', 'All Jharkhand Students Union'],
			'AGP' : ['AGP', 'Asom Gana Parishad'],
			'BJD' : ['BJD', 'Biju Janata Dal'],
			'BPF' : ['BPF', 'Bodoland People\'s Front'],
			'DMDK' : ['DMDK', 'Desiya Murpokku Dravidar Kazhagam'],
			'DMK' : ['DMK', 'Dravida Munnetra Kazhagam'],
			'HSPDP' : ['HSPDP', 'Haryana Janhit Congress (BL)'], 
			'INLD' : ['INLD', 'Indian National Lok Dal'], 
			'IUML' : ['IUML', 'Indian Union Muslim League'], 
			'JKNC' : ['JKNC', 'Jammu & Kashmir National Conference'], 
			'JKNPP' : ['JKNPP', 'Jammu & Kashmir National Panthers Party'], 
			'JKPDP' : ['JKPDP', 'Jammu and Kashmir People\'s Democratic Party'], 
			'JD(S)' : ['JD(S)', 'Janata Dal (Secular)'], 
			'JD(U)' : ['JD(U)', 'Janata Dal (United)'], 
			'JMM' : ['JMM', 'Jharkhand Mukti Morcha'], 
			'JVM(P)' : ['JVM(P)', 'Jharkhand Vikas Morcha (Prajatantrik)'], 
			'KC(M)' : ['KC(M)', 'Kerala Congress'], 
			'LJP' : ['LJP', 'Lok Janshakti'], 
			'MNS' : ['MNS', 'Maharashtra Navnirman Sena'], 
			'MGP' : ['MGP', 'Maharashtrawadi Gomantak'], 
			'MSCP' : ['MSCP', '	Manipur State Congress'], 
			'MNF' : ['MNF', 'Mizo National Front'], 
			'MPC' : ['MPC', 'Mizoram People\'s Conference'], 
			'NPF' : ['NPF', 'Naga People\'s Front'], 
			'NPP' : ['NPP', 'National People\'s Party'], 
			'PMK' : ['PMK', 'Pattali Makkal Katchi'],
			'PPA' : ['PPA', 'People\'s Party of Arunachal'], 
			'RJD' : ['RJD', 'Rashtriya Janata Dal'], 
			'RLD' : ['RLD', 'Rashtriya Lok Dal'], 
			'RLSP' : ['RLSP', 'Rashtriya Lok Samta Party'],
			'RSP' : ['RSP', 'Revolutionary Socialist Party'], 
			'SP' : ['SP', 'Samajwadi Party'], 
			'SAD' : ['SAD', 'Shiromani Akali Dal'], 
			'SS' : ['SS', 'Shiv Sena'], 
			'SDF' : ['SDF', 'Sikkim Democratic Front'], 
			'SKM' : ['SKM', 'Sikkim Krantikari Morcha'], 
			'TRS' : ['TRS', 'Telangana Rashtra Samithi'], 
			'TDP' : ['TDP', 'Telugu Desam Party'], 
			'UDP' : ['UDP', 'United Democratic Party'], 
			'YSRCP' : ['YSRCP', 'YSR Congress'], 
			'SJP' : ['SJP', 'Samajwadi Janata Party (Rashtriya)']
	}

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
	
def getTwtr(name):
	url = "https://twitter.com/search?f=users&vertical=news&q=" + "%20".join(name.split(' '))
	
	pol_words = ['official', 'minister', 'politician', 'member of parliment', 'member of legislative assembly']
	f = open("poltwtr.csv", 'a', encoding = 'utf-8')
	flag = open("flag.csv", 'a', encoding = 'utf-8')	
	try:
		site = urllib.request.urlopen(url)
		html = site.read()
		soup = BeautifulSoup(html,"html.parser")
		wholediv = [i.text.replace('\n', ' ').strip() for i in soup.find_all('div', class_= 'ProfileCard-userFields')]
		dispname = [i.text.replace('\n', ' ').strip() for i in soup.find_all('a', class_ = 'ProfileNameTruncated-link u-textInheritColor js-nav js-action-profile-name' )]
		handle = [i.text.replace('\n', ' ').strip() for i in soup.find_all('a', class_= 'ProfileCard-screennameLink u-linkComplex js-nav')]
		

		
		for i in range(min(10, len(wholediv))):
			
			if "Verified account" in wholediv[i] and similar(dispname[i], name) >= 0.8:
				f.write(name+','+handle[i])
				f.write('\n')
				break
			
			elif "Verified account" not in wholediv[i] and similar(dispname[i], name) >= 0.8:
				for iter in pol_words:
					if iter in wholediv[i].lower():
						f.write(name+','+handle[i])
						f.write('\n')
						break
					break
			
			elif "Verified account" in wholediv[i] and similar(dispname[i], name) <= 0.8:
				apndd = pol_words
				apndd.append(name)
				print(wholediv[i].lower())
				for iter in apndd:
					if iter in wholediv[i].lower():
						f.write(name+','+handle[i])
						f.write('\n')
						break
					break

			else:
				if name.lower() in wholediv[i].lower():
					for iter in pol_words:
						if iter in wholediv[i].lower():
							flag.write(name+','+handle[i])
							flag.write('\n')
							break
						break
				
	except Exception as e:
		print(e)
	
	f.close()
	flag.close()
	
def main():
	for line in file.readlines():
		line = line.strip()
		print(line)
		getTwtr(line)
		party = []
		url = 'https://en.wikipedia.org/wiki/'+line
		try:
			site = urllib.request.urlopen(url)
			html = site.read()
			soup = BeautifulSoup(html,"html.parser")
			res = [i.text.replace('\n', ' ').strip() for i in soup.find_all('p')]
			x = min(4, len(res))
			op = ""
			for iter in range(len(res)):
				if len(res[iter]) > 60:
					op = op + res[iter]
			
			result = op.split('.')
			fop = ""
			for iter in range(x):
				fop = fop + result[iter] + '.'
			
			fop = re.sub(r"\[[^\]]\]", "", fop)
			fop = re.sub("[^\u0000-\u007F]", "", fop)
			fop = re.sub("\([^\(\)]*[^\u0000-\u007F]+[^\(\)]*\)", "", fop)
			fop.encode('ascii', 'ignore').decode('ascii')
			
			for ls in partyList:
				for p in partyList[ls]:
					if p in fop and ls not in party:
						party.append(ls)
		except:
			pass
		opdic.append({"name":line, "party":party, "intro": fop})

	file.close()

	op = open("intro.json", "a", encoding = "utf-8")
	op.write(json.dumps(opdic))

main()