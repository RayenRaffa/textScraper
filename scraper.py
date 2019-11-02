import sys
import re
import os
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup
from extractVendors import ExtractVendors
from extractProducts import ExtractProducts
from extractCategories import ExtractCategories
from extractIndustries import ExtractIndustries
from postProcess import PostProcess



base_url = 'https://dir.indiamart.com'

def scrape(base_url,out_dir='./out',log_dir=None):

    industries = ExtractIndustries(base_url)
    for industry in industries.itertuples():
            categories = ExtractCategories(base_url, industry)
            break
    for category in categories.itertuples():
            products   = ExtractProducts(base_url, category)
            break
    for product in products.itertuples():
            vendors    = ExtractVendors(base_url, product)
            break # Testing : run the loop once only


    return 0



scrape(base_url)


# categories = pd.DataFrame(columns={'Name', 'URL','Industry'})
# industries = pd.DataFrame(columns={'Name', 'URL'})
# sellers = pd.DataFrame(columns=['Name', 'URL', 'Phone', 'Address','Category','Industry'])
# sellers, categories, industries =  scrape(sellers, categories, industries)
# PostProcess()