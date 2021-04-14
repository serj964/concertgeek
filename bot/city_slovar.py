import math

class city_slovar:
    def __init__(self):
        self.SLOVAR = {'moscow': '55.755814, 37.617635',
                       'Санкт-Петербург': '59.939095, 30.315868',
                       'Сочи': '43.585472, 39.723089'
                       #'Краснодар': '45.035470, 38.975313',
                       #'Казань': '55.796127, 49.106405',
                       #'Новосибирск': '55.030199, 82.920430',
                       #'Екатеринбург': '56.838011, 60.597465',
                       #'Нижний Новгород': '56.331927, 44.023225',
                       #'Челябинск': '55.159897, 61.402554',
                       #'Владивосток': '43.115536, 131.885485',
                       #'Белгород': '50.595414, 36.587268',
                       #'Владимир': '56.129057, 40.406635',
                       #'Ижевск': '56.852676, 53.206891',
                       #'Красноярск': '56.010563, 92.852572',
                       #'Мурманск': '68.970663, 33.074909',
                       #'Смоленск': '54.782630, 32.045287',
                       #'Омск': '54.989342, 73.368212',
                       #'Хабаровск': '48.480223, 135.071917',
                       #'Самара': '53.195873, 50.100193',
                       #'Ростов-на-Дону': '47.222078, 39.720349',
                       #'Уфа': '54.735147, 55.958727',
                       #'Воронеж': '51.660781, 39.200269',
                       #'Пермь': '58.010450, 56.229434',
                       #'Волгоград': '48.707067, 44.516975',
                       #'Тула': '54.193122, 37.617348',
                       #'Рязань': '54.629560, 39.741908',
                       #'Калуга': '54.513845, 36.261215',
                       #'Тверь': '56.859625, 35.911851'
                }

    def __rad(self, x):
        return math.radians(x)
    
    
    def __measure(self, user_lat, user_long, city_lat, city_long):
        a = math.cos(self.__rad(city_lat))*math.cos(self.__rad(user_lat))*math.cos(self.__rad(user_long)-self.__rad(city_long))
        b = math.sin(self.__rad(city_lat))*math.sin(self.__rad(user_lat))
        return 6367*math.acos(a + b)
    
    
    #транслитерация для spotify
    def nearest_city(self, user_lat, user_long):
        dicti = {}
        for city in self.SLOVAR.keys():
            s = self.SLOVAR[city]
            lat = float(s[0:s.find(',', 0,len(s))])
            long = float(s[s.find(',', 0,len(s))+2:len(s)])
            dist = self.__measure(user_lat, user_long, lat, long)
            dicti[city] = dist
            
        dist = 40000
        nearest = ''
        for city in dicti.keys():
            if dicti[city] < dist:
                nearest = city
                dist = dicti[city]
                
        return nearest