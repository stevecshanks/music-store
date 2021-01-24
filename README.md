# Music Store

[![Build Status](https://travis-ci.org/stevecshanks/music-store.svg?branch=main)](https://travis-ci.org/stevecshanks/music-store)
[![Coverage Status](https://coveralls.io/repos/github/stevecshanks/music-store/badge.svg?branch=main)](https://coveralls.io/github/stevecshanks/music-store?branch=main)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f4f03b6b12ca48be89538b148d4681b7)](https://www.codacy.com/app/stevecshanks/music-store?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=stevecshanks/music-store&amp;utm_campaign=Badge_Grade)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/stevecshanks/music-store/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/stevecshanks/music-store/?branch=main)

A simple music store app to play around with Flask

## Setup

```shell
docker-compose up -d

docker-compose exec app bash

flask db upgrade

# If you have a Bandcamp account:
python seed_db_from_bandcamp.py
# If you don't:
python seed_db.py
```

Browse to http://localhost:3000/ to access the app.
