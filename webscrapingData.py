from datetime import date, timedelta, datetime
import requests
from bs4 import BeautifulSoup
import json

class data_scrapping:
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


if __name__ == '__main__':
    url = 'https://www.skysports.com/football/news/12098/12354033/world-cup-2022-dates-draw-schedule-kick-off-times-final-for-qatar-tournament'
    data_dir = 'data/matchs/'
    ds = data_scrapping(url, data_dir)
    ds.get_data()