from datetime import date, timedelta, datetime
import requests
from bs4 import BeautifulSoup
import json

class schedule_scrapping:
    """Makes the webscrapping from a URL and get data from the schedule"""
    #Se obtiene el día de hoy
    today = date.today()
    #Se obtiene el día de mañana en formato núymero de día
    tomorrow = (today + timedelta(days=1)).strftime("%d")
    #Se formatea el día de hoy a formato númerodedía
    todayFormated = today.strftime("%d")
    #Se hace un formato Mes_dd_aaaa
    formatDateOutput = today.strftime("%b_%d_%Y")
    formatDateTomorrowOutput = (today + timedelta(days=1)).strftime("%b_%d_%Y")

    def __init__(self, url, data_dir):
        self._url = url
        self._data_dir = data_dir

    def get_schedule(self):
        """Getting the schedule for tomorrow"""
        page = requests.get(self._url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            #se toma la lista de días de diciembre (tds), de la página
            listDays = soup.find_all('td', class_='day')
            #Se recorre la lista de días y se busca el que corresponda al día de mañana
            for day in listDays:
                        nday = (day.find('div', class_='date').get_text()).replace('.','')
                        #Se hace el procesamiento de los datos
                        scheduleList = self.process_Data_Schedule(day)
                        #Se valida que no sea un día de descanso
                        if scheduleList == []:
                            print(nday, ' Break Day - Not matches scheduled')
                        else: 
                            xd = ''
                            #Se crea el archivo .json 
                            if(int(nday[0:2]) < 20):
                                xd = nday[0:2] + '_dic'
                            else:
                                xd = nday[0:2] + '_nov'
                            with open(f'{self._data_dir}results_schedule_{xd}.json', 'w') as fd:
                                json_object = json.dumps(scheduleList, indent=4)
                                fd.write(json_object)
                                print('Json de la fecha ', xd, ' generado')
        except:
            pass

    def process_Data_Schedule(self, dayData):
        """Processing the data of the schedule for today
            args: 
            scheduleData: string from a html"""
        matchsList = []
        #Se extrae la información de cada partido
        matchs = dayData.find_all('div', class_='cont-marcador')
        for match in matchs:
            penal_local = match.find('div', class_='col-equipo-local')
            if(penal_local.find('span', class_='pen') is None):
                penal_local = '0'
            else:
                penal_local = penal_local.find('span', class_='pen').text[1]
            penal_visitante = match.find('div', class_='col-equipo-visitante')
            if(penal_visitante.find('span', class_='pen') is None):
                penal_visitante = '0'
            else:
                penal_visitante = penal_visitante.find('span', class_='pen').text[1]
            matchDict = { 
                'name_local': ((match.find_all('abbr', class_='nombre-equipo'))[0]['title']),
                'score_local': (((match.find_all('a', class_='marcador finalizado marcador'))[0].text).replace('\n', '')).replace(' ', '')[0],
                'score_penal_local': penal_local,
                'name_visitor': (match.find_all('abbr', class_='nombre-equipo'))[1]['title'],
                'score_visitor': (((match.find_all('a', class_='marcador finalizado marcador'))[1].text).replace('\n', '')).replace(' ', '')[0],
                'score_penal_visitor': penal_visitante }
            #Se agrega cada diccionario a la lista.
            matchsList.append(matchDict)
        return matchsList

if __name__ == '__main__':
    url = 'https://colombia.as.com/resultados/futbol/mundial/calendario/dias/'
    data_dir = 'data/corpus/'
    sc = schedule_scrapping(url, data_dir)
    sc.get_schedule()