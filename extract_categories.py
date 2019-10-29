import re
import os
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup
from extract_products import ExtractProducts

# URL to be scraped
base_url = 'https://dir.indiamart.com'
final_output = './out/'
# industry = final_output + 'Industrial Plants and Machineries/'

industries = pd.DataFrame({'Name':['Test industry'],'URL':['/industry/packaging-material.html']})
print(industries)

print(industries.loc[:,'URL'])

def ExtractCategories(industries,categories=None):
    categories = pd.DataFrame(columns={'Name', 'URL'})    
    for industry in industries.loc[:,'URL']:
	    
	    try:
	    	print(industry)
	    	industry_page = urllib.request.urlopen(base_url + industry)
	    	industry_soup = BeautifulSoup(industry_page, 'html.parser')
	    	categories_box = industry_soup.find('div', attrs={'class': 'mid'})    	
	    except Exception as e:
    		print(f"!!!!!! Error fetching categories from {industry} : {e}")
    		categories_box = None
	    

	    try:
	    	industry_name = categories_box.find('h1').getText().strip()
	    	print(industry_name)
	    except Exception as e:
	    	print(f"Warning : Could not get Category name")
	    	industry_name = industry[1:].split('.')[0]

	    industry_path = final_output + industry_name

	    if not os.path.exists(industry_path):
	    	print(f"Creating directory for : {industry_name} ...")
    		os.makedirs(industry_path)

	    if (categories_box):
	    	try:
	    		categories_sub_box = categories_box.find_all('ul')  # Due to Html implementation of base_url
	    	except Exception as e:
	    		print(f"!!!!! Error fetching categories_sub_box from {industry} : {e}")
	    		categories_sub_box = None

    		for cat_sub_box in categories_sub_box:
    			try:
    				cat_list = cat_sub_box.find_all('li')
    			except Exception as e:
    				print(f"!!!! Error fetching cat_list from cat_sub_box : {e}")
    				cat_list = None
    			for cat in cat_list:
    				try:
    					cat_tag = cat.find('a', href=True)
    					cat_name = cat_tag.getText().strip()
    					cat_url = cat_tag['href']
    					print(f"Found {cat_name} at {cat_url} : Adding ..")
    					new_cat = pd.DataFrame({"Name":[cat_name], "URL":[cat_url]})
    					print(new_cat)
    					categories = categories.append(new_cat, ignore_index=True)
    				except Exception as e:
    					print(f"Error fetching category url from cat_tag : SKIPPING : {e}")
    print(f"Found {len(categories.index)} categories")
    print(categories.iloc[:10,:])

    return categories


categories = pd.DataFrame(columns={'Name', 'URL'})
categories = ExtractCategories(industries,categories)
