"""Paging module"""

FIRSTPAGE = 0
NEXTPAGE = 1
PREVIOUSPAGE = 2
ANOTHERPAGE = 3
LASTPAGE = 4


class Paging:
    """
    A class to display many items, on several pages
    """
    _page = 0
    _items_by_page = 10
    _nb_pages = 0
    _start = 0
    _end = 0

    def __init__(self,
                 total_items: int = 0,
                 items_by_page: int = 10):
        if not isinstance(total_items, int):
            raise TypeError(
                f"total_items must be an integer (not {type(total_items)} -> {total_items})")
        if not isinstance(items_by_page, int):
            raise RuntimeError(
                f"items_by_page must be an integer (not {type(items_by_page)})")

        self._total_items = total_items
        self.items_by_page = items_by_page

    @property
    def total_items(self):
        return self._total_items

    @property
    def items_by_page(self):
        return self._items_by_page

    @items_by_page.setter
    def items_by_page(self, new_items_by_page: int):
        self._items_by_page = new_items_by_page
        self._nb_pages = (self._total_items - 1) // self._items_by_page + 1
        new_page = (self._start // new_items_by_page) + 1
        self.page = new_page

    @property
    def page(self):
        return self._page

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @page.setter
    def page(self, page: int):
        if self._nb_pages < 1:
            return
        if page < 1:
            raise ValueError("Page number should be > 0")
        if page > self._nb_pages:
            raise ValueError("Maximum page number is %d" % self._nb_pages)
        self._page = page
        self._start = self._items_by_page * (page - 1) + 1
        self._end = self._start + self._items_by_page - 1
        if self._end > self.total_items:
            self._end = self.total_items
        return True

    def previous(self):
        res = False
        if self.page > 1:
            res = self.page = self.page - 1
        else:
            print("Already on the first page")
        return res

    def next(self):
        res = False
        if self.page == self._nb_pages and self.page != 0:
            print("Déjà sur la dernière page")
        else:
            res = self.page = self.page + 1
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
                        res = self.page = page
                    except ValueError as err:
                        previous_error = str(err)
            return res
        elif direction == FIRSTPAGE:
            self.page = 1
        elif direction == LASTPAGE:
            self.page = self._nb_pages
        else:
            self.previous() if direction == PREVIOUSPAGE else self.next()

    def current_position(self) -> str:
        return f"Page: {self.page}/{self._nb_pages}, {self.total_items} résultats ({self.start}-{self.end})"

    @property
    def contextual_items(self):
        items = []
        if self.total_items > 1:
            items.append((
                f"Changer le nombre d'éléments par page (actuellement : {self._items_by_page})",
                "c",
                "change_number_results_per_page"))
        if self.page > 1:
            items.append((
                "Première page",
                "f",
                "move_to",
                [FIRSTPAGE])
            )
            items.append((
                "Page précédente",
                "j",
                "move_to",
                [PREVIOUSPAGE])
            )
        if self.page != self._nb_pages:
            items.append((
                "Page suivante",
                "k",
                "move_to",
                [NEXTPAGE])
            )
            items.append((
                "Dernière page",
                "l",
                "move_to",
                [LASTPAGE])
            )
        if self._nb_pages > 1:
            items.append((
                "Autre page",
                "p",
                "move_to",
                [ANOTHERPAGE])
            )
        return items
