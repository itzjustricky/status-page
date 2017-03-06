"""
    Some HTML-based objects to be passed
    into pandas DataFrame to be printed out


    @author: Ricky Chang
"""

import itertools
from xml.etree import ElementTree as ET


class HTMLPyObject(object):
    """ Object to serve as representation of HTML Object """

    def __init__(self, element, attrib=None, **kwargs):
        """
        :param element: the name of the element for the html object
        :param attrib: a dictionary of html attributes
            to be passed into the html object
        """
        if attrib is None:
            attrib = dict()
        elif not isinstance(attrib, dict):
            raise ValueError("The passed argument attrib was not of type dict")

        html_attrib = dict()
        for k, v in itertools.chain(attrib.items(), kwargs.items()):
            html_attrib[str(k)] = str(v)

        self._etree_obj = ET.Element(
            element, attrib=html_attrib)

    def sub_element(self, element, attrib=None, **kwargs):
        if attrib is None:
            attrib = dict()
        elif not isinstance(attrib, dict):
            raise ValueError("The passed argument attrib was not of type dict")

        html_attrib = dict()
        for k, v in itertools.chain(attrib.items(), kwargs.items()):
            html_attrib[str(k)] = str(v)

        return ET.SubElement(self._etree_obj, element, html_attrib)

    def __str__(self):
        return ET.tostring(self._etree_obj).decode()

    def __repr__(self):
        return str(self)


class HTMLImage(HTMLPyObject):
    """ Object to serve as representation of HTML Image """

    def __init__(self, src, attrib=None, **kwargs):
        attrib['src'] = src
        super(HTMLImage, self).__init__(self, 'img', attrib, **kwargs)

    def scale_image(self, width, height):
        self._etree_obj.set('width', str(width))
        self._etree_obj.set('height', str(height))
