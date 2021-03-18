import requests
import datetime


class Concerts:
    def __init__(self):
        self.concerts = []

    def load_concerts(self, city='moscow', day=datetime.date.today(), number_of_days=120):
        self.concerts = []
        limit = 20
        offset = 0
        link = f"https://afisha.yandex.ru/api/events/rubric/concert?limit={limit}&offset={offset}&hasMixed=0&date={day.strftime('%Y-%m-%d')}&period={number_of_days}&city={city}&_=1615390892410"
        responce = requests.get(link)
        total = responce.json()['paging']['total']
        data = responce.json()['data']
        while offset <= total:
            for concert in data:
                d = {}
                try:
                    d['title'] = concert['event']['title']
                except Exception:
                    pass
                try:
                    d['url'] = 'https://afisha.yandex.ru' + concert['event']['url']
                except Exception:
                    pass
                try:
                    d['price'] = concert['event']['tickets'][0]['price']['min'] // 100
                except Exception:
                    pass
                try:
                    d['date'] = concert['scheduleInfo']['preview']['text']
                except Exception:
                    pass
                try:
                    d['place'] = concert['scheduleInfo']['oneOfPlaces']['title'] + ', ' + concert['scheduleInfo']['oneOfPlaces']['address']
                except Exception:
                    pass
                self.concerts.append(d)
            offset += limit
            link = f"https://afisha.yandex.ru/api/events/rubric/concert?limit={limit}&offset={offset}&hasMixed=0&date={day.strftime('%Y-%m-%d')}&period={number_of_days}&city={city}&_=1615390892410"
            responce = requests.get(link)
            data = responce.json()['data']

    def find_concerts(self, artist):
        suitable_concerts = []
        for concert in self.concerts:
            if concert['title'].lower() == artist.lower():
                suitable_concerts.append(concert)
        return suitable_concerts
