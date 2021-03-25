import re
import math
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class spotify_music_analyzer:
    def __init__(self):
        self.MEDIANA = 0.4
        self.WEIGHT = 0.125
        self.SLOVAR = {'pasosh':'пасош',
                       'buerak':'буерак', 
                       'dzhizus': 'джизус', 
                       'mukka': 'мукка', 
                       'valentin strykalo': 'валентин стрыкало', 
                       'zavtra broshu': 'завтра брошу',
                       'pasha technique': 'паша техник',
                       'leto v gorode': 'лето в городе',
                       'nurminsky': 'нурминский',
                       'svidaniye': 'свидание',
                       'kasta': 'каста',
                       'electroforez': 'электрофорез',
                       'agatha christie': 'агата кристи',
                       'kino': 'кино'}0



    #проверяет исполнителей на наличие feat.
    def __feat_check(self, lst):
        i = 0
        for artist in lst:
            try:
                s = re.search(r' feat. | ft. ', artist)
                p1, p2 = artist[0:s.start()], artist[s.end():]
                lst.pop(i)
                lst.insert(i, p1)
                lst.append(p2)
            except AttributeError:
                pass
    
            i += 1
        
        return lst



    #возвращает список песен, добавленных в "любимые треки" (по названию артистов)
    def __get_list_songs(self, sp):
        lst = []
        i = 0
        while (i <= (len(lst) // 50)):
            results = sp.current_user_saved_tracks(offset = 50*i, limit = 50)
            for idx, item in enumerate(results['items']):
                track = item['track']
                lst.append(track['artists'][0]['name'].lower())
            i += 1
        
        final_lst = self.__feat_check(lst)
    
        return final_lst


    #возвращает список добавленных в плейлисты песен (по названию артистов)
    def __get_list_playlists(self, sp):
        lst = []
        i = 0
        while (i <= (len(lst) // 50)):
            play = sp.current_user_playlists(offset = 50*i, limit = 50)
            for i in range(len(play['items'])):
                item = play['items'][i]
                playlist = sp.user_playlist(item['owner']['id'], item['id'])

                for i in range(0, len(playlist["tracks"]["items"])):
                    if playlist["tracks"]["items"][i]['track']['id'] != None:
                        lst.append(playlist["tracks"]["items"][i]['track']['album']['artists'][0]['name'].lower())         
            i += 1

        final_lst = self.__feat_check(lst)
    
        return final_lst


    #шаг
    def __step(self, m): 
        return math.log(m) / 25


    #распределение очков между песнями из "любимых треков"
    def __points_songs(self, sp):
        dic = {}
        k = ''
        n = self.__get_list_songs(sp)
        m = len(n)
        p = self.__step(m)
        s = self.MEDIANA + p
        for artist in n:
        
            if (artist in dic):
                dic[artist].append(s)
            else:
                dic[artist] = [s]
            
            s = s - (2 * p) / m
        
            if artist == k:
                dic[artist].append(0.005)
            else:
                k = artist
            
        return dic
    
    
    #распределение очков между песнями из плейлистов    
    def __points_playlists(self, sp):
        try:
            dic = {}
            n = self.__get_list_playlists(sp)
            m = len(n)
            p = self.__step(m)
            s = self.WEIGHT
            for artist in n:
        
                if (artist in dic):
                    dic[artist].append(s)
                else:
                    dic[artist] = [s]
            
                s = s - p / (5 * m)
            
            return dic
    
        except ValueError:
            pass
    
    
    #транслитерация для spotify
    def __transliterate(self, lst):
        for key in self.SLOVAR:
            for i in range(len(lst)):
                if lst[i] == key:
                    lst[i] = self.SLOVAR[key]
                    
        return lst
        
    
    #возвращает наиболее "любимых" исполнителей
    def get_favourite_artists(self, sp):
        dic1 = self.__points_songs(sp)
        dic2 = self.__points_playlists(sp)
        result = {}
        lst = []
        try:
            for key in (dic1.keys() | dic2.keys()):
                if key in dic1: result.setdefault(key, []).extend(dic1[key])
                if key in dic2: result.setdefault(key, []).extend(dic2[key])
                
        except AttributeError:
            result = dic1
    
    
        for artist in result.keys():
            result[artist] = sum((result[artist]))
    
        list_d = list(result.items())

        list_d.sort(key = lambda i: i[1], reverse=True)

        for i in range(math.ceil((len(list_d) ** 0.85))):
            lst.append(list_d[i][0])
        
        return self.__transliterate(lst)