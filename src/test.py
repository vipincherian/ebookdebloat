'''
Temporary test file for epub library

'''
# from zipfile import ZipFile
from ebook import Epub
import sys


# print('Test')

file_name = sys.argv[1]

print(sys.argv)

epub_file = Epub()
epub_file.load(file_name)
