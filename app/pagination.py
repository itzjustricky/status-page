"""
    Module containing objects that represent Paginations

    Paginator : class
    StyledPaginator : class

"""

from math import ceil


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
                   right_current=2, right_edge=2):
        """ Generator to return pages that should be displayed

        :param left_edge: the # of pages on
        """
        last = 0
        for num in range(1, self.n_pages + 1):
            if num <= left_edge or \
               (num >= self.page - left_current and
                num <= self.page + right_current) or \
               num > self.n_pages - right_edge:

                # if pages are not consecutive
                if last + 1 != num:
                    yield None
                yield num
                last = num

    def info(self):
        start_row = (self.page - 1) * self.per_page + 1
        end_row = min(self.page * self.per_page, self.total_count)
        return "Showing {} to {} of {} rows".format(
            start_row, end_row, self.total_count)


class StaticPaginator(Paginator):
    """ Paginator that follows a scheme to create a
        fixed number of page links
    """

    def iter_pages(self, n_tiles_shown=7):
        """ Generator to return pages that should be displayed
            preference would be given to left-current for pages
        :param n_tiles_shown: refers to the # of values returned
            by the generator (including None)
        """

        if n_tiles_shown < 7:
            raise ValueError("There must be at least 7 pages shown "
                             "for the StaticPaginator.")

        if self.total_count <= n_tiles_shown:
            for num in range(1, self.n_pages + 1):
                yield num
        else:
            last = 0
            edge = n_tiles_shown - 2
            # current page is at beginning of total pages
            if self.page < edge:
                for num in range(1, self.n_pages + 1):
                    if num <= edge or \
                       num == self.n_pages:

                        if last + 1 != num:
                            yield None
                        yield num
                        last = num
            # current page is at end of total pages
            elif self.page > (self.n_pages - edge + 1):
                for num in range(1, self.n_pages + 1):
                    if num == 1 or \
                       num > self.n_pages - edge:

                        if last + 1 != num:
                            yield None
                        yield num
                        last = num
            # current page is somewhere in the middle
            else:
                tiles_available = n_tiles_shown - 5
                right_current = tiles_available // 2
                left_current = tiles_available - right_current
                for num in range(1, self.n_pages + 1):
                    if num == 1 or \
                       (num >= self.page - left_current and
                        num <= self.page + right_current) or \
                       num == self.n_pages:

                        if last + 1 != num:
                            yield None
                        yield num
                        last = num
