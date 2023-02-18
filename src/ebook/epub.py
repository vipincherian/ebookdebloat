'''
Class for Epub
'''

from zipfile import ZipFile
from . import constants
from . import exceptions
from .entry_container import ContainerEntry
from .entry_opf import OpfEntry


class Epub:
    '''
    Class docstring
    '''

    def __init__(self, file_name=''):
        self._archive = None
        if file_name != '':
            self.load(file_name)

        self._entries = {}

    def __del__(self):
        self.close()

    def close(self):
        '''
        Close the zip archive already loaded
        '''
        if self._archive is not None:
            self._archive.close()

    def load(self, file_name):
        '''
        Load from the file name specified
        '''
        self._archive = ZipFile(file_name, 'r')
        # self._archive.printdir()
        # map(print, self._archive.namelist())
        file_names = self._archive.namelist()

        # Load container

        if constants.CONTAINER_LOCATION not in file_names:
            raise exceptions.Error("Hello")

        # print(names)
        # print(self._archive.read(constants.CONTAINER_LOCATION))

        container = ContainerEntry(
            data=self._archive.read(constants.CONTAINER_LOCATION))
        print(container.root_file)

        self._entries[constants.CONTAINER_LOCATION] = container
        file_names.remove(constants.CONTAINER_LOCATION)

        # Load root OPF

        if container.root_file not in file_names:
            raise exceptions.Error("Root file not found")

        opf = OpfEntry(container.root_file,
                       self._archive.read(container.root_file))

        self._entries[container.root_file] = opf
        file_names.remove(container.root_file)

        print(self._entries)

if __name__ == "__main__":
    print("hello")
