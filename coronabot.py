import datetime
import json
import requests
import argparse
import logging
from bs4 import BeautifulSoup
from tabulate import tabulate
import pymsteams

DEFAULT_TEAMS_WEBHOOK = '<Teams Webhook URL>'

FORMAT = '[%(asctime)-15s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG,
                    filename='bot.log', filemode='a')

URL = 'https://www.mohfw.gov.in/'
SHORT_HEADERS = ['Sno', 'State', 'Confirmed Indians',
                 'Confirmed Foreigners', 'Cured', 'Death']
FILE_NAME = 'corona_india_data.json'


def extract_contents(row): return [x.text.replace('\n', '') for x in row]


def save(x):
    with open(FILE_NAME, 'w') as f:
        json.dump(x, f)


def load():
    res = {}
    with open(FILE_NAME, 'r') as f:
        res = json.load(f)
    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--states', default=',')
    args = parser.parse_args()
    interested_states = args.states.split(',')

    current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    info = []

    try:
        response = requests.get(URL).content
        soup = BeautifulSoup(response, 'html.parser')
        header = extract_contents(soup.tr.find_all('th'))

        stats = []
        all_rows = soup.find_all('tr')
        for row in all_rows:
            stat = extract_contents(row.find_all('td'))
            if stat:
                if len(stat) == 5:
                    # last row
                    stat = ['', *stat]
                    stats.append(stat)
                elif any([s.lower() in stat[1].lower() for s in interested_states]):
                    stats.append(stat)

        past_data = load()
        cur_data = {x[1]: {current_time: x[2:]} for x in stats}

        changed = False

        for state in cur_data:
            if state not in past_data:
                # handling condition when new state has emerged
                info.append(
                    f'NEW_STATE {state} got corona virus: {cur_data[state][current_time]}')
                past_data[state] = {}
                changed = True
            else:
                past = past_data[state]['latest']
                cur = cur_data[state][current_time]
                if past != cur:
                    changed = True
                    info.append(f'Change for {state}: {past}->{cur}')

        events_info = ''
        for event in info:
            logging.warning(event)
            events_info += '<br> - ' + event.replace("'", "")

        if changed:
            # override the latest one now
            for state in cur_data:
                past_data[state]['latest'] = cur_data[state][current_time]
                past_data[state][current_time] = cur_data[state][current_time]
            save(past_data)

            table = tabulate(stats, headers=SHORT_HEADERS, tablefmt='html')
            print(events_info)
            print('hello')
            events_info = '<p>'+events_info+'</p>'
            teams_text = '<h2>Please find Latest CoronaVirus Summary for India below:</h2><br>'
            teams_text += events_info+table

            myTeamsMessage = pymsteams.connectorcard(DEFAULT_TEAMS_WEBHOOK)
            myTeamsMessage.text(teams_text)
            myTeamsMessage.send()
    except Exception as e:
        logging.exception('oops, corono script failed.')
        myTeamsMessage = pymsteams.connectorcard(DEFAULT_TEAMS_WEBHOOK)
        myTeamsMessage.text(
            'Exception occured: [{e}]<br>Scraping format changed on host website.')
        myTeamsMessage.send()
