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
		industries_list = industries_loc.find_all('div',attrs={'class':re.compile('catBx')})
		print(f"Found {len(industries_list)} : Collecting URLs ...")
		for industry in industries_list:
			try:
				industy_link = industry.find('a',href=True)
				industry_url = 'https:' + industy_link['href']
				industry_name = industry.find('div',attrs={'class':'catHd'}).getText().strip()
			except Exception as e:
				if(industry_url):
					print(f"Error fetching industry name from {industry_url} : {e}")
					industry_name = industry_url[1:].split('.')[0]
				else:
					print(f"Error fetching industry URL : {e} : SKIPPING ...")
					industry_url = None
			if(industry_url):
				new_indus = pd.DataFrame({"Name":[industry_name], "URL":[industry_url]})
				print(new_indus)
				industries = industries.append(new_indus, ignore_index=True)

	return industries

industries = ExtractIndustries()
print(f"\nDONE : Found {len(industries.index)} industries")
print(industries.iloc[:10,:])