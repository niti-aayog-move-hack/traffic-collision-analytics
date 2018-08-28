import importlib.machinery
import sys
import re

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\Production_LA\pyt\Core\Progs.py')
core_programs = loader.load_module('report')

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\Production_LA\pyt\Core\FetchTwitterData.py')
FetchTwitterData = loader.load_module('report')

name = sys.argv[1].strip()
orig_name = name
name = re.sub(" ", "", name)

line_list = FetchTwitterData.main(name)

core_programs.Map_main(name,orig_name,line_list)