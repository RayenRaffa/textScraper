import sys
import re
import os
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup


# URL to be scraped
base_url = 'https://dir.indiamart.com'
final_output = './out/'
# industry = final_output + 'Industrial Plants and Machineries/'

industries = pd.DataFrame({'Name':['Test industry'],'URL':['https://dir.indiamart.com/industry/packaging-material.html']})
print(industries)
print(industries.loc[:,'URL'])

def ExtractCategories(industries,categories):


    log_dir = './Logs/'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


    old_stdout = sys.stdout
    log_file = open(log_dir+"extractCategories.log","w")
    sys.stdout = log_file

    for i in range(len(industries.index)):
        row = industries.iloc[i]
        industry = row['URL']
        industry_name = row['Name']
        print(f"Fetching categories from {industry_name} ...")
        try:
            industry_page = urllib.request.urlopen(industry)
            industry_soup = BeautifulSoup(industry_page, 'html.parser')
            categories_box = industry_soup.find('div', attrs={'class': 'mid'})    	
        except Exception as e:
            print(f"!!!!!! Error fetching categories from {industry} : {e}")
            categories_box = None


        industry_path = final_output + industry_name
        
        if (categories_box):
            try:
                categories_sub_box = categories_box.find_all('ul')  # Due to Html implementation of base_url
            except Exception as e:
                print(f"!!!!! Error fetching categories_sub_box from {industry} : {e}")
                categories_sub_box = []

            for cat_sub_box in [categories_sub_box[0]]: # Testing
            # for cat_sub_box in categories_sub_box: # Production
                try:
                    cat_list = cat_sub_box.find_all('li')
                except Exception as e:
                    print(f"!!!! Error fetching cat_list from cat_sub_box : {e}")
                    cat_list = []
                for cat in [cat_list[0]]: # Testing
                #for cat in cat_list: # Production
                    try:
                        cat_tag = cat.find('a', href=True)
                        cat_name = cat_tag.getText().strip()
                        cat_url = cat_tag['href']
                        new_cat = pd.DataFrame({"Name":[cat_name], "URL":[cat_url],"Industry":[industry_name]})
                        print(f"Found category {cat_name} : appending ...")
                        categories = categories.append(new_cat, ignore_index=True)
                    except Exception as e:
                        print(f"Error fetching category url from cat_tag : SKIPPING : {e}")
    print(f"\nDONE : Found {len(categories.index)} categories\n")
    print(categories.iloc[:10,:])
    
    sys.stdout = old_stdout
    log_file.close()

    print(f"\nDONE : Found {len(categories.index)} categories\n")

    return categories



categories = pd.DataFrame(columns={'Name', 'URL','Industry'})
categories = ExtractCategories(industries,categories)

i=0
row = categories.iloc[i]
print(':::::::::: '+row+' :::::::::::::')
name = row['Name']
url = row['URL']
print(f":::::::::::: {name} ::::::::::")
print(f"~~~~~~~~~~~~ {url} :::::::::::")