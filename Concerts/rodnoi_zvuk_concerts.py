import requests
import datetime
import re


class Concerts:
    def __init__(self):
        self.concerts = []

    def load_concerts(self, categories=4, per_page=100):
        self.concerts = []
        link = f"https://api.rodzvuk.ru/?rest_route=/wp/v2/posts&{categories}=4&{per_page}=100"
        responce = requests.get(link)
        for concert in responce.json():
            d = {}
            try:
                d['title'] = concert['title']['rendered']
            except Exception:
                pass               
            self.concerts.append(d)

    def find_concerts(self, artist):
        suitable_concerts = []
        for concert in self.concerts:
            if re.search(artist.lower(), concert['title'].lower()):
             suitable_concerts.append(concert)
        return suitable_concerts
