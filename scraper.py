import re
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup




# URL to be scraped
base_url = 'https://dir.indiamart.com'
category = '/indianexporters/m_miscel.html'
category_page = urllib.request.urlopen(base_url + category)
category_soup = BeautifulSoup(category_page, 'html.parser')
category_list = category_soup.find('section', attrs={'class':'ctgry'})
out_file = category_soup.find('span', attrs={'id':base_url+category}).getText().strip()
for c in category_list.find_all('a', attrs={'class':'GNTitle title'}):
    query = c['href']

    url = base_url + query

    # Query the URL for its html
    page = urllib.request.urlopen(url)

    # Parsing the URL page into BeautifulSoup format
    soup = BeautifulSoup(page, 'html.parser')

    sellers = pd.DataFrame(columns=['Name', 'URL', 'Phone', 'Address'])
    #Extracting vendor box from the webpage
    vendor_list = soup.find('ul', attrs={'id':'m'})
    vendors = vendor_list.find_all('li', attrs={'id':re.compile('LST')})

    for vendor_box in vendors:
        vendor_info_box = vendor_box.find('div', attrs={'class':'r-cl b-gry'})
        vendor_url = vendor_info_box.find('a')
        #print(vendor_url.text)
        #print(vendor_url['href'])
        vendor_number = vendor_info_box.find('div', attrs={'id':re.compile('mobenq')}).getText()
        vendor_number = vendor_number[4:]
        vendor_number.strip()
        #print(vendor_number)
        #print(vendor_number.text)
        vendor_address = vendor_info_box.find('p', attrs={'class':'sm clg'})
        #print(vendor_address.text)
        sellers = sellers.append({'Name':vendor_url.text, 'URL':vendor_url['href'], 'Phone':vendor_number, 'Address':vendor_address.text.strip()}, ignore_index=True)

    print('Found : ' + str(len(sellers.index)) + ' Results')
    
    sheet = c.text
    print(sheet)
    writer = ExcelWriter(out_file+'.xlsx')
    sellers.to_excel(writer,sheet_name=sheet) # TO DO : adapt script to write multiple sheets per file, one industry per file
    writer.save()
    writer.close()
