"""
Contains utilities to read and clean FIA files
"""
from pandas import DataFrame, read_csv
import pandas as pd
from collections import defaultdict
import numpy as np
import math
import bisect
import urllib2
import os

def check(row):
    """
    Checks for human intervention in a plot
    """
    if row['DSTRBCD1'] == 80.0:
        return True
    if row['DSTRBCD2'] == 80.0:
        return True
    if row['DSTRBCD3'] == 80.0:
        return True
    if row['TRTCD1'] == 10.0:
        return True
    if row['TRTCD1'] == 30.0:
        return True
    if row['TRTCD1'] == 50.0:
        return True
    if row['TRTCD2'] == 10.0:
        return True
    if row['TRTCD2'] == 30.0:
        return True
    if row['TRTCD2'] == 50.0:
        return True
    if row['TRTCD3'] == 10.0:
        return True
    if row['TRTCD3'] == 30.0:
        return True
    if row['TRTCD3'] == 50.0:
        return True
    return False

def check_n(row):
    """
    Checks for negative human intervention in a plot
    """
    if row['DSTRBCD1'] == 80.0:
        return 1
    if row['DSTRBCD2'] == 80.0:
        return 1
    if row['DSTRBCD3'] == 80.0:
        return 1
    if row['TRTCD1'] == 10.0:
        return 1
    if row['TRTCD2'] == 10.0:
        return 1
    if row['TRTCD3'] == 10.0:
        return 1
    return 0

def check_p(row):
    """
    Checks for positive human intervention in a plot
    """
    if row['TRTCD1'] == 30.0:
        return 1
    if row['TRTCD1'] == 50.0:
        return 1
    if row['TRTCD2'] == 30.0:
        return 1
    if row['TRTCD2'] == 50.0:
        return 1
    if row['TRTCD3'] == 30.0:
        return 1
    if row['TRTCD3'] == 50.0:
        return 1
    return 0

class Plot(object):
    """
    Contains all the subplots/trees measured for a particular plot.
    Internally contains a dataframe of all the trees and their subplots.
    Has methods to computer total BA/TPA and species importance values
    """
    def __init__(self, trees, plot, dstrb, py):
        self.df = trees
        self.py = py
        self.na = self.df.TPA_UNADJ.isnull().sum()
        self.df.fillna(0)
        self.tpa = self.df['TPA_UNADJ'].sum()
        self.ba = ((math.pi * (self.df['DIA']/2) ** 2) * self.df['TPA_UNADJ']).sum()
        self.carb = ((self.df['CARBON_AG'] + self.df['CARBON_BG']) * self.df['TPA_UNADJ']).sum()
        self.lon = plot.loc['LON']
        self.lat = plot['LAT']
        self.human_n = check_n(dstrb)
        self.human_p = check_p(dstrb)

    def calc_iv(self):
        """
        Calculates all importance values for species in this plot.
        Returns:
        {
            <spp1>: <impval1>,
            ...
        }
        """

        #Element 0 is TPA
        #Element 1 is BA
        #Element 2 is subplots
        param_dd = defaultdict(lambda: [0, 0, set()])
        grouped = self.df.groupby('SPCD')
        for name, group in grouped:
            param_dd[name][0] = group['TPA_UNADJ'].sum()
            param_dd[name][1] = ((math.pi * (group['DIA'] / 2) ** 2) * group['TPA_UNADJ']).sum()
            param_dd[name][2].update(group['SUBP'])
        total_subp = set()
        total_subp.update(self.df['SUBP'])
        sum_freq = 0.0
        for spp in param_dd:
            param_dd[spp][2] = len(param_dd[spp][2])/float(len(total_subp))
            sum_freq += param_dd[spp][2]
        for spp in param_dd:
            param_dd[spp][0] /= self.tpa
            param_dd[spp][1] /= self.ba
            param_dd[spp][2] /= sum_freq
        iv_dd = dict()
        for spp in param_dd:
            iv_dd['iv'+str(spp)] = sum(param_dd[spp][x] for x in np.arange(3)) / 3.0
        return iv_dd

    def plot_stats(self):
        """
        Returns a dictionary of all the plot stats.
        Can be used as a row in the dataframe used for clustering
        """
        stats = {
            'py': self.py,
            'carb': self.carb,
            'samples': len(self.df.index),
            'na': self.na,
            'lon': self.lon,
            'lat': self.lat,
            'human_p': self.human_p,
            'human_n': self.human_n
        }
        stats.update(self.calc_iv())
        return stats

