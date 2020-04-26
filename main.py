import asyncio
import os
import re
import subprocess
import sys
import threading
import time

import aiohttp
import requests
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from bs4 import BeautifulSoup

from MainWindow import Ui_MainWindow

ROOT_URL = 'http://horriblesubs.info'
ALL_SHOWS = ROOT_URL + '/shows/'
API_URL = ROOT_URL + '/api.php?method=getshows&type=show&showid={}&nextid={}'

EPISODES = list()
QUALITIES = ['1080', '720', '480']
SELECTED_SHOW = None
INTELL_PARSE = False


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

    def setText(self, **kwargs):
        return self.title

    def __str__(self):
        return '{} - {}'.format(self.title, self.show_link)

    def __repr__(self):
        return '{} - {}'.format(self.title, self.show_link)


class Episode(QListWidgetItem):

    def __init__(self, title, magnet, quality):
        self.repr_string = '{} ({}p)'.format(title, quality)
        super().__init__(self.repr_string)
        self.title = title
        self.magnet = magnet
        self.quality = quality

    def __str__(self):
        return self.repr_string

    def __repr__(self):
        return self.repr_string


async def fetch_html(session, link):
    async with session.get(link) as response:
        return await response.text()


async def fetch_links(show, show_id, next_iter, quality):
    async with aiohttp.ClientSession() as session:
        api = API_URL.format(show_id, next_iter)
        html = await fetch_html(session, api)

    soup = BeautifulSoup(html, 'lxml')
    if soup.body.text == 'DONE':
        return

    links = soup.find_all(class_='rls-info-container')
    for link in links:
        quality_block = link.find('div', class_='link-{}p'.format(quality))
        _link = quality_block.find(title='Magnet Link')

        title = '{} - {}'.format(show.get('title'), link.get('id'))

        episode = Episode(title, _link.get('href'), quality)
        EPISODES.append(episode)


def get_episodes(show, quality='1080'):
    html = requests.get(ROOT_URL + show['href']).text
    soup = BeautifulSoup(html, 'lxml')
    main_div = soup.find('div', class_='entry-content')

    script_block = getattr(main_div, 'script', None)
    if not script_block:
        raise Exception('Something nasty happened, please contact the developer!')

    show_id = re.findall(r'\d+', script_block.string)[0]
    pages = 12

    if INTELL_PARSE:
        api = API_URL.format(show_id, 0)
        api_html = requests.get(api).text
        api_soup = BeautifulSoup(api_html, 'lxml')
        last_episode = int(api_soup.find('div', class_='rls-info-container').get('id'))
        pages = int(last_episode / 12) + 1

    EPISODES.clear()
    tasks = list()
    loop = asyncio.new_event_loop()
    for iteration in range(pages):
        task = loop.create_task(fetch_links(show, show_id, iteration, quality))
        tasks.append(task)

    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)

    return sorted(EPISODES)


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
        self.setFixedSize(self.size())
        self.selectQuality.addItems(QUALITIES)
        self.selectQuality.currentTextChanged.connect(self.quality_changed)

        self.animeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.animeView.doubleClicked.connect(self.display_episodes)
        self.searchField.installEventFilter(self)
        self.searchButton.clicked.connect(self.fill_table)
        self.downloadButton.clicked.connect(self.download_selected)
        self.selectAll.clicked.connect(self.select_all)
        self.deselectAll.clicked.connect(self.deselect_all)
        self.intellTurn.stateChanged.connect(self.intellTurn_changed)

    def eventFilter(self, widget, event):
        if event.type() == QEvent.KeyPress and widget is self.searchField:
            key = event.key()
            if key == Qt.Key_Return:
                self.fill_table()
        return QWidget.eventFilter(self, widget, event)

    def fill_table(self):
        global SELECTED_SHOW
        SELECTED_SHOW = None
        self.animeView.clear()
        thread = threading.Thread(target=self.fill_table_thread)
        thread.start()
        self.loadingStatus.setVisible(True)

    def fill_table_thread(self):
        if self.searchField.text() == '':
            return
        shows = matched_shows(self.searchField.text())
        for show in shows:
            self.animeView.addItem(show)
        self.loadingStatus.setVisible(False)

    def display_episodes(self):
        thread = threading.Thread(target=self.display_episodes_thread)
        thread.start()
        self.loadingStatus.setVisible(True)

    def display_episodes_thread(self):

        global SELECTED_SHOW

        start = time.time()
        if SELECTED_SHOW is None:
            selected_item = self.animeView.selectedItems()[0]
            SELECTED_SHOW = AnimeShow(selected_item.show_link,
                                      selected_item.title)  # Save the selected show to the global scope
        else:
            selected_item = SELECTED_SHOW

        selected_quality = self.selectQuality.currentText()
        episodes = get_episodes(selected_item.show_link, selected_quality)
        self.animeView.clear()
        for episode in episodes:
            self.animeView.addItem(episode)
        print(time.time() - start)
        self.loadingStatus.setVisible(False)

    def quality_changed(self):
        if SELECTED_SHOW is None:
            return

        self.animeView.clear()
        self.display_episodes()

    def download_selected(self):
        items = self.animeView.selectedItems()
        for item in items:
            open_magnet(item.magnet)

    def select_all(self):
        self.animeView.selectAll()

    def deselect_all(self):
        self.animeView.clearSelection()

    def intellTurn_changed(self):
        global INTELL_PARSE
        INTELL_PARSE = not INTELL_PARSE


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
