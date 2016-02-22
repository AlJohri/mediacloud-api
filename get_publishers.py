import requests, csv, os, sys

MEDIACLOUD_KEY = os.getenv("MEDIACLOUD_KEY")

s = requests.Session()
s.params = {"key": MEDIACLOUD_KEY}
s.headers = {'Accept': 'application/json'}

COLLECTIONS_TAG_SETS_ID = 5 # Collections Tag Set
MAINSTREAM_TAG_ID = 8875027 # https://dashboard.mediameter.org/api/media/tags/single/8875027
REGIONAL_TAG_ID = 2453107 # Large list of regional TC and newspapers sites, collected by Pew in 2010.

MEDIA_TYPE_TAGS_SET = 1099 # Media Type Tag Set
GENERAL_NEWS_TAG_ID = 8878416

PKLOCATION_TAG_SETS_ID = 15 # Location Tags

media_fieldnames = ["media_id", "media_name", "media_url"]
feeds_fieldnames = ["feeds_id", "name", "url", "feed_type"] + media_fieldnames

if sys.argv[-1] == "regional":
    TAG_ID = REGIONAL_TAG_ID
    feeds_filename = "feeds_regional.csv"
    media_filename = "media_regional.csv"
elif sys.argv[-1] == "mainstream":
    TAG_ID = MAINSTREAM_TAG_ID
    feeds_filename = "feeds_mainstream.csv"
    media_filename = "media_mainstream.csv"
elif sys.argv[-1] == "all":
    TAG_ID = GENERAL_NEWS_TAG_ID
    feeds_filename = "feeds_general_news.csv"
    media_filename = "media_general_news.csv"
else:
    print("provide type of feeds/sources to download from mediacloud")
    sys.exit()

with open("data/" + feeds_filename, "w") as feeds_file, open("data/" + media_filename, "w") as media_file:

    feeds_writer = csv.DictWriter(feeds_file, feeds_fieldnames)
    feeds_writer.writeheader()

    media_writer = csv.DictWriter(media_file, media_fieldnames)
    media_writer.writeheader()

    last_media_id = 0
    while True:

        media_list = s.get("https://api.mediacloud.org/api/v2/media/list", params={
                "rows": 1000,
                "tags_id": TAG_ID,
                "last_media_id": last_media_id
        }).json()

        if len(media_list) == 0: break
        if type(media_list) is dict and media_list.get('error'):
            print(media_list.get('error'))
            break

        for media in media_list:

            media_dict = {
                "media_id": media['media_id'],
                "media_name": media['name'],
                "media_url": media['url'],
            }

            media_writer.writerow(media_dict)

            last_feeds_id = 0
            while True:

                feeds = s.get("https://api.mediacloud.org/api/v2/feeds/list", params={
                    "media_id": media['media_id'],
                    "last_feeds_id": last_feeds_id
                }).json()

                if len(feeds) == 0: break
                if type(feeds) is dict and feeds.get('error'):
                    print(feeds.get('error'))
                    break

                for feed in feeds:

                    feed_dict = {
                        "feeds_id": feed['feeds_id'],
                        "name": feed['name'],
                        "url": feed['url'],
                        "feed_type": feed['feed_type']
                    }

                    feed_dict.update(media_dict)
                    print(feed_dict)

                    feeds_writer.writerow(feed_dict)

                last_feeds_id = feeds[-1]['feeds_id']

        last_media_id = media_list[-1]['media_id']