import importlib.machinery
import importlib.machinery
import re
import sys

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\LifeAnalytics\SaaS\La v0.2 - With Core\pyt\Core\Progs.py')
core_programs = loader.load_module('report')

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\LifeAnalytics\SaaS\La v0.2 - With Core\pyt\Core\FetchTwitterData.py')
FetchTwitterData = loader.load_module('report')


name = sys.argv[1].strip()
name = re.sub(" ", "", name)
word = sys.argv[2].strip()

line_list = FetchTwitterData.main(name)
core_programs.WordInsights(line_list,word,name)