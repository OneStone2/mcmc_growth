import random
from collections import defaultdict
from scipy import stats, linalg
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
from pandas import DataFrame, read_csv
import numpy as np

def cluster(in_file, n_clusters=2, norm=None):
    data_points = pd.read_csv(in_file, index_col='index')
    if norm == 'z_score':
        #Apply Z-score normalization
        for column in data_points:
            data_points[column] = stats.zscore(data_points[column], axis=None)
    else:
        if norm == 'interval':
            #Apply interval normalization
            for column in data_points:
                data_points[column] = (
                    data_points[column] - min(data_points[column])
                ) / (
                    max(data_points[column]) - min(data_points[column])
                )
    #Apply PCA
    pca = PCA(n_components='mle')
    data_pca = pca.fit_transform(data_points)
    #Create the clusters based on the PCA axes
    clusters = KMeans(n_clusters=n_clusters).fit(data_pca)
    centroids = clusters.cluster_centers_
    labels = clusters.labels_
    data_points['cluster'] = labels
    return data_points

def test(observed, expected, freq_e):
    """
    Take the observed and expected Markov state transition models and checks how different they are.
    Inputs must be square matrices with the frequencies.
    Use the chi-square test.
    Ignore expected values of less than 1.
    Success if returns greater than 0.05.
    """
    MIN_SIG = 1
    exp_arr = []
    obs_arr = []
    for i, row in expected.iterrows():
        for j, elem in enumerate(row):
            if elem * freq_e[i] >= MIN_SIG:
                exp_arr.append(expected.loc[i][j])
                obs_arr.append(observed.loc[i][j])
    return stats.chisquare(obs_arr, exp_arr, axis=None, ddof = len(observed.columns) - 1)[1]

def construct_groups(data_points, n_clusters=2):
    """
    Shuffles all the list of state transitions in 11 different groups.
    Returns a list of 11 dataframes with the sum of the transitions recorded.
    """
    REQ_TRANS = 5
    N_GROUPS = 10
    #Store all the changes of state as 3-tuples
    #First element: difference in years
    #Second element: initial state
    #Third element: final state
    #Discard all elements whose difference is not exactly 5 years
    state_changes = []
    prev_id = None
    prev_state = None
    for cur_id, row in data_points.iterrows():
        if (prev_id != None) and (prev_id / 10000 == cur_id / 10000):
            if cur_id - prev_id == REQ_TRANS:
                new_state_change = (cur_id - prev_id, prev_state, row['cluster'])
                state_changes.append(new_state_change)
        prev_id = cur_id
        prev_state = row['cluster']
    #Sort the list of changes of state randomly
    #From the ordering, draw 10+1 groups and create a matrix for each group
    random.shuffle(state_changes)
    group_year = []
    j = 0
    for i in np.arange(N_GROUPS + 1):
        year_state = pd.DataFrame(0, index=np.arange(n_clusters), columns=np.arange(n_clusters))
        next_cutoff = (i + 1) * len(state_changes) / (N_GROUPS + 1)
        while j < next_cutoff:
            cur_change = state_changes[j]
            year_state.loc[cur_change[1],cur_change[2]] += 1
            j += 1
        group_year.append(year_state)
    return group_year

def construct_msm(group_year):
    """
    Do bootstrapping removing one of the groups every time.
    Then, perform chi-square test and keep the best performing group.
    """  
    best_m = pd.DataFrame()
    best_p = 0
    year_sum = sum(group_year)
    for i in np.arange(len(group_year) - 1):
        group_sum = year_sum - group_year[i]
        msm = group_sum.divide(group_sum.sum(axis = 1), axis = 0)
        expected = group_year[i]
        freq_rows = expected.sum(axis = 1)
        expected = expected.divide(freq_rows, axis = 0)
        p_value = test(msm, expected, freq_rows)
        if p_value > best_p:
            best_m = msm
            best_p = p_value
    return best_m

def validate_msm(msm, test_group):
    """
    Test the obtained Markov state transition model against the final group
    """
    freq_rows = test_group.sum(axis = 1)
    expected = test_group.divide(freq_rows, axis = 0)
    return test(msm, expected, freq_rows)

