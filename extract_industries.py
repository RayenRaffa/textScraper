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


def ExtractIndustries(base_url=base_url):

	industries = pd.DataFrame(columns=['Name','URL'])
	try:
    	industries_page = urllib.request.urlopen(base_url)
    	industry_soup = BeautifulSoup(industries_page, 'html.parser')
    	industries_loc = industry_soup.find('div', attrs={'class':'cat-pdt'})
    except Exception as e:
    	industries_loc = None
    	if (industry_soup):
    		print(f"Error locating industries box in {base_url} : {e} ")
    	else:
    		print(f"Error loading {base_url} : {e}")
    if (industries_loc):
    	industries_list = industries_loc.find_all('div')
    	print(f"Found {len(industries_list)} : Collecting URLs ...")
    	for in


    return industries

