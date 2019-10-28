import re
import os
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup


# URL to be scraped
base_url = 'https://dir.indiamart.com'
final_output = './out/'
industry = final_output + 'Industrial Plants and Machineries/'
if not os.path.exists(industry):
    os.makedirs(industry)

categories = ['/indianexporters/m_miscel.html',
              '/indianexporters/m_prmach.html',
              '/indianexporters/m_grind.html',
              '/indianexporters/au_equip.html',
              '/indianexporters/conveyor-systems.html',
              '/indianexporters/e_furnce.html',
              '/impcat/heattransfer-exchangers.html']


per_indus_count = 0
missing_urls = 0
missing_addresses = 0


for category in categories:
    try:
        category_page = urllib.request.urlopen(base_url + category)
        category_soup = BeautifulSoup(category_page, 'html.parser')
        category_list = category_soup.find('section', attrs={'class': 'ctgry'})
        out_dir = industry + \
            category_soup.find(
                'span', attrs={
                    'id': base_url + category}).getText().strip() + '/'
    except Exception as e:
        print(
            f"++++++++++++++++++++++ WARNING : {e} : Skipping cat {category}")
        out_dir = None

    if (out_dir):
	    if not os.path.exists(out_dir): 
	    	os.makedirs(out_dir)	
	    	
	    per_cat_count = 0
	    try:
	    	subcategories = category_list.find_all('a', attrs={'class': 'GNTitle title'})
	    except Exception as e:
	    	print(f"============= Error fetching subcategories from {category} ... Skipping")

	    for c in subcategories:
	        query = c['href']

	        url = base_url + query

	        # Query the URL for its html
	        page = urllib.request.urlopen(url)

	        # Parsing the URL page into BeautifulSoup format
	        soup = BeautifulSoup(page, 'html.parser')

	        sellers = pd.DataFrame(columns=['Name', 'URL', 'Phone', 'Address'])
	        # Extracting vendor box from the webpage
	        vendor_list = soup.find('ul', attrs={'id': 'm'})
	        vendors = vendor_list.find_all('li', attrs={'id': re.compile('LST')})

	        for vendor_box in vendors:
	            try:
	                vendor_info_box = vendor_box.find(
	                    'div', attrs={'class': 'r-cl b-gry'})
	                vendor_url = vendor_info_box.find('a')
	                # print(vendor_url.text)
	                # print(vendor_url['href'])
	                vendor_number = vendor_info_box.find(
	                    'div', attrs={'id': re.compile('mobenq')}).getText()
	                vendor_number = vendor_number[4:]
	                vendor_number.strip()
	                # print(vendor_number)
	                # print(vendor_number.text)
	                vendor_address = vendor_info_box.find(
	                    'p', attrs={'class': 'sm clg'})
	                # print(vendor_address.text)
	                seller_url = vendor_url.text
	            except Exception as e:
	                print(
	                    f"!!!!!!!!!!!!! WARNING : Error fetching data: {e} !!!!!!!!!!!!!!")
	                missing_urls += 1
	                seller_url = "Missing"

	            try:
	                seller_address = vendor_address.text.strip()
	            except Exception as e:
	                print(
	                    f"00000000000 Warning : Seller Address not found {e} 00000000000")
	                missing_addresses += 1
	                seller_address = "Missing"
	            if (seller_url != "Missing"):
	                sellers = sellers.append({'Name': seller_url,
	                                          'URL': vendor_url['href'],
	                                          'Phone': vendor_number,
	                                          'Address': seller_address},
	                                         ignore_index=True)

	        print('Found : ' + str(len(sellers.index)) + ' Results')
	        per_cat_count += len(sellers.index)
	        per_indus_count += len(sellers.index)
	        sheet = c.text
	        print(sheet)
	        writer = ExcelWriter(out_dir + sheet + '.xlsx')
	        # TO DO : adapt script to write multiple sheets per file, one industry
	        # per file
	        sellers.to_excel(writer, sheet_name=sheet)
	        writer.save()
	        writer.close()
	    print("--------------------------------\
	    ------------------------------\
	    ------------------------------\
	    ******************************\
	    ******************************\
	    Found : " + str(per_cat_count) + " Results\
	    ******************************\
	    ******************************\
	    ------------------------------\
	    ------------------------------\
	    ------------------------------")
    else:
        print(f"Error fetching category {category} ... SKIPPING")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
        Found : " + str(per_indus_count) + " Results TOTAL !\
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(str(missing_urls) + " missings urls.")
print(str(missing_addresses) + " missing addresses")
