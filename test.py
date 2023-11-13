class Search(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Поиск')
        uic.loadUi('image.ui', self)
        self.search_btn.clicked.connect(self.search_f)

    def search_f(self):
        query = self.search_text.text().lower()
        query = query.replace(' ', '+')
        url = f"https://minecraft.fandom.com/ru/wiki/{query}"
        resp = requests.get(url)
        if resp.status_code == 200:
            print(1)
        soup = BeautifulSoup(resp.content, "html.parser")
        i = soup.find('В')
        print(i)
        print(soup)

    def closeEvent(self, event):
        self.destroy()