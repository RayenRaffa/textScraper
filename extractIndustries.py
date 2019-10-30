import sys
import re
import os
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup




def ExtractIndustries(base_url,out_dir='./out',log_dir=None):

	if (log_dir):
		if not os.path.exists(log_dir):
			os.makedirs(log_dir)
		old_stdout = sys.stdout
		log_file = open(os.path.abspath(log_dir)+"/extractIndustries.log","w")
		sys.stdout = log_file

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
				industries = industries.append({"Name":industry_name, "URL":industry_url}, ignore_index=True)
			except Exception as e:
				if(industry_url):
					print(f"Warning could not fetch industry name from {industry_url} : {e} : IMPOROV_MODE_ACTIVATED")
					industry_name = industry_url[1:].split('.')[0]
					industries = industries.append({"Name":industry_name, "URL":industry_url}, ignore_index=True)
				else:
					print(f"Error fetching industry URL : {e} : SKIPPING ...")

	try:
		if not os.path.exists(out_dir):
			os.makedirs(out_dir)
		writer = ExcelWriter(os.path.abspath(out_dir) + '/industries.xlsx') # TO DO : adapt script to write multiple sheets per file, one industry per file
		industries.to_excel(writer)
		writer.save()
		writer.close()
		print(f"\nSaved Industries data at {os.path.dirname(out_dir)}/industries.xlsx")
	except Exception as e:
		print(industries)
		print(f"{e} \nPlease remove {os.path.dirname(out_dir)} or provide another out_dir")

	if(log_dir):
		sys.stdout = old_stdout
		log_file.close()
	
	print(f"\nDONE : Collected {len(industries.index)} industries TOTAL !")
	

	return industries




# base_url = 'https://dir.indiamart.com'

# industries = ExtractIndustries(base_url)