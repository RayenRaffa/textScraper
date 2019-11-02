import sys
import re
import os
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup


def ExtractVendors(base_url,product,out_dir='./out',log_dir=None):

    if(log_dir):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = open(log_dir + "extractProducts.log", "a")
        old_stdout = sys.stdout
        sys.stdout = log_file

    prod_name   = product[1] # Product is a tuple : [Index, Name, URL, subCategory, Category, Industry]
    prod_url    = product[2]
    prod_subCat = product[3]
    prod_cat    = product[4]
    prod_indus  = product[5]

    # Query the URL for its html
    prod_page = urllib.request.urlopen(prod_url)

    # Parsing the URL page into BeautifulSoup format
    prod_soup = BeautifulSoup(prod_page, 'html.parser')

    # Extracting vendor box from the webpage
    vendor_list = prod_soup.find('ul', attrs={'id': 'm'})
    vendors_box = vendor_list.find_all('li', attrs={'id': re.compile('LST')})
    vendors = pd.DataFrame(columns={'Name','URL','Phone','Address','Category','Industry'})

    for vendor_box in vendors_box:
        try:
            vendor_info_box = vendor_box.find(
                'div', attrs={'class': 'r-cl b-gry'})
            vendor_info = vendor_info_box.find('a', href=True)
            vendor_name = vendor_info.getText().strip()
            vendor_url  = vendor_info['href']
            # print(vendor_url.text)
            # print(vendor_url['href'])
            vendor_number = vendor_info_box.find('div', attrs={'id': re.compile('mobenq')}).getText()
            vendor_number = vendor_number.strip('cCaAlL')
            # print(vendor_number)
            # print(vendor_number.text)
            vendor_address = vendor_info_box.find('p', attrs={'class': 'sm clg'}).getText().strip()
            # print(vendor_address.text)
            vendors = vendors.append({'Name': vendor_name,
                                      'URL': vendor_url,
                                      'Phone': vendor_number,
                                      'Address': vendor_address,
                                      'Category': prod_cat,
                                      'Industry': prod_indus},
                                     ignore_index=True, sort=False)
        except Exception as e:
            print(f"\n!!!!!!!!!!!!!  Error fetching vendor data\n{e} .. SKIPPING ...\n")

    if (len(vendors.index) > 0):
        vendors.sort_values('Name', inplace=True)
        vendors.drop_duplicates('URL', inplace=True)
        vendors = vendors[['Name','URL','Phone','Address','Category','Industry']]
        print(f'\nFound : {len(vendors.index)}  vendors in {prod_name} .. creating file ...\n')
        prod_out_dir = out_dir + '/' + prod_indus + '/' + prod_cat + '/' + prod_subCat
        vendors_file = prod_out_dir + '/vendors_' + prod_name + '.xlsx'
        if not os.path.exists(prod_out_dir):
            os.makedirs(prod_out_dir)
        writer = ExcelWriter(vendors_file) # TO DO : adapt script to write multiple sheets per file, one industry per file
        vendors.to_excel(writer, index=False)
        writer.save()
        writer.close()
    else:
        print(f"\nNo vendors found at {prod_url} : SKIPPING ..\n")

    if(log_dir):
        sys.stdout = old_stdout
        log_file.close()


    return vendors
