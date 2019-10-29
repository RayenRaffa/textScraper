import re
import os
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup
from extract_products import ExtractProducts
from extract_categories import ExtractCategories
from extract_industries import ExtractIndustries
# URL to be scraped
base_url = 'https://dir.indiamart.com'
final_output = './out/'
# industry = final_output + 'Industrial Plants and Machineries/'


def scrape(base_url=base_url):

    industries = ExtractIndustries(base_url)
    categories = ExtractCategories(industries)
    print(f"Found {len(categories.index)} categories TOTAL !")
    print(categories.iloc[:10,:])

    return categories



scrape()