import re
import os, sys, subprocess, time
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtXml import QDomNode

import requests
from bs4 import BeautifulSoup

from MainWindow import Ui_MainWindow

ROOT_URL = 'http://horriblesubs.info'
ALL_SHOWS = ROOT_URL + '/shows/'
API_URL = 'https://horriblesubs.info/api.php?method=getshows&type=show&showid={}&nextid={}'


def open_magnet(magnet):
    """Open magnet according to os."""
    if sys.platform.startswith('linux'):
        subprocess.Popen(['xdg-open', magnet],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif sys.platform.startswith('win32'):
        os.startfile(magnet)
    elif sys.platform.startswith('cygwin'):
        os.startfile(magnet)
    elif sys.platform.startswith('darwin'):
        subprocess.Popen(['open', magnet],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        subprocess.Popen(['xdg-open', magnet],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class AnimeShow(QListWidgetItem):
    
    def __init__(self, show_link, title):
        super().__init__(title)
        self.show_link = show_link
        self.title = title

    def setText(self):
        return self.title

    def __str__(self):
        return '{} - {}'.format(self.title, self.show_link)

    def __repr__(self):
        return '{} - {}'.format(self.title, self.show_link)


class Episode(QListWidgetItem):
    
    def __init__(self, title, magnet):
        super().__init__(title)
        self.title = title
        self.magnet = magnet
    
    def __str__(self):
        return '{} - {}'.format(self.title, self.magnet)

    def __repr__(self):
        return '{} - {}'.format(self.title, self.magnet)


def get_episodes(show, quality=1080):
    
    html = requests.get(ROOT_URL + show['href']).text
    soup = BeautifulSoup(html, 'lxml')
    main_div = soup.find('div', class_='entry-content')
    script_block = main_div.find('script').text
    show_id = re.findall('\d+', script_block)[0]

    next_iter = 0
    result = list()
    while True:
        api = API_URL.format(show_id, next_iter)
        html = requests.get(api).text
        soup = BeautifulSoup(html, 'lxml')
        if soup.body.text == 'DONE':
            return result
        links = soup.find_all(class_='rls-info-container')
        for link in links:

            quality_block = link.find('div', class_='link-{}p'.format(quality))
            _link = quality_block.find(title='Magnet Link')

            title = '{} - {}'.format(show.get('title'), link.get('id'))

            episode = Episode(title, _link.get('href'))
            result.append(episode)

        next_iter += 1


def matched_shows(search):
    html = requests.get(ALL_SHOWS).text
    soup = BeautifulSoup(html, 'lxml')
    
    main_div = soup.find('div', class_='post-inner-content')
    _matched_shows = main_div.find_all('a', title=re.compile('(?i){}'.format(search)))
    result = list()
    for show in _matched_shows:
        anime_show = AnimeShow(show, show.text)
        result.append(anime_show)
    return result


class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loadingStatus.setVisible(False)

        self.animeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.animeView.doubleClicked.connect(self.display_episodes)
        self.searchField.installEventFilter(self)
        self.searchButton.clicked.connect(self.fill_table)
        self.showEpisodes.clicked.connect(self.display_episodes)
        self.downloadButton.clicked.connect(self.download_selected)
        self.selectAll.clicked.connect(self.select_all)
        self.deselectAll.clicked.connect(self.deselect_all)
    
    def eventFilter(self, widget, event):
        if event.type() == QEvent.KeyPress and widget is self.searchField:
            key = event.key()
            if key == Qt.Key_Return:
                self.fill_table()
        return QWidget.eventFilter(self, widget, event)

    def fill_table(self):
        self.animeView.clear()
        self.loadingStatus.setVisible(True)
        if self.searchField.text() == '':
            return
        shows = matched_shows(self.searchField.text())
        for show in shows:
            self.animeView.addItem(show)
        self.loadingStatus.setVisible(False)

    def display_episodes(self):
        selected_item = self.animeView.selectedItems()[0]
        self.animeView.clear()
        self.loadingStatus.setVisible(True)
        episodes = get_episodes(selected_item.show_link)
        for episode in episodes:
            self.animeView.addItem(episode)
        self.loadingStatus.setVisible(False)
    
    def download_selected(self):
        items = self.animeView.selectedItems()
        for item in items:
            open_magnet(item.magnet)
    
    def select_all(self):
        self.animeView.selectAll()
    
    def deselect_all(self):
        self.animeView.clearSelection()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())