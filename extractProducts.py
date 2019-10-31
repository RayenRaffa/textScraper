import sys
import re
import os
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup




def ExtractProducts(base_url, category, out_dir='./out', log_dir=None):

    if(log_dir):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        old_stdout = sys.stdout
        log_file = open(log_dir + "extractProducts.log", "a")
        sys.stdout = log_file

    category_name       = category[1].strip()
    category_url        = category[2].strip()
    category_s_industry = category[3].strip()  # Tuple = [Index, Name, URL, Industry]
    cat_out_dir = out_dir + '/' + category_s_industry + '/' + category_name
    try:
        category_page = urllib.request.urlopen(category_url)
        category_soup = BeautifulSoup(category_page, 'html.parser')
        category_box = category_soup.find_all(
            'section', attrs={'class': 'ctgry'})
    except Exception as e:
        print(
            f"++++++++++++++++++++++ WARNING : {e} : Skipping cat {category}")
        category_box = []

    subCategories = pd.DataFrame(columns=['Name','URL','Category','Industry'])
    products = pd.DataFrame(columns=['Name','URL','Availabel SKUs','subCategory','Category','Industry'])

    for cat in category_box:
        try:
           	subCategory_box = cat.find_all('li', attrs={'class': 'box'})
        except Exception as e:
            print(f"Error fetching subCategory_box from {category_name} ... Skipping")
            subCategory_box = []

        for subCategory in subCategory_box:
            products_per_subCat = pd.DataFrame(columns=['Name', 'URL','Available SKUs','subCategory','Category','Industry'])
            try:
                subCategory_soup = subCategory.find('a', attrs={'class':'GNTitle title'})
                subCategory_name = subCategory_soup.getText().strip()
                subCategory_url  = base_url + subCategory_soup['href']
                subCategories    = subCategories.append({'Name':subCategory_name,
                                                            'URL':subCategory_url,
                                                            'Category':category_name,
                                                            'Industry':category_s_industry})
            except Exception as e:
                print(f"Error fetching subCategory data\n{e}\nProceeding to products in subCategory")
                subCategory_name = 'Other products'

            subCat_out_dir = cat_out_dir + '/' + subCategory_name
            try:
                products_box = subCategory_box.find_all('div', attrs={'class':'lik'})
            except Exception as e:
                print(f"Error fetching products from subCategory\n{e}\n SKIPPINg ...")
                products_box = []

            for prod_box in products_box:
                try:
                    prod_soup = prod_box.find('a', href=true)
                    prod_url  = base_url + prod_soup['href']
                    prod_name = prod_soup.getText().strip()
                    prod_sku_number = prod_box.find('span').getText().strip(')(')
                    data = pd.DataFrame({'Name':prod_name,
                                                'URL':prod_url,
                                                'Available SKUs':prod_sku_number,
                                                'subCategory': subCategory_name,
                                                'Category':category_name,
                                                'Industry':category_s_industry})
                    products_per_subCat = products_per_subCat.append(data,ignore_index=True)
                    products = products.append(data, ignore_index=True)
                except Exception as e:
                    print(f"Error fetching product from {subCategory_name}\n{e} : SKIPPING ..")
                
                if not os.path.exists(subCat_out_dir):
                    os.makedirs(subCat_out_dir)
                writer = ExcelWriter(subCat_out_dir + '/products.xlsx') # TO DO : adapt script to write multiple sheets per file, one industry per file
                products_per_subCat.to_excel(writer,startrow = writer.sheets['Sheet1'].max_row, index=False)
                writer.save()
                writer.close()
                print(f"\nSaved products of {subCategory_name} data at {subCat_out_dir}/products.xlsx")
        
        if not os.path.exists(cat_out_dir):
            os.makedirs(cat_out_dir)
        writer = ExcelWriter(cat_out_dir + '/subCategories.xlsx') # TO DO : adapt script to write multiple sheets per file, one industry per file
        subCategories.sort_values('Name',inplace=True)
        subCategories.drop_duplicates('URL',inplace=True)
        subCategories.to_excel(writer,startrow = writer.sheets['Sheet1'].max_row, index=False)
        writer.save()
        writer.close()
        print(f"Found {len(subCategories.index)} subCategories TOTAL in category : {category_name}\nSaved data at {cat_out_dir}/subCategories.xlsx")


        writer = ExcelWriter(cat_out_dir + '/products.xlsx') # TO DO : adapt script to write multiple sheets per file, one industry per file
        products = products.append(subCategories, ignore_index=True)
        products.sort_values('Name',inplace=True)
        products.drop_duplicates('URL',inplace=True)
        products.to_excel(writer,startrow = writer.sheets['Sheet1'].max_row, index=False)
        writer.save()
        writer.close()
        print(f"Found {len(products.index)} products TOTAL in category : {category_name}\nSaved data at {cat_out_dir}/products.xlsx")






    if(log_dir):
        sys.stdout = old_stdout
        log_file.close()

    return products



# categories = pd.DataFrame(columns=['Name', 'URL','Industry'])
# categories = categories.append({'Name': 'Test CAT',
# 								'URL':'/indianexporters/glue.html',
# 								'Industry': 'Test Industry'},
# 								ignore_index=True)


# sellers = pd.DataFrame(columns=['Name', 'URL', 'Phone', 'Address','Category','Industry'])

# sellers = ExtractProducts(sellers,categories,base_url)
# print(sellers.iloc[:10,:])
