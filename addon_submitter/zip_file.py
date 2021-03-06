# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com
"""Module for working with zipped addons"""

from hashlib import md5
from xml.dom.minidom import parse
from zipfile import ZipFile
from typing import Union, BinaryIO
from django.core.files import File
from django.db.models import FileField

__all__ = ['ZippedAddon']


class ZippedAddon:
    """Represents a zipped addon"""
    def __init__(self, fo: Union[BinaryIO, File, FileField]) -> None:
        """
        :param fo: file-like object with zipped addon
        :raises FileNotFoundError: if zip has no addon.xml file
        :raises AttributeError: if an invalid file-like object is supplied
        :raises zipfile.BadZipFile: if a file-like object does not contain
            a zip archive.
        """
        self._md5 = md5(fo.read()).hexdigest()
        fo.seek(0)
        self._zipfile = ZipFile(fo)
        self._id = None
        self._version = None
        self._is_folder = False
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
                self._is_folder = True
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
    def is_folder(self) -> bool:
        """
        :return: if addon is zipped in a folder
        """
        return self._is_folder

    @property
    def md5(self) -> str:
        """
        :return: MD5 hexdigest of an archive file
        """
        return self._md5

    def extract(self, path: str = None) -> None:
        """
        Extract archive

        :param path: directory to extract the zip to
        """
        self._zipfile.extractall(path)
