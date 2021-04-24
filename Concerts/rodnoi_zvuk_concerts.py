import requests
import datetime
import re
from bs4 import BeautifulSoup


class Concerts:
    def __init__(self):
        self.concerts = []



    def __get_link_to_last_news(self):
        link_news = "https://rodzvuk.ru/category/news"
        responce = requests.get(link_news)
        soup = BeautifulSoup(responce.text, 'html.parser')
        for link in soup.find_all('a'):
            try:
                if re.search('weekgigs', link.get('href')):
                    return link.get('href')
            except Exception:
                pass

    def load_concerts(self):
        self.concerts = []
        link = f"https://rodzvuk.ru{self.__get_link_to_last_news()}"
        responce = requests.get(link)
        soup = BeautifulSoup(responce.text, 'html.parser')
        p = []
        for i in soup.find_all('p'):
            p.append(i)
        i = 1
        while i < len(p):
            if p[i].string == "МОСКВА":
                current_city = "Москва"
                i += 1
            elif p[i].string == "САНКТ-ПЕТЕРБУРГ" or \
                p[i].string == "ПИТЕР":
                current_city = "Санкт-Петербург"
                i += 1

            elif re.match("Понедельник", p[i].string) or \
                re.match("Вторник", p[i].string) or \
                re.match("Среда", p[i].string) or \
                re.match("Четверг", p[i].string) or \
                re.match("Пятница", p[i].string) or \
                re.match("Суббота", p[i].string) or \
                re.match("Воскресенье", p[i].string):
                current_date = p[i].string
                i += 1

            else:
                d = {}
                d["city"] = current_city
                d["date"] = current_date
                d["title"] = p[i].string
                i += 2
                if p[i].string is not None:
                    d["comment"] = p[i].string
                    i += 1
                print(p[i])
                d["url"] = p[i].a.get('href')
                i += 1
                self.concerts.append(d)




    def find_concerts(self, artist):
        suitable_concerts = []
        for concert in self.concerts:
            if artist.lower() == concert['title'].lower():
             suitable_concerts.append(concert)
        return suitable_concerts
            
    def get_concerts(self):
        return self.concerts 
