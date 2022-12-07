from datetime import date, timedelta, datetime
import requests
from bs4 import BeautifulSoup
import json
import sys

class data_scrapping:
    """Makes the webscrapping from a URL and get data from the schedule"""
    #Se obtiene el día de hoy
    today = datetime.now()
    #Se formatea el día de hoy a formato númerodedía
    todayFormated = today.strftime("%d")
    #Se hace un formato Mes_dd_aaaa_hh:mm
    formatDateOutput = today.strftime("%b_%d_%Y_%H_%M")

    def __init__(self, url, data_dir, hour):
        self._url = url
        self._data_dir = data_dir
        self._hour = hour

    def get_match_data(self):
        """Getting the schedule for tomorrow"""
        page = requests.get(self._url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            #se toma la lista de días de diciembre (tds), de la página
            listDays = soup.find_all('td', class_='day')
            #Se recorre la lista de días y se busca el que corresponda al día de mañana
            if(self.todayFormated <= '18'):
                for day in listDays:                                    #self.todayFormated # '05'
                    if(day.find('div', class_='date').get_text()[:2] == self.todayFormated):
                        #Se hace el procesamiento de los datos, horas en formato 'HH:MM'
                        datadict = self.get_Data(day, self._hour)
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
                return self.scrap_statistics(newURL['href'], penal_local, penal_visitante)

    def scrap_statistics(self, url, penal_local, penal_visitante):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            lineups = requests.get('https://resultados.as.com/' + soup.find('a', {'data-item':'lineups'})['href'])
            stats = requests.get('https://resultados.as.com/' + soup.find('a', {'data-item':'stats'})['href'])
            lineups_soup = BeautifulSoup(lineups.content, 'html.parser')
            stats_soup = BeautifulSoup(stats.content, 'html.parser')
            teams_names = lineups_soup.find_all('span', class_='large')
            scorers = lineups_soup.find_all('div', class_='scorers')
            scores = lineups_soup.find_all('span', class_='team-score')
            lineups_local = lineups_soup.find_all('ul', class_='team-lup')[1]
            lineups_visitor = lineups_soup.find_all('ul', class_='team-lup')[3]
            alings = stats_soup.find_all('div', class_='Opta-TeamFormation')
            posetion = stats_soup.find_all('span', class_='stat-val')
            penals = soup.find_all('p', class_='ki')
            
            data_dict = {
                'local': teams_names[0].text, 
                'alineacion_local': self.process_team_lineup(lineups_local),
                'posesion_local': posetion[0].text,
                'anotadores_local': self.validate_scorers(scorers[0]),
                'goles_local': (scores[0].text)[0], 
                'goles_def_penal_local': penal_local,
                'visitante': teams_names[1].text,
                'alineacion_visitante': self.process_team_lineup(lineups_visitor),
                'posesion_visitante': posetion[1].text,
                'anotadores_visitante': self.validate_scorers(scorers[1]),
                'goles_visitante':(scores[1].text)[0],
                'goles_def_penal_visitante': penal_visitante,
                'data_extra': self.process_extra_data(stats_soup.find_all('div', class_='stat-wr'))
            }
            return data_dict
        except:
            print('error en el metodo scrap_statistics')
            pass

    def validate_scorers(self, scorers): 
        if( (scorers.get_text()).replace('\n','') == '' ):
            return ''
        else:
            return (scorers.get_text()).replace('\n','')

    def process_team_lineup(self, lineups):
        players = []
        position = []
        linupDict = {}
        for player in lineups:
                if ((player.get_text()).replace('\n','') != ''):
                    if((player.get_text()).replace('\n','') != 'Banquillo'):
                        if((player.get_text()).split('\n')[1] == 'ent'):
                            linupDict['alineacion'] = (player.get_text()).split('\n')[3]
                        linupDict[(player.get_text()).split('\n')[1]] = (player.get_text()).split('\n')[2]
        return linupDict

    def process_extra_data(self, data_extra):
        extra_dict = {}
        for extra in data_extra[3:10]:
            extra_dict[(((extra.find('h4')).text).replace(' ', '_')).lower() + '_local'] = (extra.find_all('span', class_='stat-val')[0]).text
            extra_dict[(((extra.find('h4')).text).replace(' ', '_')).lower() + '_visitante'] = (extra.find_all('span', class_='stat-val')[1]).text
        return extra_dict

if __name__ == '__main__':
    url = 'https://colombia.as.com/resultados/futbol/mundial/calendario/dias/'
    data_dir = 'data/matchs/'
    hour = sys.argv[1]
    ds = data_scrapping(url, data_dir, hour)
    ds.get_match_data()