import sys
import re
import os
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup




def GetContactInfo(urls,out_dir='./out',log_dir=None):

	if (log_dir):
		if not os.path.exists(log_dir):
			os.makedirs(log_dir)
		old_stdout = sys.stdout
		log_file = open(os.path.abspath(log_dir)+"/extractIndustries.log","a")
		sys.stdout = log_file

	people = pd.DataFrame(columns=['URL','MAIL','MOBILE'])
	missing_people = pd.DataFrame(columns=['URL'])
	missing_contacts = pd.DataFrame(columns=['URL'])
	missing_emails = pd.DataFrame(columns=['URL'])
	missing_phones = pd.DataFrame(columns=['URL'])

	# Dictionary that the funciton will return
	all_data = {
		'people':people, 
		'missing_people':missing_people,
		'missing_contacts':missing_contacts,
		'missing_emails':missing_emails,
		'missing_phones':missing_phones
	}
		
	for base_url in urls['URL']:
		# print(f"Scanning : {base_url}")
		# base_url = url[1]
		# print(f"DEBUG: {base_url} ! YAY")
		try:
			person_page = urllib.request.urlopen(base_url)
			person_soup = BeautifulSoup(person_page, 'html.parser')
		except Exception as e:
			person_soup = None
			print(f"URL {base_url} NOT FOUND ! marking ..")
			missing_people = missing_people.append({'URL':base_url}, ignore_index=True)

		if(person_soup):
			try:
				contact_box = person_soup.find('div', attrs={'class':'contactBox'})
			except Exception as e:
				contact_box = None
				print(f"Error locating contact_box at {base_url} ! marking ...")
				missing_contacts = missing_contacts.append({'URL':base_url}, ignore_index=True)


		if (contact_box):
			try:
				email_box = contact_box.find('a', attrs={'class':'widgetContacts__item widgetContacts__item_publicemail'})
				email = email_box.getText()
			except Exception as e:
				missing_emails = missing_emails.append({'URL':base_url}, ignore_index=True)
				print(f"WARNING : Email missing at {base_url} ! marking ...")
				email = None


			try:
				phone_box = contact_box.find('a', attrs={'class':'widgetContacts__item widgetContacts__item_mobile'})
				phone = phone_box.getText()
			except Exception as e:
				missing_phones = missing_phones.append({'URL':base_url}, ignore_index=True)
				print(f"WARNING : Phone missing at {base_url} ! marking ...")
				phone = None

			if(email):
				people = people.append({
					'URL':base_url,
					'MAIL':email,
					'MOBILE':phone
					}, ignore_index=True)
				print(f"SUCCES : Added {base_url} !")
			elif (not email and not phone):
				missing_contacts = missing_contacts.append({'URL':base_url}, ignore_index=True)
				print(f"WARNING Error: Contact info missing at {base_url} ! marking ...")



	if not os.path.exists(out_dir):
		os.makedirs(out_dir)


	people.sort_values('URL',inplace=True)
	people.drop_duplicates('URL', inplace=True)
	file_path = out_dir+'/people.csv'
	people.to_csv(file_path, index=None, header=True,sep='|')
	print(f"Found {len(people.index)} : Saved data at {file_path}.")

	missing_people.sort_values('URL',inplace=True)
	missing_people.drop_duplicates('URL', inplace=True)
	file_path = out_dir+'/missing_people.csv'
	missing_people.to_csv(file_path, index=None, header=True,sep='|')
	print(f"Found {len(missing_people.index)} missing_people : Saved data at {file_path}.")

	missing_contacts.sort_values('URL',inplace=True)
	missing_contacts.drop_duplicates('URL', inplace=True)
	file_path = out_dir+'/missing_contacts.csv'
	missing_contacts.to_csv(file_path, index=None, header=True,sep='|')
	print(f"Found {len(missing_contacts.index)} missing_contacts : Saved data at {file_path}.")

	missing_emails.sort_values('URL',inplace=True)
	missing_emails.drop_duplicates('URL', inplace=True)
	file_path = out_dir+'/missing_emails.csv'
	missing_emails.to_csv(file_path, index=None, header=True,sep='|')
	print(f"Found {len(missing_emails.index)} missing_emails : Saved data at {file_path}.")

	missing_phones.sort_values('URL',inplace=True)
	missing_phones.drop_duplicates('URL', inplace=True)
	file_path = out_dir+'/missing_phones.csv'
	missing_phones.to_csv(file_path, index=None, header=True,sep='|')
	print(f"Found {len(missing_phones.index)} missing_phones : Saved data at {file_path}.")
	

	if(log_dir):
		sys.stdout = old_stdout
		log_file.close()
	
	print(f"\nDONE !!")
	

	return all_data



urls = pd.read_csv('./out/urls.csv',sep='|')
print(f"Loaded {len(urls.index)} URLs from urls.csv")
urls.sort_values('URL',inplace=True)
urls.drop_duplicates('URL', inplace=True)
print(f"Found {len(urls.index)} distinct URLs in urls.csv")

# print(urls)
GetContactInfo(urls)