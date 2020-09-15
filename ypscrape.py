import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import lxml

import pandas as pd


search_name = input('Please, enter a search term name:\n')
location_name = input('Please enter a location (no commas):\n')
formated_search_name = search_name.replace(' ', '+')
formated_location_name = location_name.replace(' ', '+')
print(f'Searching {search_name} in {location_name}. Wait, please...')


base_url = 'https://www.yellowpages.com'
search_url = f'https://www.yellowpages.com/search?search_terms={formated_search_name}&geo_location_terms={formated_location_name}'


    
data = {
  'Business Name': [],
  'Phone Number': [],
  'Address One': [],
  'Address Two': [],
}

def export_table_and_print(data):
    table = pd.DataFrame(data, columns=['Business Name', 'Phone Number', 'Address One', 'Address Two'])
    table.index = table.index +1
    table.to_csv(f'{location_name}_{search_name}.csv', sep=',', encoding='utf-8', index=False)
    print(table)

# grabbing all of the data i'm looking for
def get_leads(container):
    name_span = container.h2.span
    bname = name_span.text.strip() if name_span else ''

    phone_container = container.find("div",{"class":"phones phone primary"})
    pnumber = phone_container.text.strip() if phone_container else ''

    adrone_container = container.find("div",{"class":"street-address"})
    adrone = adrone_container.text.strip() if adrone_container else ''

    adrtwo_container = container.find("div",{"class":"locality"})
    adrtwo = adrtwo_container.text.replace(',', '') if adrtwo_container else ''
    
    # stores data into the table
    data['Business Name'].append(bname)
    data['Phone Number'].append(pnumber)
    data['Address One'].append(adrone)
    data['Address Two'].append(adrtwo)

def parse_page(url):
    # HTTP GET requests
    page = requests.get(url)

    # if page.status_code == requests.codes.ok:
    bs = BeautifulSoup(page.text, 'lxml')

        # check_no_results = bs.find("div",{"class":"v-card"})
        # if check_no_results and check_no_results.text:
        #     print('Search returned no results.')
        #     return None 

    list_all_businesses = bs.findAll("div",{"class":"v-card"})    

    container = list_all_businesses[0]

    for container in list_all_businesses:
        get_leads(container)

    next_page_text = bs.find('div',{"class":"pagination"}).find('ul').findAll('li')[-1].text


    if next_page_text == "Next":
        next_page_partial = bs.find('div',{"class":"pagination"}).find('ul').findAll('li')[-1].find('a')['href']
        next_page_url = base_url + next_page_partial
        parse_page(next_page_url)
    else:
        export_table_and_print(data)

parse_page(search_url)
