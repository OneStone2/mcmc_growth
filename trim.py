# coding: utf-8

import pandas as pd
from pandas import DataFrame, read_csv
import numpy as np
import bisect

def clean(in_file, out_file='data/forest.csv'):
    data_points = pd.read_csv(in_file)
    #Split plots whenever a forest doubles its number of trees
    #or loses at least half
    #This step is a bit slow, it should be worked on
    prev_tpa = None
    prev_plot = None
    prev_seq = 0
    for i, row in data_points.iterrows():
        if prev_plot != int(row['py'] / 10000):
            prev_seq += 1
            prev_plot = int(row['py'] / 10000)
        else:
            if (prev_tpa * 2 < row['tpa']) or (prev_tpa / 2 > row['tpa']):
                prev_seq += 1
        data_points.loc[i, 'new'] = prev_seq
        prev_tpa = row['tpa']
    #Renumber the rows to make the spliiting effective
    data_points.index = (data_points.loc[:, 'py'] % 10000 + data_points.loc[:,'new'] * 10000).apply(int)
    #Remove entries with few trees
    MIN_TREES = 5
    data_points = data_points[data_points['samples'] >= MIN_TREES]
    #Drop samples, new and py.  They're not necessary anymore
    data_points = data_points.drop(['samples', 'new', 'py'], axis = 1)
    #Remove plots for which there is only a single measurement in time
    keep_rows = []
    prev_plot = None
    valid = False
    for py, row in data_points.iterrows():
        if (prev_plot is None) or (int(prev_plot / 10000) != int(py / 10000)):
            if valid:
                keep_rows.append(prev_plot)
            valid = False
        else:
            keep_rows.append(prev_plot)
            valid = True
        prev_plot = py
    data_points = data_points.loc[keep_rows]
    #Find which species are the most important
    #Keep top importance values that add up to MIN_IV
    MIN_IV = 0.5
    keep_cols = [col for col in list(data_points) if not col.startswith('iv')]
    col_iv = [col for col in list(data_points) if col.startswith('iv')]
    sorted_iv = data_points[col_iv].apply(sum, axis=0).sort_values(ascending=False)
    cutoff = bisect.bisect_left(np.cumsum(sorted_iv), len(data_points.index) * MIN_IV) +1
    #Add 1 to the cutoff so the total IV is guaranteed to be over MIN_IV
    for i in np.arange(cutoff):
        keep_cols.append(sorted_iv.index[i])  
    data_points = data_points.loc[:, keep_cols]
    #Add the index as a column
    data_points.reset_index(inplace=True)
    DATA_CLEAN_CSV = 'data/forest.csv'
    data_points.to_csv(DATA_CLEAN_CSV, index=False)



