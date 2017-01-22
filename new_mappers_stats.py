#!/usr/bin/env python2
"""
graf odoslanych privitacich sprav pre OSM novacikov
 - sluzi pre priblizny odhad poctu novych maperov

zobrazeny je graf poctu sprav po tyzdnoch a kumulovany
pocet po mesiacoch.

nakolko vstupne data zavisia od spravneho fungovania
skriptu na odosielanie privitacich sprav, treba na to
pri intepretovani vysledkov mysliet.

"""
import requests
import logging
import bs4
import time
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from urllib2 import quote
from calendar import month_abbr as mn
from collections import OrderedDict
from datetime import datetime, timedelta

cookies = ''

# these two variables need to be pupulated
senderlogin = ''
senderpass = ''

logging.basicConfig(level=logging.DEBUG)

def osm_auth():
        global cookies
        logging.debug('Authenticating..')
        r = requests.get('https://www.openstreetmap.org/')
        cookies = r.cookies
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        token = soup.find('meta', attrs={'name': 'csrf-token'})['content']
        data = {
            'username': senderlogin,
            'password': senderpass,
            'authenticity_token': token
            }
        r = requests.post('https://www.openstreetmap.org/login',
                          data=data, cookies=cookies)
        logging.debug('OSM cookies: %s' % cookies)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        token = soup.find('meta', attrs={'name': 'csrf-token'})['content']
        if token:
            return token
        else:
            raise Exception("token could not be obtained")

token = osm_auth()
data = {'authenticity_token': token}

outbox_url = 'https://www.openstreetmap.org/user/{0}/outbox'.format(quote(senderlogin))
r = requests.get(outbox_url, cookies=cookies, data=data)
soup = bs4.BeautifulSoup(r.text, 'html5lib')

# filter only messages with subject == "Privitanie" 
greeting_messages = [x for x in soup.find_all('tr', attrs={'class': 'inbox-row'})
                     if x.select('td.inbox-subject')[0].text in 'Privitanie']

index = []
for msg in greeting_messages:
    index.append(pd.to_datetime(msg.select('td.inbox-sent')[0].text))

df = pd.DataFrame({'# of new editors': [1] * len(index)}, index=index)
monthly = df.groupby(df.index.month).sum()
monthly = monthly.rename(index=lambda n: mn[int(n)])
monthly.plot(title='New OSM editors by months (cumulative)')

weekly = df.groupby(lambda n: str(n.year)+'/'+str(n.week)).sum()
weekly = weekly.reindex(['{0.year}/{0.week}'.format(x) for x in pd.date_range('20150101',end=pd.datetime.today(), freq='7D')])
weekly.fillna(0, inplace=True)
weekly.plot(title='New OSM editors in Slovakia by weeks')
plt.show()
