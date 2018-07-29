import re
import store
from bs4 import BeautifulSoup
from store.models import Album, db
from urllib.request import urlopen

app = store.create_app()
app.app_context().push()


def main():
    username = input('What is your Bandcamp username? ')

    collection_url = 'https://bandcamp.com/' + username
    collection = urlopen(collection_url)
    soup = BeautifulSoup(collection, features='html.parser')

    all_albums = get_albums(soup)
    for i, album in enumerate(all_albums):
        create_album(album)
        print('Added album {}/{}'.format(i + 1, len(all_albums)))


def get_albums(soup):
    return soup.find_all('li', attrs={'class': 'collection-item-container'})


def create_album(album):
    db_album = Album(artist=get_artist(album), name=get_name(album), bandcamp_url=get_bandcamp_url(album),
                     cover_image_url=get_cover_image_url(album))
    db.session.add(db_album)
    db.session.commit()


def get_artist(album):
    artist_text = album.find('div', attrs={'class': 'collection-item-artist'}).text
    return re.search('by (.*)', artist_text).group(1)


def get_name(album):
    title_div = album.find('div', attrs={'class': 'collection-item-title'})
    return next(title_div.stripped_strings)


def get_bandcamp_url(album):
    return album.find('div', attrs={'class': 'collection-title-details'}).a.get('href')


def get_cover_image_url(album):
    return album.find('img', attrs={'class': 'collection-item-art'}).get('src')


main()
