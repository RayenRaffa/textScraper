import sys
import re
import os
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup
from extractProducts import ExtractProducts
from extractCategories import ExtractCategories
from extractIndustries import ExtractIndustries
from postProcess import PostProcess
# URL to be scraped
base_url = 'https://dir.indiamart.com'
final_output = './out/'
# industry = final_output + 'Industrial Plants and Machineries/'


def scrape(sellers, categories, indusries, base_url=base_url):

    industries = ExtractIndustries(base_url)
    categories = ExtractCategories(industries,categories)
    sellers = ExtractProducts(sellers,categories,base_url)
    print(f"\nFound {len(categories.index)} categories TOTAL !")
    print(categories.iloc[:10,:])
    print(f"\nFound {len(sellers.index)} sellers TOTAL !")

    return sellers, categories, industries


categories = pd.DataFrame(columns={'Name', 'URL','Industry'})
industries = pd.DataFrame(columns={'Name', 'URL'})
sellers = pd.DataFrame(columns=['Name', 'URL', 'Phone', 'Address','Category','Industry'])
sellers, categories, industries =  scrape(sellers, categories, industries)
PostProcess()