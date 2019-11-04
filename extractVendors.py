import sys
import re
import os
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup


def ExtractVendors(product,out_dir='./out',log_dir=None):

    if(log_dir):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = open(log_dir + "extractProducts.log", "a")
        old_stdout = sys.stdout
        sys.stdout = log_file

    prod_name   = product.Name # Product is a tuple : [Index, Name, URL, subCategory, Category, Industry]
    prod_url    = product.URL
    prod_subCat = product.subCategory
    prod_cat    = product.Category
    prod_indus  = product.Industry

    # Query the URL for its html
    try:
        prod_page = urllib.request.urlopen(prod_url)
    except Exception as e:
        print(f"Error fetching product URL\n{e}\nSkipping ..")
        prod_page = None


    vendors = pd.DataFrame(columns={'Name','URL','Phone','Address','Category','Industry'})
    
    
    if(prod_page):
        # Parsing the URL page into BeautifulSoup format
        prod_soup = BeautifulSoup(prod_page, 'html.parser')

        # Extracting vendor box from the webpage
        vendor_list = prod_soup.find('ul', attrs={'id': 'm'})
        vendors_box = vendor_list.find_all('li', attrs={'id': re.compile('LST')})

        for vendor_box in vendors_box:
            try:
                vendor_info_box = vendor_box.find(
                    'div', attrs={'class': 'r-cl b-gry'})
                vendor_info = vendor_info_box.find('a', href=True)
                vendor_name = vendor_info.getText().strip()
                vendor_url  = vendor_info['href']
                # print(vendor_url.text)
                # print(vendor_url['href'])
                try:
                    vendor_number = vendor_info_box.find('div', attrs={'id': re.compile('mobenq')}).getText()
                    vendor_number = vendor_number.strip('cCaAlL')
                    # print(vendor_number)
                    # print(vendor_number.text)
                except Exception as e:
                    print(f"!! !! Error fetching vendor phone\n{e}\n")
                    vendor_number = 'Not Found'
                try:
                    vendor_address = vendor_info_box.find('p', attrs={'class': 'sm clg'}).getText().strip()
                    # print(vendor_address.text)
                except Exception as e:
                    print(f"!! Error fetching vendor address\n{e}\n")
                    vendor_address = 'Not Found'
                    
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
            print(f'\nFound : {len(vendors.index)}  vendors in {prod_name} : creating file ...')
            prod_out_dir = out_dir + '/' + prod_indus + '/' + prod_cat + '/' + prod_subCat
            vendors_file = prod_out_dir + '/vendorsOf_' + prod_name + '.xlsx'
            if not os.path.exists(prod_out_dir):
                os.makedirs(prod_out_dir)
            writer = ExcelWriter(vendors_file) # TO DO : adapt script to write multiple sheets per file, one industry per file
            try:
                vendors.to_excel(writer, index=False)
                writer.save()
                print(f"Saved vendors of {prod_name} at:\n{vendors_file}\n")
                writer.close()
            except Exception as e:
                print(f"\n***** Error saving to {vendors_file}\n{e}\nSkipping ..")
                del writer
        
        else:
            print(f"\nNo vendors found at {prod_url} : SKIPPING ..\n")
        
    if(log_dir):
        sys.stdout = old_stdout
        log_file.close()


    return vendors


g_vendors = pd.DataFrame(columns={'Name','URL','Phone','Address','Category','Industry'})
file_name = './out/all_products.xlsx'
products = pd.read_excel(file_name)
i = 1
ttl_prods = len(products.index)
for product in products.itertuples():
    if i < 17175:
        print("Skipping scraped product URL...")
    else:
        vendors = ExtractVendors(product)
        g_vendors = g_vendors.append(vendors, ignore_index=False)
        del vendors
        print(f"\n\n%%% {i*100/ttl_prods}% of products scanned ..")
    i += 1


g_vendors.sort_values('Name',inplace=True)
g_vendors.drop_duplicates('URL',inplace=True)
writer = ExcelWriter('./out/all_vendors.xlsx')
try:
    g_vendors.to_excel(writer, index=False, encoding='UTF-8')
    writer.save()
    writer.close()
    print(f"Found {len(g_vendors.index)} distinct vendors !\nRecap file saved as XLSX at {file_name}")
except Exception as e:
    print(f"Error saving recap file as XLSX")
    writer.close()

g_vendors.to_csv('./out/all_vendors.csv',index=False,sep='|',encoding='UTF-8')
print(f"Recap file saved as CSV at ./out/all_vendors.csv\nDONE")