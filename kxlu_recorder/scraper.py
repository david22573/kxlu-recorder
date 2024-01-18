from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import os
import re


def get_site_content():
    url = 'https://kxlu.com/schedule/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    html = response.text

    with open('kxlu.html', 'w', encoding='utf-8') as f:
        print("content refreshed")
        f.write(html)

    return html


def sanitize_time(time_str: str):
    day = time_str.split(' ')[0]
    _time = time_str[len(day):]
    schedule_time = [t.strip() for t in _time.split('-')]
    schedule_range = []
    for time_range in schedule_time:
        time_obj = datetime.strptime(time_range.strip(), '%I:%M %p')
        clean_time = time_obj.strftime('%H:%M')
        schedule_range.append(clean_time)
    return (day, schedule_range) if len(schedule_range) > 1 else (day, schedule_range[0])


def get_djs():
    djs = {}
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    if not html_files or datetime.now() - datetime.fromtimestamp(os.path.getmtime(html_files[0])) > timedelta(days=1):
        html_content = get_site_content()
    else:
        with open(html_files[0], 'r', encoding='utf-8') as f:
            html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    schedule_grid = soup.find('section', class_='schedule-grid')

    for schedule_item in schedule_grid.find_all('div', class_='tooltip-details'):
        dj_name = schedule_item.find('h4').text
        schedule_time = schedule_item.find('span', class_='time').text
        day, schedule_time = sanitize_time(schedule_time)
        djs[dj_name][day] = [] if dj_name not in djs else djs[dj_name][day]
        djs[dj_name][day].append(schedule_time)
    return djs


djs = get_djs()
print(djs)
# print(djs['In a Dream with Mystic Pete'])