def parse(state, online=True):
    """
    Takes the raw FIA file and returns a bunch of Plot objects
    """
    TREES_COLS = [
        'INVYR', 'PLOT', 'STATUSCD', 'CARBON_AG', 'CARBON_BG',
        'TPA_UNADJ', 'DIA', 'PREVDIA', 'DIACALC', 'SPCD', 'SUBP'
    ]
    PLOT_COLS = ['INVYR', 'PLOT', 'LAT', 'LON']
    DSTRB_COLS = [
        'PLOT', 'INVYR', 'DSTRBCD1', 'DSTRBCD2', 'DSTRBCD3',
        'TRTCD1', 'TRTCD2', 'TRTCD3'
    ]
    if online:
        TREES_WEB = "http://apps.fs.fed.us/fiadb-downloads/CSV/"+state+"_TREE.csv"
        PLOT_WEB = "http://apps.fs.fed.us/fiadb-downloads/CSV/"+state+"_PLOT.csv"
        DSTRB_WEB = "http://apps.fs.fed.us/fiadb-downloads/CSV/"+state+"_COND.csv"
        response = urllib2.urlopen(TREES_WEB)
        csv = response.read()
        f = open('temp', 'w')
        f.write(csv)
        f.close()
        trees_df = pd.read_csv('temp', usecols=TREES_COLS)
        response = urllib2.urlopen(PLOT_WEB)
        csv = response.read()
        f = open('temp', 'w')
        f.write(csv)
        f.close()
        plot_df = pd.read_csv('temp', usecols=PLOT_COLS)
        response = urllib2.urlopen(DSTRB_WEB)
        csv = response.read()
        f = open('temp', 'w')
        f.write(csv)
        f.close()
        dstrb_df = pd.read_csv('temp', usecols=DSTRB_COLS)
        os.remove('temp')
    else:
        TREES_FILE = 'data/'+state+'_TREE.csv'
        PLOT_FILE = 'data/'+state+'_PLOT.csv'
        DSTRB_FILE = 'data/'+state+'_COND.csv'
        trees_df = pd.read_csv(TREES_FILE, usecols=TREES_COLS)
        plot_df = pd.read_csv(PLOT_FILE, usecols=PLOT_COLS)
        dstrb_df = pd.read_csv(DSTRB_FILE, usecols=DSTRB_COLS)

    trees_df = trees_df[trees_df.STATUSCD == 1]
    trees_df.DIA.fillna(trees_df.DIACALC, inplace=True)
    trees_df.drop('DIACALC', axis=1, inplace=True)
    trees_df.DIA.fillna(trees_df.PREVDIA, inplace=True)
    trees_df.drop('PREVDIA', axis=1, inplace=True)

    grouped = trees_df.groupby(['PLOT', 'INVYR'])
    for name, group in grouped:
        yield Plot(
            group,
            plot_df[(plot_df.INVYR == name[1]) & (plot_df.PLOT == name[0])].iloc[0],
            dstrb_df[(dstrb_df.INVYR == name[1]) & (dstrb_df.PLOT == name[0])].iloc[0],
            name[0] * 10000 + name[1]
        )

def cluster_prep_file(plots, state):
    """
    Given a list of Plot objects, write them to a named CSV
    """
    out_filename = 'data/'+state+'_1.csv'
    df = pd.DataFrame([p.plot_stats() for p in plots])
    df = df.fillna(0)
    df.to_csv(out_filename, index=False)
    return out_filename

def clean(state, b):
    """
    Cleans the data for usage in the analysis.
    """
    in_file = 'data/'+state+'_1.csv'
    out_file = 'data/'+state+'_2a.csv'
    data_points = pd.read_csv(in_file)

    #Remove entries before the year 1999
    MIN_YR = 1999
    data_points = data_points[data_points['py'] % 10000 >= MIN_YR]
    #Remove entries with few trees
    MIN_TREES = 5
    data_points = data_points[data_points['samples'] - data_points['na'] >= MIN_TREES]
    #Remove entries with too many invalid trees
    NA_THRESHOLD = 5
    data_points = data_points[data_points['na'] < NA_THRESHOLD]
    #Keep only most importaqnt species
    MIN_IV = 0.7
    keep_cols = [col for col in list(data_points) if not col.startswith('iv')]
    col_iv = [col for col in list(data_points) if col.startswith('iv')]
    sorted_iv = data_points[col_iv].apply(sum, axis=0).sort_values(ascending=False)
    cutoff = bisect.bisect_left(np.cumsum(sorted_iv), len(data_points.index) * MIN_IV) +1
    #Add 1 to the cutoff so the total IV is guaranteed to be over MIN_IV
    for i in np.arange(cutoff):
        keep_cols.append(sorted_iv.index[i])
    data_points = data_points.loc[:, keep_cols]
    #Drop samples and na.  They're not necessary anymore
    data_points = data_points.drop(['samples', 'na'], axis=1)
    data_points.to_csv(out_file, index=False)

    if b:
        out_file = 'data/'+state+'_2b.csv'
        #Re-number the plots so that human interventions are not applied
        cur_np = 1
        prev_id = data_points.loc[data_points.index[0], 'py'] // 10000
        for i, row in data_points.iterrows():
            if (prev_id != row['py'] // 10000) or (row['human_n'] == 1) or (row['human_p'] == 1):
                cur_np += 1
            prev_id = row['py'] // 10000
            data_points.loc[i, 'py'] = int(cur_np * 10000 + row['py'] % 10000)
        data_points.to_csv(out_file, index=False)
