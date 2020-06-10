FIRSTPAGE = 0
NEXTPAGE = 1
PREVIOUSPAGE = 2
ANOTHERPAGE = 3
LASTPAGE = 4


class Paging:
    def __init__(self, streamResult, nbRes=0, resultsByPage=10):
        self.nbRes = nbRes
        self.streamResult = streamResult
        self.curPage = 0
        self.start = 0
        self.end = 0
        self.setResultPerPage(resultsByPage)

    def setResultPerPage(self, resultsByPage):
        self.resultsByPage = resultsByPage
        self.nbPages = (self.nbRes - 1) // self.resultsByPage + 1
        newPage = (self.start // resultsByPage) + 1
        self.setPage(newPage)

    def setPage(self, page):
        if self.nbPages < 1:
            return
        if page < 1:
            raise ValueError("Page number should be > 0")
        if page > self.nbPages:
            raise ValueError("Maximum page number is %d" % self.nbPages)
        self.curPage = page
        self.start = self.resultsByPage * (page - 1) + 1
        self.end = self.start + self.resultsByPage - 1
        if self.end > self.nbRes:
            self.end = self.nbRes
        return True

    def showResults(self):
        self.streamResult()

    def previous(self):
        res = False
        if self.curPage > 1:
            res = self.setPage(self.curPage - 1)
        else:
            print("Already on the first page")
        return res

    def next(self):
        res = False
        if self.curPage == self.nbPages and self.curPage != 0:
            print("Already on the last page")
        else:
            res = self.setPage(self.curPage + 1)
        return res

    def moveTo(self, direction):
        if direction == ANOTHERPAGE:
            page = 0
            previousError = None
            res = None
            while page == 0 or not res:
                if previousError:
                    print(f"! {previousError}")
                page = input("Page number: ").strip().replace(" ", "")
                if not page.isnumeric():
                    page = 0
                else:
                    page = int(page)
                    try:
                        res = self.setPage(page)
                    except ValueError as err:
                        previousError = str(err)
            return res
        elif direction == FIRSTPAGE:
            return self.setPage(1)
        elif direction == LASTPAGE:
            return self.setPage(self.nbPages)
        else:
            return self.previous() if direction == PREVIOUSPAGE else self.next()

    def currentPosition(self) -> str:
        return f"Page: {self.curPage}/{self.nbPages}, {self.nbRes} résultats ({self.start}-{self.end})"
