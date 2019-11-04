import sys
import os
import re
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


def PostProcess(data_dir='./out', log_dir=None):

    if(log_dir):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = open(log_dir + "postProcess.log", "a")
        old_stdout = sys.stdout
        sys.stdout = log_file

    print("Scanning files ...")

    agg_data_df = pd.DataFrame(
    columns=[
        'Name',
        'URL',
        'Phone',
        'Address',
        'Category',
         'Industry'])
    for root, dirs, files in os.walk(data_dir):
        for name in files:
            file_nature = name.split('_')[0]
            if file_nature == "vendorsOf":
                file_name = os.path.join(root, name)
                print(f"Adding : {name} ..")
                file_df = pd.read_excel(file_name)
                agg_data_df = agg_data_df.append(file_df, ignore_index=True, sort=False)

    agg_data_df.sort_values('Name', inplace=True)
    agg_data_df.drop_duplicates('URL', inplace=True)
    print(f"Found {len(agg_data_df.index)} distinct product URLs")

    writer = ExcelWriter(data_dir + '/all_vendors.xlsx')
    d = {'Name': agg_data_df['Name'],
            'URL': agg_data_df['URL'],
            'Phone': agg_data_df['Phone'],
            'Address': agg_data_df['Address'],
            'Category': agg_data_df['Category'],
            'Industry': agg_data_df['Industry']}
    del agg_data_df
    all_vendors_df = pd.DataFrame(d,
    columns=[
        'Name',
        'URL',
        'Phone',
        'Address',
        'Category',
         'Industry'])
    
    del d

    try:
        all_vendors_df.to_excel(writer, index=False, encoding='UTF-8')
        writer.save()
        writer.close()
        print(
            f"Found {len(all_vendors_df.index)} distinct vendors !\nRecap file saved as XLSX at {out_dir}/all_vendors.xlsx")
    except Exception as e:
        print(f"Error saving recap file as XLSX")
        writer.close()

    all_vendors_df.to_csv(
        './out/all_vendors.csv',
        index=False,
        sep='|',
         encoding='UTF-8')
    print(f"Recap file saved as CSV at ./out/all_vendors.csv")

    sample_writer = ExcelWriter(data_dir+'sample_vendors.xlsx')
    sample_vendors_df = all_vendors_df.iloc[0:500,:]
    try:
        samplevendors_df.to_excel(sample_writer, index=False, encoding='UTF-8')
        sample_writer.save()
        sample_writer.close()
        print(
            f"Sample file saved as XLSX at {out_dir}/sample_vendors.xlsx")
    except Exception as e:
        print(f"Error saving sample file as XLSX")
        sample_writer.close()

    sample_vendors_df.to_csv(
        './out/sample_vendors.csv',
        index=False,
        sep='|',
         encoding='UTF-8')
    print(f"Sample file saved as CSV at ./out/sample_vendors.csv\nDONE")

    if(log_dir):
        sys.stdout = old_stdout
        log_file.close()

    print(f"Found {len(all_vendors_df.index)} distinct vendor URLs")
    print("PostProcess : DONE.")

    return 0

PostProcess()
