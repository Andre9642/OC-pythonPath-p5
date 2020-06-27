"""Paging module"""
from typing import Callable

FIRSTPAGE = 0
NEXTPAGE = 1
PREVIOUSPAGE = 2
ANOTHERPAGE = 3
LASTPAGE = 4


class Paging:
    """
    A class to display many items, on several pages
    """

    def __init__(self,
                 total_items: int=0,
                 items_by_page: int=10):
        self._total_items = total_items
        self._page = 0
        self._start = 0
        self._end = 0
        self.items_by_page = items_by_page

    @property
    def items_by_page(self):
        return self._items_by_page

    @items_by_page.setter
    def items_by_page(self, new_items_by_page: int):
        self._items_by_page = new_items_by_page
        self._nb_pages = (self.total_items - 1) // self._items_by_page + 1
        new_page = (self._start // new_items_by_page) + 1
        self.page = new_page

    @page.setter
    def page(self, page: int):
        if self.nb_pages < 1:
            return
        if page < 1:
            raise ValueError("Page number should be > 0")
        if page > self.nb_pages:
            raise ValueError("Maximum page number is %d" % self.nb_pages)
        self._page = page
        self._start = self._items_by_page * (page - 1) + 1
        self._end = self._start + self._items_by_page - 1
        if self._end > self.total_items:
            self._end = self.total_items
        return True

    def previous(self):
        res = False
        if self.page > 1:
            res = self.set_page(self.page - 1)
        else:
            print("Already on the first page")
        return res

    def next(self):
        res = False
        if self.page == self.nb_pages and self.page != 0:
            print("Already on the last page")
        else:
            res = self.set_page(self.page + 1)
        return res

    def move_to(self, direction: int):
        if direction == ANOTHERPAGE:
            page = 0
            previous_error = None
            res = None
            while page == 0 or not res:
                if previous_error:
                    print(f"! {previous_error}")
                page = input("Page number: ").strip().replace(" ", "")
                if not page.isnumeric():
                    page = 0
                else:
                    page = int(page)
                    try:
                        res = self.set_page(page)
                    except ValueError as err:
                        previous_error = str(err)
            return res
        elif direction == FIRSTPAGE:
            return self.set_page(1)
        elif direction == LASTPAGE:
            return self.set_page(self.nb_pages)
        else:
            return self.previous() if direction == PREVIOUSPAGE else self.next()

    def current_position(self) -> str:
        return f"Page: {self.page}/{self.nb_pages}, {self.total_items} résultats ({self._start}-{self._end})"

    def contextual_items(self):
        items = [("c",
                 f"Change the number of items per page (currently : {self._items_by_page})",
                 "change_number_results_per_page")]
        if self.page > 1:
            items.append(("f", "First page", "move_to", FIRSTPAGE))
            items.append(
                ("j", "Previous page", "move_to", PREVIOUSPAGE))
        if self.page != self.nb_pages:
            items.append(("k", "Next page", "move_to", NEXTPAGE))
            items.append(("l", "Last page", "move_to", LASTPAGE))
        if self.nb_pages > 1:
            items.append(
                ("p", "Another page", "move_to", ANOTHERPAGE))

