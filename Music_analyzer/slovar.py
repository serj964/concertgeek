class slovar:
    def __init__(self):
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
                       'kino': 'кино',
                       'grazhdanskaya oborona': 'гражданская оборона',
                       'poshlaja molli': 'пошлая молли'}

        
    #транслитерация для spotify
    def transliterate(self, lst):
        for key in self.SLOVAR:
            for i in range(len(lst)):
                if lst[i] == key:
                    lst[i] = self.SLOVAR[key]
                    
        return lst
