# Music Store

[![Build Status](https://travis-ci.org/stevecshanks/music-store.svg?branch=master)](https://travis-ci.org/stevecshanks/music-store)
[![Coverage Status](https://coveralls.io/repos/github/stevecshanks/music-store/badge.svg?branch=master)](https://coveralls.io/github/stevecshanks/music-store?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f4f03b6b12ca48be89538b148d4681b7)](https://www.codacy.com/app/stevecshanks/music-store?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=stevecshanks/music-store&amp;utm_campaign=Badge_Grade)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/stevecshanks/music-store/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/stevecshanks/music-store/?branch=master)

A simple music store app to play around with Flask

## Setup

### Backend

```shell
pip install -r requirements.txt
export FLASK_APP=store
flask db upgrade

# If you have a Bandcamp account:
python seed_db_from_bandcamp.py
# If you don't:
python seed_db.py

flask run
```

### Frontend

```shell
cd frontend
npm start
```
