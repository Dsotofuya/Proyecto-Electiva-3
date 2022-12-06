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
    formatDateOutput = today.strftime("%b_%d_%Y_%H_%M")

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
                        if datadict == {}:
                            print('Break Day - Not matches scheduled')
                        else: 
                        #Se crea el archivo .json 
                            with open(f'{self._data_dir}data_match_{datadict["local"]}_vs_{datadict["visitante"]}_{self.formatDateOutput}.json', 'w') as fd:
                                json_object = json.dumps(datadict, indent=4)
                                fd.write(json_object)
                                print('Json del encuentro ', datadict["local"], ' vs ', datadict["visitante"], ' generado')
            else:
               print("The word coup has ended")
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
        link_stats = 'https://resultados.as.com/' + soup.find('a', {'data-item':'stats'})['href']
        try:
            lineups = requests.get('https://resultados.as.com/' + soup.find('a', {'data-item':'lineups'})['href'])
            lineups_soup = BeautifulSoup(lineups.content, 'html.parser')
            teams_names = lineups_soup.find_all('span', class_='large')
            scorers = lineups_soup.find_all('div', class_='scorers')
            scores = lineups_soup.find_all('span', class_='team-score')
            penals = lineups_soup.find_all('sub', class_='penal')
            lineups_local = lineups_soup.find_all('ul', class_='team-lup')[1]
            lineups_visitor = lineups_soup.find_all('ul', class_='team-lup')[3]
            data_dict = {
                'local': teams_names[0].text,
                #'entrenador_local': (trainers.find_all('span', class_='in-pla-name').text)[0], 
                #alineacion_local:
                #jugadores_local:
                #posesion_local
                #disparos_recibidos
                #tarjetas_amarillas_local
                #tarjetas_rojas_local
                #faltas_recibidas
                #faltas_cometidas
                #perdidas_posesion
                #recuperaciones_posesion
                #fueras_juego
                #remates_fuera
                #remates_dentro
                #disparos_bloqueados
                'anotadores_local': (scorers[0].get_text()).replace('\n',''),
                'goles_local': (scores[0].text)[0], 
                'goles_def_penal_local': penals[0].text,
                'visitante': teams_names[1].text,
                #'entrenador_visitante': (trainers.find_all('span', class_='in-pla-name').text)[1],
                #alineacion_visitante:
                #jugadores_visitante:
                #posesion_local
                #disparos_recibidos
                #tarjetas_amarillas_local
                #tarjetas_rojas_local
                #faltas_recibidas
                #faltas_cometidas
                #perdidas_posesion
                #recuperaciones_posesion
                #fueras_juego
                #remates_fuera
                #remates_dentro
                #disparos_bloqueados
                'anotadores_visitante': scorers[1].get_text().replace('\n',''),
                'goles_visitante':(scores[1].text)[0],
                'goles_def_penal_visitante': penals[1].text,
            }
            return data_dict
        except:
            pass

if __name__ == '__main__':
    url = 'https://colombia.as.com/resultados/futbol/mundial/calendario/dias/'
    data_dir = 'data/matchs/'
    ds = data_scrapping(url, data_dir)
    ds.get_match_data()