"""
    Module containing objects that represent Paginations

    Paginator : class
    StyledPaginator : class

"""

from math import ceil
# from xml.etree import ElementTree as ET


class Paginator(object):
    """ Object that handles logic of what pages are shown
        Credit to: Armin Ronacher
    """

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def n_pages(self):
        """ The number of pages total for the Pagination """
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.n_pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """ Generator to return pages that should be displayed """
        last = 0
        for num in range(1, self.n_pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and
                num < self.page + right_current) or \
               num > self.n_pages - right_edge:

                if last + 1 != num:
                    yield None
                yield num
                last = num
