from datetime import date, timedelta, datetime
import requests
from bs4 import BeautifulSoup
import json

class data_scrapping:
    """Makes the webscrapping from a URL and get data from the schedule"""
    #Se obtiene el día de hoy
    today = datetime.now()
    #Se formatea el día de hoy a formato númerodedía
    todayFormated = today.strftime("%d")
    #Se hace un formato Mes_dd_aaaa_hh:mm
    formatDateOutput = today.strftime("%b_%d_%Y_%H:%M")

    def __init__(self, url, data_dir):
        self._url = url
        self._data_dir = data_dir

    def get_match_data(self):
        """Getting the schedule for tomorrow"""
        page = requests.get(self._url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            #se toma la lista de días de diciembre (tds), de la página
            listDays = soup.find_all('td', class_='day')
            #Se recorre la lista de días y se busca el que corresponda al día de mañana
            if(self.todayFormated <= '18'):
                for day in listDays:
                    if(day.find('div', class_='date').get_text()[:2] == self.todayFormated):
                        #Se hace el procesamiento de los datos
                        datadict = self.get_Data(day, '10:00')
                        #Se valida que no sea un día de descanso
                        #if datadict == {}:
                        #    print('Break Day - Not matches scheduled')
                        #else: 
                            #Se crea el archivo .json 
                        #    with open(f'{self._data_dir}data_match_{datadict["local"]}_{datadict["visitante"]}_{self.formatDateOutput}.json', 'w') as fd:
                        #        json_object = json.dumps(scheduleList, indent=4)
                        #        fd.write(json_object)
                        #        print('Json del encuentro ', {datadict["local"]}, ' vs ', {datadict["visitante"]}, ' generado')
           # else:
            #    print("The word coup has ended")
        except:
            pass


    def get_Data(self, dayData, hour):
        """Processing the data of a match
        args: 
            scheduleData: string from a html
            hour: string from a match hour"""
        #Se extrae la información de cada partido
        matchs = dayData.find_all('div', class_='cont-resultados grupo-')
        for match in matchs:
            if((match.find('time').get_text()).replace(' COT ','') == hour):
                newURL = match.find_all('a', class_='marcador finalizado marcador')[0]
                return self.scrap_statistics(newURL['href'])

    def scrap_statistics(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        link_lineups = 'https://resultados.as.com/' + soup.find('a', {'data-item':'lineups'})['href']
        link_stats = 'https://resultados.as.com/' + soup.find('a', {'data-item':'stats'})['href']
        try:
            print(link_lineups)
            print(link_stats)
        except:
            pass
#matchDict = { 'name': (match.find('p', class_='grupo')['title']).replace('-', 'vs'), 'hour':  }
if __name__ == '__main__':
    url = 'https://colombia.as.com/resultados/futbol/mundial/calendario/dias/'
    data_dir = 'data/matchs/'
    ds = data_scrapping(url, data_dir)
    ds.get_match_data()