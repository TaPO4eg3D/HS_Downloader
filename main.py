import re
import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile, QAbstractTableModel, Qt

import requests
from bs4 import BeautifulSoup

from MainWindow import Ui_MainWindow

ROOT_URL = 'http://horriblesubs.info'
ALL_SHOWS = ROOT_URL + '/shows/'

class AnimeShow:
    
    def __init__(self, show_id, title):
        self.show_id = show_id
        self.title = title
    
    @property
    def tuple(self):
        return (self.title, self.show_id)
    
    def __str__(self):
        return '{} - {}'.format(self.title, self.show_id)

    def __repr__(self):
        return '{} - {}'.format(self.title, self.show_id)

class Episode:
    
    API_URL = 'http://horriblesubs.info/lib/getshows.php?type=show&showid={}&nextid={}'

    def __init__(self, show_id, quality=1080):
        self.show_id = show_id

def matched_shows(search):
    html = requests.get(ALL_SHOWS).text
    soup = BeautifulSoup(html, 'lxml')
    
    main_div = soup.find('div', id='main')
    _matched_shows = main_div.find_all('a', title=re.compile('(?i){}'.format(search)))
    result = list()
    for show in _matched_shows:
        html = requests.get(ROOT_URL + show['href']).text
        soup = BeautifulSoup(html, 'lxml')
        main_div = soup.find('div', id='main')
        script_block = main_div.find('script').text
        show_id = re.findall('\d+', script_block)[0]

        anime_show = AnimeShow(show_id, show.text)
        result.append(anime_show)
    return result


class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self);

        headers = ['Наименование', 'Код']
        data_list = [('', '')]
        model = AnimeModel(self, data_list, headers)
        self.animeView.setModel(model)

        self.searchButton.clicked.connect(self.fill_table)
    
    def fill_table(self):
        headers = ['Наименование', 'Код']
        if(self.searchField.toPlainText() == ''):
            return
        shows = matched_shows(self.searchField.toPlainText())
        data_list = list()
        for show in shows:
            data_list.append(show.tuple)
        model = AnimeModel(self, data_list, headers)
        self.animeView.setModel(model)

class AnimeModel(QAbstractTableModel):
    
    def __init__(self, parent, mylist, header, *args):
        super().__init__(parent, *args)
        self.mylist = mylist
        self.header = header
    
    def rowCount(self, parent):
        return len(self.mylist)
    
    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]
    
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(SIGNAL("layoutChanged()"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())