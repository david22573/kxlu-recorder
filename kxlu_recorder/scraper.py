from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import os

URL = 'https://kxlu.com/schedule/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}
HTML_FILE = 'kxlu.html'


def get_site_content():
    """Fetch site content and save to a local HTML file."""
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        html = response.text

        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            print("Content refreshed")
            f.write(html)

        return html
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL content: {e}")
        return None


def read_html_file(file_path):
    """Read HTML content from a local file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def sanitize_time(time_str: str):
    """Convert a time string to a day and time range."""
    day, _time = time_str.split(' ', 1)
    schedule_time = [t.strip() for t in _time.split('-')]
    schedule_range = [datetime.strptime(
        t.strip(), '%I:%M %p').strftime('%H:%M') for t in schedule_time]
    return (day, tuple(schedule_range)) if len(schedule_range) > 1 else (day, schedule_range[0])


def get_djs():
    """Extract DJ schedule information from the HTML content."""
    djs = {}
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]

    if not html_files or datetime.now() - datetime.fromtimestamp(os.path.getmtime(html_files[0])) > timedelta(days=1):
        html_content = get_site_content()
    else:
        html_content = read_html_file(html_files[0])

    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        schedule_grid = soup.find('section', class_='schedule-grid')

        for schedule_item in schedule_grid.find_all('div', class_='tooltip-details'):
            dj_name = schedule_item.find('h4').text.upper()
            schedule_time = schedule_item.find('span', class_='time').text
            day, schedule_time = sanitize_time(schedule_time)
            djs.setdefault(dj_name, {}).setdefault(day[:-1], schedule_time)

    return djs


def main():
    """Main function to get DJs and print their schedule."""
    djs = get_djs()
    print(djs)
    # for name in djs:
    # shows = djs[name]
    # print(name)
    # print(shows)


if __name__ == '__main__':
    main()
