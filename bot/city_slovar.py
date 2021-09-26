from math import cos, radians, acos, sin

class City_slovar:
    def __init__(self):
        self.SLOVAR = {'Москва': ['moscow', 55.755814, 37.617635],
                       'Санкт-Петербург': ['saint-petersburg', 59.939095, 30.315868],
                       'Сочи': ['sochi', 43.585472, 39.723089],
                       'Алма-Ата': ['almaty', 43.237163, 76.945627],
                       'Алматы': ['almaty', 43.237163, 76.945627],
                       'Архангельск': ['arhangelsk', 64.539911, 40.515762],
                       'Астрахань': ['astrahan', 46.347614, 48.030178],
                       'Белгород': ['belgorod', 50.595414, 36.587268],
                       'Брянск': ['bryansk', 53.243556, 34.363425],
                       'Владивосток': ['vladivostok', 43.115536, 131.885485],
                       'Владимир': ['vladimir', 56.129057, 40.406635],
                       'Волгоград': ['volgograd', 48.707067, 44.516975],
                       'Воронеж': ['voronezh', 51.660781, 39.200269],
                       'Екатеринбург': ['yekaterinburg', 56.838011, 60.597465],
                       'Ижевск': ['izhevsk', 56.852676, 53.206891],
                       'Иркутск': ['irkutsk', 52.289588, 104.280606],
                       'Казань': ['kazan', 55.796127, 49.106405],
                       'Калининград': ['kaliningrad', 54.710162, 20.510137],
                       'Калуга': ['kaluga', 54.513845, 36.261215],
                       'Краснодар': ['krasnodar', 45.035470, 38.975313],
                       'Красноярск': ['krasnoyarsk', 56.010563, 92.852572],
                       'Курск': ['kursk', 51.730846, 36.193015],
                       'Липецк': ['lipetsk', 52.608826, 39.599229],
                       'Мурманск': ['murmansk', 68.970663, 33.074909],
                       'Нижний Новгород': ['nizhny-novgorod', 56.331927, 44.023225],
                       'Новосибирск': ['novosibirsk', 55.030199, 82.920430],
                       'Омск': ['omsk', 54.989342, 73.368212],
                       'Орел': ['orel', 52.970756, 36.064358],
                       'Пермь': ['perm', 58.010450, 56.229434],
                       'Псков': ['pskov', 57.819274, 28.332460],
                       'Ростов-на-Дону': ['rostov-na-donu', 47.222078, 39.720349],
                       'Рязань': ['ryazan', 54.629560, 39.741908],
                       'Самара': ['samara', 53.195873, 50.100193],
                       'Саратов': ['saratov', 51.533562, 46.034266],
                       'Серпухов': ['serpuhov', 54.913681, 37.416601],
                       'Смоленск': ['smolensk', 54.782630, 32.045287],
                       'Тверь': ['tver', 56.859625, 35.911851],
                       'Томск': ['tomsk', 56.484645, 84.947649],
                       'Тула': ['tula', 54.193122, 37.617348],
                       'Тюмень': ['tyumen', 57.152985, 65.541227],
                       'Уфа': ['ufa', 54.735147, 55.958727],
                       'Хабаровск': ['khabarovsk', 48.480223, 135.071917],
                       'Челябинск': ['chelyabinsk', 55.159897, 61.402554]
                }

    
    def __measure(self, user_lat, user_long, city_lat, city_long):
        a = cos(radians(city_lat))*cos(radians(user_lat))*cos(radians(user_long)-radians(city_long))
        b = sin(radians(city_lat))*sin(radians(user_lat))
        return 6367*acos(a + b)
    
    
    #возвращает по координатам
    def nearest_city_by_location(self, user_lat, user_long):
        dicti = {}
        city_dicti = {}
        for city in self.SLOVAR.keys():
            s = self.SLOVAR[city]
            lat = float(s[1])
            long = float(s[2])
            dist = self.__measure(user_lat, user_long, lat, long)
            dicti[city] = dist
            
        dist = 40000
        nearest = ''
        for city in dicti.keys():
            if dicti[city] < dist:
                nearest = city
                dist = dicti[city]
        
        s = self.SLOVAR[nearest]
        city_dicti[nearest] = s[0]
                
        return city_dicti
    
    
    #возвращает по имени
    def city_by_name(self, name):
        city_name = ''
        for city in self.SLOVAR.keys():
            if name.lower() == city.lower():
                s = self.SLOVAR[city]
                city_name = s[0]
            
        if city_name != '':
            return city_name
        else:
            raise ValueError