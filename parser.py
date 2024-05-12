import json
import requests
from bs4 import BeautifulSoup


class Formula2Parser:
    def __init__(self, url):
        self.url = url
        self.data = {
            "track": {},
            "drivers": {}
        }
        self.errors = False

    def fetch_html(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching site: {e}")
            self.errors = True
            return None

    # noinspection PyTypedDict
    def parse_html(self, html):
        if html:
            soup = BeautifulSoup(html, 'html.parser')

            self.data['track'] = self.parse_track_info(soup)
            self.data['drivers'] = {
                'Sprint Race Results': self.parse_drivers_info(soup, 0),
                'Feature Race Results': self.parse_drivers_info(soup, 1),
                'Qualifying Session Results': self.parse_drivers_info(soup, 2),
                'Free Practice Results': self.parse_drivers_info(soup, 3)
            }

    def parse_track_info(self, soup):
        country = soup.find('div', {'class': 'country-circuit-name'}).text.strip() if soup.find(
            'div', {'class': 'country-circuit-name'}) else "Country Not Found"
        city = soup.find('div', {'class': 'country-circuit'}).text.strip() if soup.find('div', {
            'class': 'country-circuit'}) else "City Not Found"
        track_name = soup.find('div', {'class': 'circuit-heading'}).text.split(f'{city.upper()}')[
            0].strip() if soup.find('div', {'class': 'circuit-heading'}) else "Track Name Not Found"
        date = soup.find('div', {'class': 'schedule'}).text.split('|')[-1].strip() if soup.find(
            'div', {'class': 'schedule'}) else "Date Not Found"

        length_label = soup.find('div', {'class': 'first-row'})
        if length_label:
            length_value = length_label.find_all('p', {'class': 'value skew-border'})[1]
            length = length_value.span.text.split("\n")[
                0].strip() if length_value and length_value.span else "Length Not Found"
        else:
            length = "Length Not Found"

        return {
            'Track Name': track_name.replace(city.upper(), '').replace(country.upper(), '').replace('Latest News', '').strip(),
            'Country': country,
            'City': city,
            'Date': date,
            'Length (Km)': length.replace(' KM', '')
        }

    def parse_drivers_info(self, soup, category):
        results = []
        main_div = soup.find_all('div', {'class': 'collapsible'})[category]
        table = main_div.find('table', {'class': 'table table-bordered'}) if main_div else None
        if not table:
            return "No table found for category"

        rows = table.find_all('tr')[1:]
        for row in rows:
            cells = row.find_all('td')
            pos = cells[0].find('div', {'class': 'pos'}).text.strip() if cells[0].find('div', {
                'class': 'pos'}) else "Position Not Found"
            car_no = cells[0].find('div', {'class': 'car-no'}).text.strip() if cells[0].find('div',
                                                                                             {
                                                                                                 'class': 'car-no'}) else "Car Number Not Found"
            driver_name = cells[0].find('span', {'class': 'visible-desktop-up'}).text.strip() if \
                cells[0].find('span', {'class': 'visible-desktop-up'}) else "Driver Name Not Found"
            team_name = cells[0].find('span', {'class': 'team-name'}).text.strip() if cells[0].find(
                'span', {'class': 'team-name'}) else "Team Name Not Found"
            laps = cells[1].text.strip()
            time = cells[2].text.strip()
            gap = cells[3].text.strip()
            interval = cells[4].text.strip()
            kph = cells[5].text.strip()
            best = cells[6].text.strip()

            results.append({
                'Position': int(pos) if pos.isdigit() else pos,
                'Car Number': int(car_no) if car_no.isdigit() else car_no,
                'Driver Name': driver_name,
                'Team Name': team_name,
                'Laps': int(laps) if laps.isdigit() else laps,
                'Time': time,
                'Gap': gap if gap != '-' else 0,
                'Interval': interval if interval != '-' else 0,
                'KPH': float(kph) if kph.replace('.', '').isdigit() else kph,
                'Best Lap Time': best,
            })

        return results

    def append_data_to_json(self, filename = 'output.json'):
        if not self.errors:
            try:
                with open(filename, 'r', encoding = 'utf-8') as json_file:
                    existing_data = json.load(json_file)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_data = {}

            existing_data[self.url] = self.data

            with open(filename, 'w', encoding = 'utf-8') as json_file:
                json.dump(existing_data, json_file, ensure_ascii = False, indent = 4)

    def run(self):
        html = self.fetch_html()
        if html:
            self.parse_html(html)
            self.append_data_to_json()
