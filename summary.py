import pandas as pd
import numpy as np
import sys

from os import listdir
from os.path import isfile, join, splitext
from tabulate import tabulate

def print_summary(file):
    df = pd.read_excel(file)
    df['Stream'].dropna()

    # Get month and year based on file name
    file_name = splitext(file)[0]
    date, month = file_name.split('-')
    year = date[-6:][:4]
    
    # Print summary table
    print("Summary as of", month, year)
    summary = get_summary(df)
    summary_columns = ['Retailer', 'Streams', 'Earnings(USD)']
    print(tabulate(summary, headers=summary_columns), '\n')

    # Print top country table
    print('Top Countries for', month, year)
    top_country = get_top_country(df)
    print(tabulate(top_country, showindex=False, headers=df.columns), '\n\n\n')

def get_summary(df):
    # Group by Retailer and calculate total stream and earnings
    retailer = df.groupby('Retailer').agg(Streams=('Stream','sum'), Earnings=('Earnings($)', 'sum'))
    # Add Total row at the end
    total = retailer.sum()
    total.name = "Total"
    retailer = retailer.append(total.transpose())
    # Format output
    retailer.Earnings = retailer.Earnings.round(2)
    retailer.Streams = retailer.Streams.apply(lambda x : "{:,}".format(int(x)))
    return retailer

def get_top_country(df):
    # Get rows with top streams based on retailer
    top_country = df.loc[df.groupby('Retailer')['Stream'].idxmax()]
    # Insert columns for printing into new dataframe
    df = pd.DataFrame({'Retailer':top_country['Retailer'], 'Country':top_country['Customer Territory'],
                        'Streams': top_country['Stream'].apply(lambda x : "{:,}".format(int(x)))})
    return df


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1:
        path = "dataset"
        files = [join(path, f) for f in listdir(path)]
        for file in sorted(files):
            print_summary(file)
    else:
        for i in range(1, argc):
            print_summary(sys.argv[i])