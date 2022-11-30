from datetime import date, timedelta, datetime
import requests
from bs4 import BeautifulSoup
import json

class schedule_scrapping:
    """Makes the webscrapping from a URL and get data from the schedule"""
    #Se obtiene el día de hoy
    today = date.today()
    #Se obtiene el día de mañana en formato Día Mes númerodedía
    tomorrow = (today + timedelta(days=1)).strftime("%A %B %d")
    #Se formatea el día de hoy a formato Día Mes númerodedía
    todayFormated = today.strftime("%A %B %d")
    #Se hace un formato Mes_dd_aaaa
    formatDateOutput = today.strftime("%b_%d_%Y")

    def __init__(self, url, data_dir):
        self._url = url
        self._data_dir = data_dir

    def get_schedule(self):
        """Getting the schedule for today"""
        page = requests.get(self._url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            #se busca el div principal
            div = soup.find_all('div', class_='sdc-article-body sdc-article-body--lead')
                                                              #text=True , recursive=True 
            #Se filtran los tags que sean p
            paragraphs = soup.find_all('p')
            #Se busca el tag p que corresponda al día de hoy
            paragraphToday = soup.find('p', text=self.todayFormated)
            #Se saca el index del tag del día de hoy
            indexData = paragraphs.index(paragraphToday)
            #Se toma el texto en el index del texto + una posición para obtener los datos del calendario
            scheduleData = paragraphs[indexData+1].getText()
            #Se hace el procesamiento de los datos
            scheduleList = self.process_Data_Schedule(scheduleData)
            #Se crea el archivo .json 
            with open(f'{self._data_dir}data_{self.formatDateOutput}.json', 'w') as fd:
                json_object = json.dumps(scheduleList)
                print(json_object)
                fd.write(json_object)
                print('Json de la fecha ', self.formatDateOutput, ' generado')
        except:
            pass

    def process_Data_Schedule(self, scheduleData):
        """Processing the data of the schedule for today
            args: 
            scheduleData: string from a html"""
        #Se hace tratamiento de datos, se separa cada encuentro por )
        primeValues = scheduleData.split(")")
        #Se elimina el último objeto de la lista ya que es vacio
        primeValues.pop()
        scheduleList = []
        for element in primeValues:
            #Se filtran las horas por una busqueda de derecha a izquierda 
            hour = element[element.rfind(' '):]
            #Se filtran los nombres por una letra en especifico que aparece en los datos
            value = element[:element.rfind('k')]
            matchDict = {
                #Se reemplaza los caracteres no utiles y se reemplaza por un )
                'name': value.replace('; kic',')'),
                #formateo de la hora
                'hour': self.format_hour(hour.replace(' ','',1))
            }
            #Se agrega cada diccionario a la lista.
            scheduleList.append(matchDict)
        return scheduleList

    def format_hour(self, hour):
        """Format hour from hpm/am to military
            args: str with format hpm/am ej: 3pm"""
        #Se pasa el string a mayusculas para que sea acorde al formato
        in_time = datetime.strptime(hour.upper(), "%I%p")
        #se hace el cambio de formato y se recalcula la hora conforme a la zona horaria de colombia
        out_time = datetime.strftime((in_time - timedelta(hours=5)), "%H:%M")
        return out_time

if __name__ == '__main__':
    url = 'https://www.skysports.com/football/news/12098/12354033/world-cup-2022-dates-draw-schedule-kick-off-times-final-for-qatar-tournament'
    data_dir = 'data/'
    sc = schedule_scrapping(url, data_dir)
    sc.get_schedule()
    #sc.format_hour('7pm')