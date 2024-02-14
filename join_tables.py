#!/usr/bin/env python3
# ejr: 2024-01-29
# 2021-01-29: 0.1.0: initial version
# read in an indeterminate number of tables from the command line and combine them into a single table joining on the first column

import pandas as pd
import os
import sys

def main():

    # list to hold the dataframes
    dfs = []

    # iterate over the command line arguments and read in the tables
    for filename in sys.argv[1:]:
        print(filename)
        # check that the file exists
        if not os.path.exists(filename):
            print(f'File {filename} does not exist')
            exit(1)
        # read in the table
        df = read_table(filename)
        # append to the list
        dfs.append(df)

    # join list of dataframes on the first column
        merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on='id', how='inner')

    # write out a single table
    merged_df.to_csv('combined_table.tsv', sep='\t', index=False)

    exit(1)

def read_table(filename):
    """Read in a table and return a dataframe"""
    df = pd.read_csv(filename, sep='\t', header=0)

    # rename first column to "id"
    df = df.rename(columns={df.columns[0]: "id"})

    #rename second column to filename
    df = df.rename(columns={df.columns[1]: filename})

    return df

if __name__ == '__main__':
    main()