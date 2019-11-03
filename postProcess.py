import sys
import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile



def PostProcess(data_dir='./out'):

    if(log_dir):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = open(log_dir + "postProcess.log", "a")
        old_stdout = sys.stdout
        sys.stdout = log_file

    print("Scanning files ...")


    agg_data_df = pd.DataFrame(columns=['Name', 'URL', 'Phone', 'Address', 'Category','Industry'])
    for root, dirs, files in os.walk(data_dir):
        for name in files:
            if name == re.compile("products"):
                file_name = os.path.join(root,name)
                subcat_df = pd.read_excel(file_name)
                agg_data_df = agg_data_df.append(subcat_df, ignore_index=True)

    agg_data_df.sort_values('Name',inplace=True)
    agg_data_df.drop_duplicates('URL',inplace=True)
    print(f"Found {len(agg_data_df.index)} distinct product URLs")

    writer = ExcelWriter(data_dir+'all_products.xlsx')
    d = {'Name':agg_data_df['Name'],
            'URL':agg_data_df['URL'],
            'Phone':agg_data_df['Phone'],
            'Address':agg_data_df['Address'],
            'Category':agg_data_df['Category'],
            'Industry':agg_data_df['Industry']}
    df = pd.DataFrame(d, columns=['Name','URL','Phone','Address', 'Category','Industry'])
    #print(agg_data_df.iloc[0:10,:])
    print(df.iloc[:10,:])
    df.to_excel(writer)
    writer.save()
    writer.close()

    # sample_writer = ExcelWriter(data_dir+'sampleSellers.xlsx')
    # sample_df = df.iloc[0:500,:]
    # sample_df.to_excel(sample_writer)
    # sample_writer.save()
    # sample_writer.close()

    if(log_dir):
        sys.stdout = old_stdout
        log_file.close()

    print(f"Found {len(agg_data_df.index)} distinct product URLs")
    print("PostProcess : DONE.")
    
    return 0