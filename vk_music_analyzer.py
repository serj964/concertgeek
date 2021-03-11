import re
import math
import vk_api
from vk_api import vk_api
from vk_api.audio import VkAudio

MEDIANA = 0.45
WEIGHT = 0.125
USER_ID = 148057277
cl = 'rqozJXDcBPrygXS181xr'
url = 'http://localhost:8000/auth_complete'
token = 


#логинится
def log(): 
    vk_session = vk_api.VkApi(client_secret = cl,
                              app_id = 7562746
                             )
    #vk = vk_session.get_api()
    try:
        vk_session.code_auth(token, url)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    
    return VkAudio(vk_session)


#возвращает список альбомов и плейлистов пользователя
def get_albums():
    vkaudio = log()
    return vkaudio.get_albums()  #USER_ID


#проверяет исполнителей на наличие feat.
def feat_check(lst):
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
def get_list_songs():
    vkaudio = log()
    lst = []
    
    for track in vkaudio.get_iter(owner_id = None):
        lst.append(track['artist'].lower())
        
    final_lst = feat_check(lst)    
    
    return final_lst


#возвращает список добавленных в плейлисты песен (по названию артистов) из аудио вк
def get_list_playlists():
    vkaudio = log()
    lst = []
    
    albums = get_albums()
    
    for i in range(len(albums)):
        tracks = vkaudio.get_iter(owner_id = albums[i]['owner_id'],
                                  album_id = albums[i]['id'],
                                  access_hash = albums[i]['access_hash'])
        
        for track in tracks:
            lst.append(track['artist'].lower())
            
    final_lst = feat_check(lst)
        
    return final_lst


#шаг
def step(m):
    return math.log(m)/25


#распределение очков между добавленными песнями
def points_songs():
    dic = {}
    k = ''
    n = get_list_songs()
    m = len(n)
    p = step(m)
    s = MEDIANA + p
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
def points_playlists():
    try:
        dic = {}
        n = get_list_playlists()
        m = len(n)
        p = step(m)
        s = WEIGHT
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
def main():
    dic1 = points_songs()
    dic2 = points_playlists()
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

    for i in range(math.ceil((len(list_d) ** 0.6))):
        lst.append(list_d[i][0])
        
    return lst


    
if __name__ == '__main__':
    main()
