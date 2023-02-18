'''
Temporary test file for epub library:w

'''
# from zipfile import ZipFile
from ebook import Epub
import sys


print('Test')

file_name =     sys.argv[1 ]

x = Epub()
x.load(file_name)

print(sys.argv)
