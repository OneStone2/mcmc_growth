
# coding: utf-8

# In[ ]:

import random
from collections import defaultdict
from scipy import stats, linalg
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
from pandas import DataFrame, read_csv
import numpy as np


# In[ ]:

DATA_CSV = 'data/output.csv'
data_points = pd.read_csv(DATA_CSV, index_col = 'py')
data_points = data_points.fillna(0)


# In[ ]:

#Apply Z-score normalization
for column in data_points:
    data_points[column] = stats.zscore(data_points[column],axis=None,ddof=-1)


# In[ ]:

#Apply PCA
pca = PCA(n_components='mle')
data_pca = pca.fit_transform(data_points)


# In[ ]:

#Create the clusters based on the PCA axes
n_superclusters = 20
n_subclusters = 1
n_clusters = n_superclusters * n_subclusters
superclusters = KMeans(n_clusters=n_superclusters).fit(data_pca)
supercentroids = superclusters.cluster_centers_
labels_1 = superclusters.labels_


# In[ ]:

#And cluster a second time
#Using this snippet and then the bootstrapping is broken at the moment
data_pca = pd.DataFrame(data_pca)
data_pca.columns = map(chr, xrange(65, 65 + len(data_pca.columns)))
data_pca['cluster_1'] = [i for i in labels_1]
grouped = data_pca.groupby('cluster_1')
for name, group in grouped:
    clusters = KMeans(n_clusters=min(n_subclusters,len(group))).fit(group)
    labels_2 = clusters.labels_
    i = 0
    for py, row in group.iterrows():
        data_pca.loc[py, 'cluster_2'] = labels_2[i]
        i = i + 1
data_pca['cluster_2'] = data_pca['cluster_2'].astype(int)


# In[ ]:

plots_dd = defaultdict(lambda: [])
for i, row in data_points.iterrows():
    plots_dd[i/1000].append((i%1000, labels_1[i]))
for i in plots_dd:
    plots_dd[i].sort()


# In[ ]:

#Split all the plots randomly into 11 equally-sized groups
#The first 10 are used to create the model with cross-validation
#Once we have a Markov State transition matrix, the 11th group is used for validation
n_buckets = 10
random.seed()
group = []
while len(group) < n_buckets + 1:
    group.append([])
bucket = np.arange(n_buckets + 1).tolist()
for plot in plots_dd:
    rand = random.randint(0, len(bucket) - 1)
    group[bucket[rand]].append(plot)
    bucket.pop(rand)
    if len(bucket) == 0:
        bucket = np.arange(n_buckets + 1).tolist()


# In[ ]:

