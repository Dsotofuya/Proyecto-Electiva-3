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
            if(self.tomorrow <= '18'):
                for day in listDays:
                    if(day.find('div', class_='date').get_text()[:2] == self.tomorrow):
                        #Se hace el procesamiento de los datos
                        scheduleList = self.process_Data_Schedule(day)
                        if scheduleList == []:
                            print('Break Day - Not matches scheduled')
                        else: 
                            #Se crea el archivo .json 
                            with open(f'{self._data_dir}data_schedule_{self.formatDateTomorrowOutput}.json', 'w') as fd:
                                json_object = json.dumps(scheduleList, indent=4)
                                fd.write(json_object)
                                print('Json de la fecha ', self.formatDateTomorrowOutput, ' generado')
            else:
                print("The word coup has ended")
        except:
            pass

    def process_Data_Schedule(self, dayData):
        """Processing the data of the schedule for today
            args: 
            scheduleData: string from a html"""
        matchsList = []
        #Se extrae la información de cada partido
        matchs = dayData.find_all('div', class_='cont-resultados grupo-')
        for match in matchs:
            matchDict = { 
                'name': (match.find('p', class_='grupo')['title']).replace('-', 'vs'),
                'hour': (match.find('time').get_text()).replace(' COT ','') }
            #Se agrega cada diccionario a la lista.
            matchsList.append(matchDict)
        return matchsList

if __name__ == '__main__':
    url = 'https://colombia.as.com/resultados/futbol/mundial/calendario/dias/'
    data_dir = 'data/schedule/'
    sc = schedule_scrapping(url, data_dir)
    sc.get_schedule()