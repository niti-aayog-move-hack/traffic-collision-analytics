import importlib.machinery
import sys
import re

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\LifeAnalytics\SaaS\La v0.2 - With Core\pyt\Core\Progs.py')
core_programs = loader.load_module('report')

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\LifeAnalytics\SaaS\La v0.2 - With Core\pyt\Core\FetchTwitterData.py')
FetchTwitterData = loader.load_module('report')

name = sys.argv[1].strip()
name = re.sub(" ", "", name)
word1 = sys.argv[2].strip()
word2 = sys.argv[3].strip()

line_list = FetchTwitterData.main(name)

core_programs.WordAssoc(line_list, word1, word2, name)