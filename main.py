import re
import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtCore import *

import requests
from bs4 import BeautifulSoup

from MainWindow import Ui_MainWindow

ROOT_URL = 'http://horriblesubs.info'
ALL_SHOWS = ROOT_URL + '/shows/'
API_URL = 'https://horriblesubs.info/api.php?method=getshows&type=show&showid={}&nextid={}'

class AnimeShow(QListWidgetItem):
    
    def __init__(self, show_id, title):
        super().__init__(title)
        self.show_id = show_id
        self.title = title
    
    @property
    def tuple(self):
        return (self.title, self.show_id)

    def setText(self):
        return self.title

    def __str__(self):
        return '{} - {}'.format(self.title, self.show_id)

    def __repr__(self):
        return '{} - {}'.format(self.title, self.show_id)

class Episode:
    
    def __init__(self, title, magnet):
        self.title = title
        self.magnet = magnet
    
    def __str__(self):
        return '{} - {}'.format(self.title, self.magnet)

    def __repr__(self):
        return '{} - {}'.format(self.title, self.magnet)


def get_episodes(show_id, quality=1080):
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
            _title = link.get('id')
            episode = Episode(_title, _link.get('href'))
            result.append(episode)
        next_iter += 1

def matched_shows(search):
    html = requests.get(ALL_SHOWS).text
    soup = BeautifulSoup(html, 'lxml')
    
    main_div = soup.find('div', class_='post-inner-content')
    _matched_shows = main_div.find_all('a', title=re.compile('(?i){}'.format(search)))
    result = list()
    for show in _matched_shows:
        html = requests.get(ROOT_URL + show['href']).text
        soup = BeautifulSoup(html, 'lxml')
        main_div = soup.find('div', class_='entry-content')
        script_block = main_div.find('script').text
        show_id = re.findall('\d+', script_block)[0]

        anime_show = AnimeShow(show_id, show.text)
        result.append(anime_show)
    return result


class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self);
        self.searchButton.clicked.connect(self.fill_table)
        self.showEpisodes.clicked.connect(self.display_episodes)
    
    def fill_table(self):
        self.animeView.clear()
        if(self.searchField.toPlainText() == ''):
            return
        shows = matched_shows(self.searchField.toPlainText())
        print(shows)
        for show in shows:
            self.animeView.addItem(show)

    def display_episodes(self):
        selected_item = self.animeView.selectedItems()[0]
        print(selected_item.show_id)

if __name__ == "__main__":
    print(get_episodes(1075))
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    # sys.exit(app.exec_())