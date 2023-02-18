'''
Class for Epub entry
'''
# import lxml.etree.ElementTree as ET
from lxml import etree
import lxml
import unittest

from .entry import Entry
from . import constants
from . import exceptions


class ContainerEntry(Entry):
    def __init__(self, data):
        Entry.__init__(self)

        self._data = data
        self._path = constants.CONTAINER_LOCATION
        self.root_file = None

        self.parse()

    def parse(self):
        '''
        Parse the container file into an xml tree
        '''
        xml_string = self._data.decode()

        try:
            # print(xml_string)
            elem = etree.fromstring(xml_string)

            # print(elem.items())
            # print(elem.tag)

            # Use namespace to search
            namespace = {"d": constants.CONTAINER_NS}
            elem = elem.find('d:rootfiles/d:rootfile', namespace)

            # print(elem.items())
            # print(type(elem.items()))

            self.root_file = next(
                (item[1] for item in elem.items() if item[0] == 'full-path'),
                None)
        # except xml.etree.ElementTree.ParseError:
        except Exception:
            raise


class TestContainerEntry(unittest.TestCase):
    def test_load(self):
        data = b'''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
	<rootfiles>
		<rootfile full-path="package.opf" media-type="application/oebps-package+xml"/>
	</rootfiles>
</container>'''
        obj = ContainerEntry(data=data)
        self.assertEqual(obj.root_file, 'package.opf')

    def test_load_malformed(self):
        data = b'''<?xml version="1.0"?>
</container>'''
        self.assertRaises(Exception, ContainerEntry.__init__, data=data)

    def test_load_none(self):
        data = b'''<?xml version="1.0"?>
</container>'''
        self.assertRaises(Exception, ContainerEntry.__init__)


if __name__ == "__main__":
    unittest.main()
