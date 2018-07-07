import store
from store.models import Album, db


app = store.create_app()
app.app_context().push()

albums = [
    Album(artist='Deus Vermin', name='Monument To Decay',
          cover_image_url='https://f4.bcbits.com/img/a1486857090_16.jpg',
          bandcamp_url='https://deusvermin.bandcamp.com/album/monument-to-decay'),
    Album(artist='hvíldarlauss dauðr', name='Terrorforming',
          cover_image_url='https://f4.bcbits.com/img/a0234421477_16.jpg',
          bandcamp_url='https://hvildarlaussdaudr.bandcamp.com/album/terrorforming'),
    Album(artist='Vacivus', name='Rite of Ascension',
          cover_image_url='https://f4.bcbits.com/img/a1747549551_16.jpg',
          bandcamp_url='https://vacivus.bandcamp.com/album/rite-of-ascension'),
    Album(artist='Bròn', name='Ànrach', cover_image_url='https://f4.bcbits.com/img/a2353430697_16.jpg',
          bandcamp_url='https://bronmusic.bandcamp.com/album/nrach'),
    Album(artist='Plague Rider', name='Paroxysm', cover_image_url='https://f4.bcbits.com/img/a1359105345_16.jpg',
          bandcamp_url='https://plaguerider.bandcamp.com/album/paroxysm'),
]

for album in albums:
    db.session.add(album)
db.session.commit()