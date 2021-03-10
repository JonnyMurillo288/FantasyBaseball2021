import requests
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np 
from selenium.webdriver import Firefox
import geckodriver_autoinstaller
geckodriver_autoinstaller.install()


##=================== TOP 100 PROSPECTS ++++ DIVIDE THEM BY ETA 2021 AND 2022============##

top_100_spect = 'https://blogs.fangraphs.com/2021-top-100-prospects/'
url = requests.get(top_100_spect)
soup = BeautifulSoup(url.content, 'html.parser')
top_table = soup.find('table',{'class' : 'sortable'})
df = pd.read_html(str(top_table))[0] #base df 
prospects_2021 = df.loc[df['ETA'] == '2021'] #split by eta THIS IS THE DF
print(prospects_2021)
prospects_2022 = df.loc[df['ETA'] == '2022']
eta_2021_ls = [name for name in prospects_2021['Name']] #lists of prospects in their year
eta_2022_ls = [name for name in prospects_2022['Name']]
header_name = soup.find_all('div', {'class' : 'header-name'})
eta_2021_links = {}
eta_2022_links = {}
#Find players name, attach fangraphs page link to dict
for name in header_name:
    for link in name.find_all('a'): 
        player = (str(link).strip('<a href="//www.fangraphs.com/statss.aspx?playerid=0123456789'))
        if player[1:-4] in eta_2021_ls:
            eta_2021_links[player[1:-4]] = link.get('href')
        elif player[1:-4] in eta_2022_ls:
            eta_2022_links[player[1:-4]] = link.get('href')
        else:
            continue

print(prospects_2021)
##================= FIND BREAKOUTS AND COMBACKS IN ARTICLE ======================##

pitchers = 'https://www.mlb.com/news/breakout-pitcher-candidates-2021'
hitters = 'https://www.mlb.com/news/breakout-hitter-candidates-2021'
best_in_rotation = 'https://www.mlb.com/news/marlins-could-have-elite-rotation-2021'
sophomores = 'https://www.mlb.com/news/best-rookie-pitchers-from-2020'
bounceback = 'https://www.mlb.com/news/mlb-stars-who-should-bounce-back-in-2021'
veterans = 'https://www.mlb.com/news/analyzing-2020-declining-hitters'
spring_notables = 'https://www.mlb.com/news/most-interesting-players-spring-training-2021'
under_25 = 'https://www.mlb.com/news/mlb-best-players-under-25'

breakout_players_dict = {} #dict KEY: player name Value: player MLBAM ID
bounceback_dict = {}
veteran_comback_dict = {}


def breakout_players(url,dict):
    r = requests.get(url)

    soup = BeautifulSoup(r.content,'html.parser')
    players = soup.find_all('a',{'rel':'tag'})

    for a in players:
        player_id = str(a).strip('<a data-reactroot= href="/player/')
        player_id = player_id[0:6]
        dict[a.text] = player_id

# breakout_players(pitchers,breakout_players_dict) +================ Can potentially use this if =============+
# breakout_players(hitters,breakout_players_dict)  +================ I want to add my own players ============+
breakout_players(best_in_rotation,breakout_players_dict)
breakout_players(sophomores,breakout_players_dict)
breakout_players(veterans,veteran_comback_dict)
breakout_players(bounceback,bounceback_dict)
breakout_players(spring_notables,bounceback_dict)
breakout_players(under_25,breakout_players_dict)






    






