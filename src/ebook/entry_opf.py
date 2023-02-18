'''
Class for Epub entry
'''
from lxml import etree
# import lxml.etree.ElementTree as ET
import lxml
import unittest
import re
from io import BytesIO

from .entry import Entry
from . import constants
from . import exceptions
from .util import namespace_from_tag


class OpfEntry(Entry):
    def __init__(self, path, data):
        Entry.__init__(self)

        self._data = data
        self._path = path

        self._mimes = {}

        self.parse()

    def parse(self):
        '''
        Parse the container file into an xml tree
        '''
        try:
            tree = etree.parse(BytesIO(self._data))
            # elem = etree.fromstring(self._data)
            print(tree.docinfo.encoding)
            elem = tree.getroot()
            items = elem.findall('manifest/item', elem.nsmap)
            for item in items:
                entry_href = ''
                entry_type = ''
                # TODO: Can this be made concise?
                for name, value in item.items():
                    print(name, value)
                    if name == "href":
                        entry_href = value
                    if name == "media-type":
                        entry_type = value
                self._mimes[entry_href] = entry_type
            print(self._mimes)

            # TODO: Encoding how to avoid hard-coding
            # etree.ElementTree(elem).write(
            #    'out.xml', xml_declaration=True, encoding='unicode')

        except Exception:
            raise   # exceptions.ParseError from parse_error


class TestOpfEntry(unittest.TestCase):
    def test_load(self):
        data = b'''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
	<rootfiles>
		<rootfile full-path="package.opf" media-type="application/oebps-package+xml"/>
	</rootfiles>
</container>'''
        obj = OpfEntry(data=data)
        self.assertEqual(obj.root_file, 'package.opf')

    def test_load_malformed(self):
        data = b'''<?xml version="1.0"?>
</container>'''
        self.assertRaises(Exception, OpfEntry.__init__, data=data)

    def test_load_none(self):
        data = b'''<?xml version="1.0"?>
</container>'''
        self.assertRaises(Exception, OpfEntry.__init__)


if __name__ == "__main__":
    unittest.main()
