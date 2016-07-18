# coding: utf-8
from pandas import DataFrame, read_csv
from collections import defaultdict
import pandas as pd
import numpy as np
import math

def area(row):
    """
    Find the DIA parameter of a tree and calculate area
    """
    if np.isnan(row['DIA']):
            dia = row['PREVDIA'] if np.isnan(row['DIACALC']) else row['DIACALC']
    else:
        dia = row['DIA']
    return math.pi * ((dia / 2) ** 2) * row['TPA_UNADJ']

class Plot(object):
    """
    Contains all the subplots/trees measured for a particular year on a particular plot.
    Internally contains a dataframe of all the trees and their subplots.
    Has methods to computer total BA/TPA and species importance values
    """
    def __init__(self, df, py):
        self.df = df
        self.py = py
        self.tpa = None
        self.ba = None
    
    def calc_tpa(self):
        """
        Calculate the TPA for the plot.
        """
        if self.tpa != None:
            return self.tpa
        total = 0.0
        for i, row in self.df.iterrows():
            total += row['TPA_UNADJ']
        self.tpa = total
        return self.tpa
    
    def calc_ba(self):
        """
        Calculates the total basal area for the plot.
        """
        if self.ba != None:
            return self.ba
        total = 0.0
        for i, row in self.df.iterrows():
            total += area(row)
        self.ba = total
        return self.ba
    
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
        param_dd = defaultdict(lambda: [0,0,set()])
        for i, row in self.df.iterrows():
            param_dd[row['SPCD']][0] += row['TPA_UNADJ']
            param_dd[row['SPCD']][1] += area(row)
            param_dd[row['SPCD']][2].add(row['SUBP'])
        total_subp = set()
        for spp in param_dd:
            total_subp = total_subp.union(param_dd[spp][2])
        sum_freq = 0.0
        for spp in param_dd:
            param_dd[spp][2] = len(param_dd[spp][2])/float(len(total_subp))
            sum_freq += param_dd[spp][2]
        for spp in param_dd:
            param_dd[spp][0] /= self.calc_tpa()
            param_dd[spp][1] /= self.calc_ba()
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
            'tpa': self.calc_tpa(),
            'ba': self.calc_ba(),
            'samples': len(self.df.index) 
        }
        stats.update(self.calc_iv())
        return stats

def parse(fia_filename):
    """
    Takes the raw FIA file and returns a bunch of Plot objects
    """
    FIA_COLS = [
        'CN','PREV_TRE_CN','INVYR','PLOT','SUBP',
        'SPCD','DIA','DIACALC','PREVDIA','TPA_UNADJ'
    ]

    trees_df = pd.read_csv(fia_filename, usecols=FIA_COLS)
    
    trees_df.set_index('CN', drop=True, inplace=True)
    for i, row in trees_df.iterrows():
        if (np.isnan(row['TPA_UNADJ'])): 
            trees_df.set_value(i, 'TPA_UNADJ', trees_df.loc[row['PREV_TRE_CN'], 'TPA_UNADJ'])
    trees_df.reset_index(level=0, inplace=True)
    
    grouped = trees_df.groupby(['PLOT', 'INVYR'])
    for name, group in grouped:
        yield Plot(group, name[0] * 10000 + name[1])
            
def cluster_prep_file(plots, out_filename):
    """
    Given a list of Plot objects, write them to a named CSV
    """
    df = pd.DataFrame([p.plot_stats() for p in plots])
    df = df.fillna(0)
    df.to_csv(out_filename, index=False)
    return out_filename

