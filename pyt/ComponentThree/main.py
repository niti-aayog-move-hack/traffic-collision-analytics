import importlib.machinery
import sys
import re

name = sys.argv[1].strip()
orig_name = name
name = re.sub(" ", "", name)


new_loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\Production_LA\pyt\Core\FetchTwitterData.py')
FetchTwitterData = new_loader.load_module('report')

line_list = FetchTwitterData.main(name)

loader = importlib.machinery.SourceFileLoader('report', r'C:\Users\Nadig\Dropbox\Production_LA\pyt\Core\Progs.py')
Progs = loader.load_module('report')

Progs.IssueSent_main(name, orig_name, "DefIssueWords", "NewIssueWords", line_list)