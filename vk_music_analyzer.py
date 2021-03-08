import time
import math
from vk_api.audio import VkAudio

MEDIANA = 0.45
WEIGHT = 0.15
USER_ID = #id юзера, которого чекаете
LOGIN = #введите свой
PASSWORD = #введите свой


#логинится
def log(): 
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    
    return VkAudio(vk_session)


#возвращает список альбомов и плейлистов пользователя
def get_albums():
    return vkaudio.get_albums(USER_ID)


#возвращает список добавленных в аудиозаписи песен (по названию артистов) из аудио вк
def get_list_songs():
    vkaudio = log()
    lst = []
    
    for track in vkaudio.get_iter(owner_id = USER_ID):
        lst.append(track['artist'].lower())
        
    return lst


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
        
    return lst


#шаг
def step(m):
    return math.log(m)/25


#распределение очков между добавленными песнями
def points_songs():
    dic = {}
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
            
            s = s - p / (4 * m)
            
        return dic
    
    except ValueError:
        pass
    
    
#возвращает "любимых" исполнителей
def score():
    dic1 = points_songs()
    dic2 = points_playlists()
    result = {}
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

    for i in range(math.ceil((len(list_d)) ** 0.5)):
        print(list_d[i])
    #print(result)
        

def main():
    return score()


if __name__ == '__main__':
    main()
