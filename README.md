# Mediacloud API

Use Mediacloud API to get feeds and publishers (media sources).

## Usage

`source .secret` before running code

- `python get_publishers.py regional` - get regional feeds/sources
- `python get_publishers.py mainstream` - get mainstream feeds/sources
- `python get_publishers.py all` - get all feeds/sources

## Setup

Use Python 3.5+

- `pip install -r requirements.txt`
- `cp .secret.example .secret`
- `vim .secret` edit file to include api key
