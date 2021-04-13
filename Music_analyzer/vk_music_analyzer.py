import re
import math
import vk_api
from vk_api.audio import VkAudio
from Music_analyzer.password import password


class vk_music_analyzer:
    def __init__(self):
        self.MEDIANA = 0.45
        self.WEIGHT = 0.125


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


    #возвращает список добавленных в аудиозаписи песен (по названию артистов) из аудио вк
    def __get_list_songs(self, session, user_id):
        lst = []
        
        for track in session.get(owner_id = user_id):
            lst.append(track['artist'].lower())
            
        final_lst = self.__feat_check(lst)    
        
        return final_lst


    #возвращает список добавленных в плейлисты песен (по названию артистов) из аудио вк
    def __get_list_playlists(self, session, user_id):
        lst = []
        
        albums = session.get_albums(owner_id = user_id)
        
        for i in range(len(albums)):
            tracks = session.get_iter(owner_id = albums[i]['owner_id'],
                                      album_id = albums[i]['id'],
                                      access_hash = albums[i]['access_hash'])
            
            for track in tracks:
                lst.append(track['artist'].lower())
                
        final_lst = self.__feat_check(lst)
            
        return final_lst


    #шаг
    def __step(self, m):
        return math.log(m) / 25


    #распределение очков между добавленными песнями
    def __points_songs(self, session, user_id):
        dic = {}
        k = ''
        n = self.__get_list_songs(session, user_id)
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
    def __points_playlists(self, session, user_id):
        try:
            dic = {}
            n = self.__get_list_playlists(session, user_id)
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
        
        
    #возвращает наиболее "любимых" исполнителей
    def get_favourite_artists(self, user_id):
        LOGIN = '+79060733528'
        user_id = int(user_id)

        vk_session = vk_api.VkApi(LOGIN, password)
        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            
        session = VkAudio(vk_session)
        
        dic1 = self.__points_songs(session, user_id)
        dic2 = self.__points_playlists(session, user_id)
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

        for i in range(math.ceil((len(list_d) ** 0.8))):
            lst.append(list_d[i][0])
            
        return lst
