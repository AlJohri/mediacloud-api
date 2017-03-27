import requests, csv, os, sys

MEDIACLOUD_KEY = os.environ['MEDIACLOUD_KEY']

with open("data/collections.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=['tags_id', 'tag', 'label', 'description', 'is_static', 'show_on_stories', 'show_on_media', 'tag_sets_id', 'tag_set_name', 'tag_set_label', 'tag_set_description'])
    writer.writeheader()
    last_tags_id = 0
    while True:
        rows = requests.get(f"https://api.mediacloud.org/api/v2/tags/list?public=1&rows=100&last_tags_id={last_tags_id}&key={MEDIACLOUD_KEY}").json()

        if len(rows) == 0: break
        if type(rows) is dict and rows.get('error'):
            print(rows.get('error'))
            break

        for row in rows:
            print(row['tags_id'], row['tag'], row['label'])
            writer.writerow(row)

        last_tags_id = rows[-1]['tags_id']