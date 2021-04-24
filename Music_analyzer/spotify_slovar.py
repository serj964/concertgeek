class Slovar:
    def __init__(self):
        self.SLOVAR = {'pasosh':'пасош',
                       'buerak':'буерак', 
                       'dzhizus': 'джизус', 
                       'mukka': 'мукка', 
                       'valentin strykalo': 'валентин стрыкало', 
                       'zavtra broshu': 'завтра брошу',
                       'korol i shut': 'король и шут',
                       'pasha technique': 'паша техник',
                       'leto v gorode': 'лето в городе',
                       'lyapis trubetskoy': 'ляпис трубецкой',
                       'nurminsky': 'нурминский',
                       'svidaniye': 'свидание',
                       'kasta': 'каста',
                       'electroforez': 'электрофорез',
                       'agatha christie': 'агата кристи',
                       'kino': 'кино',
                       'splean': 'сплин',
                       'chaif': 'чайф',
                       'grazhdanskaya oborona': 'гражданская оборона',
                       'poshlaja molli': 'пошлая молли',
                       'max korzh': 'макс корж',
                       'maybe baby': 'мэйби бэйби',
                       'poshlaya molly': 'пошлая молли',
                       'tantsy minus': 'танцы минус',
                       'pornofilmy': 'порнофильмы',
                       'neuromonakh feofan': 'нейромонах феофан',
                       'piknik': 'пикник',
                       'alyans': 'альянс',
                       'grechka': 'гречка',
                       'operation plasticine': 'операция пластилин',
                       'zemfira': 'земфира',
                       'aquarium': 'аквариум',
                       'nike borzov': 'найк борзов',
                       'bi-2': 'би-2',
                       'pika': 'пика',
                       'malbec': 'мальбэк',
                       'eldzhey': 'элджей',
                       'sektor gaza': 'сектор газа',
                       'chicherina': 'чичерина',
                       'krematorij': 'крематорий',
                       'zhuki': 'жуки',
                       'mumiy troll': 'мумий тролль'}

        
    #транслитерация для spotify
    def transliterate(self, lst):
        for key in self.SLOVAR:
            for i in range(len(lst)):
                if lst[i] == key:
                    lst[i] = self.SLOVAR[key]
                    
        return lst
