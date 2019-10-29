import sys
import re
import os
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup


base_url = 'https://dir.indiamart.com'


def ExtractProducts(sellers,categories, base_url=base_url, output='./out/'):


    log_dir = './Logs/'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    old_stdout = sys.stdout
    log_file = open(log_dir+"extractProducts.log","w")
    sys.stdout = log_file


    per_indus_count = 0
    missing_urls = 0
    missing_addresses = 0

    for i in range(len(categories.index)):
        row = categories.iloc[i]
        category = row['URL']
        category_name = row['Name']
        category_s_industry = row['Industry']
        out_dir = output + category_s_industry + '/' + category_name + '/'
        out_dir_exists = False
        try:
            category_page = urllib.request.urlopen(base_url + category)
            category_soup = BeautifulSoup(category_page, 'html.parser')
            category_list = category_soup.find('section', attrs={'class': 'ctgry'})
        except Exception as e:
            print(
                f"++++++++++++++++++++++ WARNING : {e} : Skipping cat {category}")
            category_list = None

        if (category_list):		    	
            per_cat_count = 0
            try:
            	products = category_list.find_all('a', attrs={'class': 'GNTitle title'})
            except Exception as e:
            	print(f"============= Error fetching products from {category} ... Skipping")
            	products = []

        	# for c in products: # Production loop
            for c in [products[0]]: # Testing : fetch one seller from each product page
                query = c['href']

                url = base_url + query

                # Query the URL for its html
                page = urllib.request.urlopen(url)

                # Parsing the URL page into BeautifulSoup format
                soup = BeautifulSoup(page, 'html.parser')

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
                        seller_url = None

                    try:
                        seller_address = vendor_address.text.strip()
                    except Exception as e:
                        print(
                            f"00000000000 Warning : Seller Address not found {e} 00000000000")
                        missing_addresses += 1
                        seller_address = "Missing"
                    if (seller_url):
                        sellers = sellers.append({'Name': seller_url,
                                                  'URL': vendor_url['href'],
                                                  'Phone': vendor_number,
                                                  'Address': seller_address,
                                                  'Category': category_name,
                                                  'Industry': category_s_industry},
                                                 ignore_index=True)


                print(f'--------------------------------------- Found : {len(sellers.index)}  Results so far ----- ')
                per_cat_count += len(sellers.index)
                per_indus_count += len(sellers.index)
                sheet = c.text
                print(f"Sheet name : {sheet}")
                if not out_dir_exists:
                	os.makedirs(out_dir)
                	out_dir_exists = True

                writer = ExcelWriter(out_dir + sheet + '.xlsx') # TO DO : adapt script to write multiple sheets per file, one industry per file
                sellers.to_excel(writer, sheet_name=sheet)
                writer.save()
                writer.close()
        else:
        	print(f"Error fetching {category} ... SKIPPING")
    print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Found : {len(sellers.index)} Results TOTAL !  ~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(str(missing_urls) + " missings urls.")
    print(str(missing_addresses) + " missing addresses")

    sys.stdout = old_stdout
    log_file.close()

    return sellers



categories = pd.DataFrame(columns=['Name', 'URL','Industry'])
categories = categories.append({'Name': 'Test CAT',
								'URL':'/indianexporters/glue.html',
								'Industry': 'Test Industry'},
								ignore_index=True)


sellers = pd.DataFrame(columns=['Name', 'URL', 'Phone', 'Address','Category','Industry'])

sellers = ExtractProducts(sellers,categories,base_url)
print(sellers.iloc[:10,:])