#This snippet is even more evil than the last so I'll explain the process in words.
#Take a blank matrix.
#Count the transitions the following way:
#-Separated by how many years passed
#-Separated if they belong in the test group or in one of the other 9 groups
#So there is a matrix that records transitions of 4 years,
#another that records transitions every 5 years...
#In this code, cur stores the other 9 groups and cur_obs the test group.
#Next, take the nth root of each matrix except cur_obs
#So take the 4th root of the matrix for 4 years,
#5th root of the matrix for 5 years...
#Take the weighted average of all these matrices.
#So if there are 10 times as much data for 5 years than for 4,
#the matrix for 5 years is weighted 10 times as much.
#To avoid precision errors, rescale the matrix so all rows sum to 1.
#Next, test this matrix against the test group.
#Test separately the transitions for 4 years, the transitions for 5...
#Take the chi-square test for those cells with values greater than 5 and
#obtain a p-value.
#Repeat all this process 9 more times, each with a different test group.
#Out of the 10 matrices, choose the one that got the higher p-value.
best = pd.DataFrame(1 / n_clusters, index=np.arange(n_clusters), columns=np.arange(n_clusters))
best_p = 0.0
for i in np.arange(n_buckets):
    cur = defaultdict(
        lambda: pd.DataFrame(
            0.0, index=np.arange(n_clusters),
            columns=np.arange(n_clusters)
        )
    )
    state_weight = defaultdict(lambda: [0]*n_clusters)
    diff_weight = defaultdict(int)
    sum_diff_weight = 0.0
    cur_obs = defaultdict(
        lambda: pd.DataFrame(
            0, index=np.arange(n_clusters),
            columns=np.arange(n_clusters)
        )
    )
    for j in np.arange(n_buckets):
        for plot in (plots_dd[x] for x in group[j]):
            prev_y = None
            prev_s = None
            for year, state in plot:
                if prev_y != None:
                    diff_y = int(float(year - prev_y))
                    if i == j:
                        cur_obs[diff_y].loc[prev_s, state] += 1
                    else:
                        cur[diff_y].loc[prev_s, state] += 1
                        state_weight[diff_y][prev_s] += 1
                        diff_weight[diff_y] += 1
                        sum_diff_weight += 1
                prev_y = year
                prev_s = state
    final = pd.DataFrame(0.0, index=np.arange(n_clusters), columns=np.arange(n_clusters))
    for diff_y in diff_weight:
        diff_weight[diff_y] = diff_weight[diff_y] / sum_diff_weight
    for diff_y in cur:
        state_weight[diff_y] = [x if x != 0 else 1 for x in state_weight[diff_y]]
        cur[diff_y] = cur[diff_y].divide(state_weight[diff_y], axis=0)
        cur[diff_y] = pd.DataFrame(
            linalg.fractional_matrix_power(cur[diff_y].values, 1.0/diff_y)
        )
        #Drop the imaginary part. It is small, so it doesn't affect performance
        cur[diff_y] = cur[diff_y].apply(lambda x: np.real(x))
        #Some values will be negative. Set those to 0
        cur[diff_y][cur[diff_y] < 0] = 0
        #Rescale the rows so they add up to 1
        cur[diff_y] = cur[diff_y].divide(cur[diff_y].sum(axis=1), axis=0)
        cur[diff_y].fillna(0, inplace=True)
        final = final + cur[diff_y].multiply(diff_weight[diff_y])
    #Rescale the rows so they add up to 1
    final = final.divide(final.sum(axis=1), axis=0)
    #Test how good the model is using chi-squared test
    exp_arr = []
    obs_arr = []
    for diff_y in state_weight:
        cur_exp = pd.DataFrame(np.linalg.matrix_power(final, diff_y))
        cur_exp = cur_exp.multiply(cur_obs[diff_y].sum(axis=1), axis=0)
        #Drop all cells with an expected value of less than 5
        #Chi-square relies on having 5 or more data points per cell
        #Performance of cells with low probabilities do not affect much the model
        for k, row in cur_exp.iterrows():
            indices = [l for l, v in enumerate(row) if v >= 5]
            for l in indices:
                exp_arr.append(cur_exp.iloc[k, l])
                obs_arr.append(cur_obs[diff_y].iloc[k, l])
    p_value = stats.chisquare(obs_arr, exp_arr)[1]
    if p_value > best_p:
        best_p = p_value
        best = final


# In[ ]:

#Then, test the best matrix against the 11th group
cur_obs = defaultdict(
    lambda: pd.DataFrame(
        0, index=np.arange(n_clusters),
        columns=np.arange(n_clusters)
    )
)
for plot in (plots_dd[x] for x in group[n_buckets]):
    prev_y = None
    prev_s = None
    for year, state in plot:
        if prev_y != None:
            diff_y = int(float(year - prev_y))
            cur_obs[diff_y].loc[prev_s, state] += 1
        prev_y = year
        prev_s = state
exp_arr = []
obs_arr = []
for diff_y in state_weight:
    cur_exp = pd.DataFrame(np.linalg.matrix_power(best, diff_y))
    cur_exp = cur_exp.multiply(cur_obs[diff_y].sum(axis=0), axis=1)
    #Drop all cells with an expected value of less than 5
    #Chi-square relies on having 5 or more data points per cell
    #Performance of cells with low probabilities do not affect much the model
    for k, row in cur_exp.iterrows():
        indices = [l for l, v in enumerate(row) if v >= 5]
        for l in indices:
            exp_arr.append(cur_exp.iloc[k, l])
            obs_arr.append(cur_obs[diff_y].iloc[k, l])
print stats.chisquare(obs_arr, exp_arr)[1]
best

