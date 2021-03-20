import pandas as pd
import numpy as np

from os import listdir
from os.path import isfile, join, splitext
from tabulate import tabulate

def get_summary(file):
    df = pd.read_excel(file)
    df['Stream'].dropna()
    # Get header name
    file_name = splitext(file)[0]
    date, month = file_name.split('-')
    year = date[-6:][:4]
    
    print("Summary as of", month, year)

    # Group by Retailer and calculate total stream and earnings
    retailer = df.groupby('Retailer').agg(Streams=('Stream','sum'), Earnings=('Earnings($)', 'sum'))
    # Add Total row at the end
    total = retailer.sum()
    total.name = "Total"
    retailer = retailer.append(total.transpose())
    # Format output
    retailer.Earnings = retailer.Earnings.round(2)
    retailer.Streams = retailer.Streams.apply(lambda x : "{:,}".format(int(x)))
    print(tabulate(retailer, headers=['Retailer', 'Streams', 'Earnings(USD)']), '\n')

    # Top Countries
    top_country = df.loc[df.groupby('Retailer')['Stream'].idxmax()]
    df = pd.DataFrame({'Retailer':top_country['Retailer'], 'Country':top_country['Customer Territory'], 'Streams': top_country['Stream'].apply(lambda x : "{:,}".format(int(x)))})
    print('Top Countries for', month, year)
    print(tabulate(df, showindex=False, headers=df.columns), '\n\n\n')

if __name__ == "__main__":
    path = "dataset"
    files = [join(path, f) for f in listdir(path)]
    for file in files:
        get_summary(file)