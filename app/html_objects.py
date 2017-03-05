"""
    Some HTML-based objects to be passed
    into pandas DataFrame to be printed out


    @author: Ricky Chang
"""

import itertools
from xml.etree import ElementTree as ET


class HTMLImage(object):
    """ Object to serve as the HTML representation of an image """

    def __init__(self, src, attrib=None, **kwargs):
        """
        :param src: the source of where the image comes from
        :param attrib: a dictionary of html attributes
            to be passed into the html image
        """
        html_attrib = dict()
        if attrib is None:
            attrib = dict()
        elif not isinstance(attrib, dict):
            raise ValueError("The passed argument attrib was not of type dict")

        for k, v in itertools.chain(attrib.items(), kwargs.items()):
            html_attrib[str(k)] = str(v)

        self._src = src
        self._etree_obj = ET.Element(
            'img', src=src,
            attrib=html_attrib
        )

    @property
    def source(self):
        return self._src

    def scale_image(self, width, height):
        self._etree_obj.set('width', str(width))
        self._etree_obj.set('height', str(height))

    def __str__(self):
        return ET.tostring(self._etree_obj).decode()

    def __repr__(self):
        return str(self)
