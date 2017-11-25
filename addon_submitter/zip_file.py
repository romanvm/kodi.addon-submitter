# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

from zipfile import ZipFile
from typing import BinaryIO
from xml.dom.minidom import parse


class ZippedAddon:
    """Represents a zipped addon"""
    def __init__(self, fo: BinaryIO):
        """
        :param fo: file-like object with zipped addon
        :raises FileNotFoundError: if zip has no addon.xml file
        """
        self._zipfile = ZipFile(fo)
        self._id = None
        self._version = None
        self._has_folder = False
        self._parse_zip()

    def _parse_zip(self):
        namelist = self._zipfile.namelist()
        for fn in namelist:
            if 'addon.xml' in fn:
                with self._zipfile.open(fn) as fo:
                    doc = parse(fo)
                    break
        else:
            raise FileNotFoundError('zip file has no addon.xml')
        self._id = doc.firstChild.getAttribute('id')
        self._version = doc.firstChild.getAttribute('version')
        for fn in namelist:
            if fn == self._id + '/':
                self._has_folder = True
                break

    @property
    def id(self) -> str:
        """
        :return: addon id
        """
        return self._id

    @property
    def version(self) -> str:
        """
        :return: addon version
        """
        return self._version

    @property
    def has_folder(self) -> bool:
        """
        :return: if addon is zipped in a folder
        """
        return self._has_folder
