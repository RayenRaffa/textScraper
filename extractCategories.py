import sys
import re
import os
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup
from extractIndustries import ExtractIndustries


def ExtractCategories(base_url,industry,out_dir='./out',log_dir=None):


    if(log_dir):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        old_stdout = sys.stdout
        log_file = open(log_dir+"extractCategories.log","w")
        sys.stdout = log_file

    categories = pd.DataFrame(columns=["Name","URL","Industry"])


    industry_name = industry[1]
    industry_url = industry[2] # industry is a tuple : [Index, Name, URL]
    print(f"Fetching categories from {industry_name} ...")
    try:
        industry_page = urllib.request.urlopen(industry_url)
        industry_soup = BeautifulSoup(industry_page, 'html.parser')
        categories_box = industry_soup.find('div', attrs={'class': 'mid'})    	
    except Exception as e:
        print(f"!!!!!! Error fetching categories from {industry_url} : {e}")
        categories_box = None



    
    if (categories_box):
        try:
            categories_sub_box = categories_box.find_all('ul')  # Due to Html implementation of base_url
        except Exception as e:
            print(f"!!!!! Error fetching categories_sub_box from {industry_url}\n{e} ... SKIPPING")
            categories_sub_box = []

        #for cat_sub_box in [categories_sub_box[0]]: # Testing
        for cat_sub_box in categories_sub_box: # Production
            try:
                cat_list = cat_sub_box.find_all('li')
            except Exception as e:
                print(f"!!!! Error fetching cat_list from cat_sub_box\n{e} ... SKIPPING")
                cat_list = []
            #for cat in [cat_list[0]]: # Testing
            for cat in cat_list: # Production
                try:
                    cat_tag = cat.find('a', href=True)
                    cat_name = cat_tag.getText().strip()
                    cat_url = cat_tag['href']
                    print(f"Found category {cat_name} : appending ...")
                    categories = categories.append({"Name":cat_name, "URL":cat_url,"Industry":industry_name}, ignore_index=True)
                except Exception as e:
                    print(f"Error fetching category url from cat_tag : SKIPPING : {e}")
    print(f"\nDONE : Collected {len(categories.index)} categories from {industry_name}\n")
    print(categories.iloc[:10,:])
    


    industry_dir = os.path.abspath(out_dir)+'/'+industry_name
    try:
        if not os.path.exists(industry_dir):
            os.makedirs(industry_dir)
        writer = ExcelWriter(os.path.abspath(industry_dir) + '/categories.xlsx') # TO DO : adapt script to write multiple sheets per file, one industry per file
        categories.to_excel(writer, index=False)
        writer.save()
        writer.close()
        print(f"\nSaved Categories of {industry_name} data at {os.path.dirname(industry_dir).split('/')[-1]}/{industry_name}/categories.xlsx")
    except Exception as e:
        print(categories)
        print(f"{e} \nPlease remove {os.path.dirname(out_dir)} or provide another out_dir")


    if(log_dir):
        sys.stdout = old_stdout
        log_file.close()


    return categories



out_dir = './out'
base_url = 'https://dir.indiamart.com'
industries = ExtractIndustries(base_url)
g_categories = pd.DataFrame(columns=["Name","URL","Industry"])
for industry in industries.itertuples():
    # print(industry)
    categories = ExtractCategories(base_url,industry,out_dir)
    g_categories = g_categories.append(categories, ignore_index=True)
    print(f"Collected {len(g_categories.index)} so far ...")

# Creating recap file for all categories
print(f"Collected {len(g_categories.index)} categories TOTAL !")
g_categories.sort_values('Name',inplace=True)
g_categories.drop_duplicates('URL',inplace=True)
g_categories_final = g_categories[['Name','URL','Industry']]
print(f"Found {len(g_categories_final.index)} distinct categories")
try:
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    writer = ExcelWriter(os.path.abspath(out_dir) + '/categories_all.xlsx') # TO DO : adapt script to write multiple sheets per file, one industry per file
    g_categories_final.to_excel(writer, index=False)
    writer.save()
    writer.close()
    print(f"\nSaved ALL Categories data at {out_dir}/categories_all.xlsx")
except Exception as e:
    print(f"{e} \nPlease remove {out_dir} or provide another out_dir")