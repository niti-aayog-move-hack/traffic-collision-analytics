
import re
from operator import itemgetter
import datetime

def main(name):
	f = open("../data/" + name + "TwitterData.txt", "r", encoding = 'utf-8')

	line_list = []
	cnt = 0	

	for line in f.readlines():
		if(len(line.split("\t")) != 14):
			continue
		
		line_list.append(line.split("\t"))

	for i in range(len(line_list)):
		try:
			dt = int(line_list[i][5].split("-")[2])
			mt = int(line_list[i][5].split("-")[1])
			yr = int(line_list[i][5].split("-")[0])
			line_list[i][5] = datetime.date(yr,mt,dt)
		except:
			continue



	line_list.sort(reverse=False, key=itemgetter(5))

	for i in range(len(line_list)):
		line_list[i][5] = str(line_list[i][5])
		line_list[i] = "\t".join(line_list[i])

	return line_list