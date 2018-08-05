# HorribleSubs Downloader

This software allows you to quickly download multiple episodes of any anime from HorribleSubs.info

### Where I can download it?

For Windows you can go to the "Releases" tab where you can get the latest version

For Linux and Mac OS you can build it directly from source(Python 3.6+ is needed):

```bash
git clone https://github.com/TaPO4eg3D/HS_Downloader.git
cd HS_Downloader
pip install virtualenv # install virtualenv
virtualenv env # create virtual environment
source env/bin/activate # activate it
pip intall -r requirements.txt # install all dependencies
python main.py
```

### How to use it?

* Type the name of an anime and hit Enter or the "Search" button

    ![hs1](https://user-images.githubusercontent.com/12825777/43022809-aa76eed2-8c92-11e8-8429-aa75df5bd8b4.png)

* Choose the anime that you want and double click on it

    ![hs2](https://user-images.githubusercontent.com/12825777/43022810-aa9ec632-8c92-11e8-8e31-b256896b7457.png)

* Select the needed episodes and hit the "Download" button. If you want to change a quality use the checkbox above the button.

    ![hs3](https://user-images.githubusercontent.com/12825777/43022811-aac5ca2a-8c92-11e8-8920-424fb7fa9cf9.png)

### The checkbox "Is it a big anime?", what is that?

By default HS:Downloader can parse only 144 episodes. It was made for performance purposes.
If your anime show contains more than 144 episodes, select that option 

**IMPORTANT:** before using this software make sure that you have a torrent client that supports magnet links

Grab [this](https://www.qbittorrent.org/download.php) in case if you need one
