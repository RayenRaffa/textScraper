import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

data_dir = './out/'
agg_data_df = pd.DataFrame(columns=['Name', 'URL', 'Phone', 'Address'])
for root, dirs, files in os.walk(data_dir):
        for name in files:
            file_name = os.path.join(root,name)
            print(f"Scanning file {file_name}")
            subcat_df = pd.read_excel(file_name)
            agg_data_df = agg_data_df.append(subcat_df, ignore_index=True)

agg_data_df.sort_values('Name',inplace=True)
agg_data_df.drop_duplicates('URL',inplace=True)
print(f"Found {len(agg_data_df.index)} distinct URLs")

writer = ExcelWriter(data_dir+'MachinesAndPlants.xlsx')
d = {'Name':agg_data_df.iloc[:,1],'URL':agg_data_df.iloc[:,3],'Phone':agg_data_df.iloc[:,2],'Address':agg_data_df.iloc[:,0]}
df = pd.DataFrame(d, columns=['Name','URL','Phone','Address'])
print(agg_data_df.iloc[0:10,:])
print(df.iloc[:10,:])
df.to_excel(writer)
writer.save()
writer.close()
