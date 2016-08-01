"""
Contains code for revisions 1-4
All functions return RMSE
"""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn import linear_model
import random
import math

def analyze_r01(state, human, time):
    """
    Iteration 1
    """
    #Read data
    if human:
        DATA_CSV = 'data/'+state+'_2a.csv'
    else:
        DATA_CSV = 'data/'+state+'_2b.csv'
    data_points = pd.read_csv(DATA_CSV)
    #Shift carbon and year one row back
    nr1 = data_points['carb']
    nr1 = nr1.iloc[1:len(nr1)]
    nr2 = data_points['py']
    nr2 = nr2.iloc[1:len(nr2)]
    data_points = data_points.iloc[0:len(data_points.index)-1]
    nr1.index = np.arange(len(nr1.index))
    nr2.index = np.arange(len(nr2.index))
    #Now we can calculate difference in carbon
    if time:
        data_points.loc[:, 'growth'] = (nr1 - data_points['carb']) / (nr2 - data_points['py'])
    else:
        data_points.loc[:, 'growth'] = nr1
    data_points.loc[:, 'post_py'] = nr2
    data_points = data_points[data_points.post_py // 10000 == data_points.py // 10000]
    data_points.drop(['py', 'post_py'], axis=1, inplace=True)
    data_points.index = np.arange(len(data_points.index))
    data_points = data_points.loc[:, ['carb', 'growth']]
    data_points = data_points.as_matrix().tolist()
    #Split data into training and testing
    random.shuffle(data_points)
    training = data_points[0:9 * len(data_points) / 10]
    test = data_points[9 * len(data_points) / 10:len(data_points)]
    training = np.array(training)
    #Create the linear regression function
    m = stats.linregress(training).slope
    n = stats.linregress(training).intercept
    sq_error = 0.0
    #Perform validation
    for elem in test:
        predicted = m * elem[0] + n
        actual = elem[1]
        sq_error += (actual - predicted) ** 2
    mse = math.sqrt(sq_error/len(test))
    return mse

def analyze_r02(state, human, time):
    """
    Revision 2
    """
    #Read data
    if human:
        DATA_CSV = 'data/'+state+'_2a.csv'
    else:
        DATA_CSV = 'data/'+state+'_2b.csv'
    data_points = pd.read_csv(DATA_CSV)
    #Shift carbon and year one row back
    nr1 = data_points['carb']
    nr1 = nr1.iloc[1:len(nr1)]
    nr2 = data_points['py']
    nr2 = nr2.iloc[1:len(nr2)]
    data_points = data_points.iloc[0:len(data_points.index)-1]
    nr1.index = np.arange(len(nr1.index))
    nr2.index = np.arange(len(nr2.index))
    #Now we can calculate difference in carbon
    if time:
        data_points.loc[:, 'growth'] = (nr1 - data_points['carb']) / (nr2 - data_points['py'])
    else:
        data_points.loc[:, 'growth'] = nr1
    data_points.loc[:, 'post_py'] = nr2
    data_points = data_points[data_points.post_py // 10000 == data_points.py // 10000]
    data_points.drop(['py', 'post_py'], axis=1, inplace=True)
    data_points.index = np.arange(len(data_points.index))
    data_points = data_points.loc[:, ['carb', 'growth']]
    data_points = data_points.as_matrix().tolist()
    #Split data into 10 groups
    N_GROUPS = 10
    random.shuffle(data_points)
    groups = []
    prev_cutoff = 0
    #Create the model while performing cross-validation
    for i in np.arange(N_GROUPS):
        next_cutoff = (i + 1) * len(data_points) / N_GROUPS
        groups.append(data_points[prev_cutoff:next_cutoff])
        prev_cutoff = next_cutoff
    min_mse = float("inf")
    for i in np.arange(N_GROUPS):
        training = []
        test = []
        for j, group in enumerate(groups):
            if j == i:
                test = group
            else:
                training.extend(group)
        training = np.array(training)
        m = stats.linregress(training).slope
        n = stats.linregress(training).intercept
        sq_error = 0.0
        for elem in test:
            predicted = m * elem[0] + n
            actual = elem[1]
            sq_error += (actual - predicted) ** 2
        mse = math.sqrt(sq_error/len(test))
        if mse < min_mse:
            min_mse = mse
    return min_mse

def analyze_r03(state, human, time, called_as_r04=False):
    """
    Revision 3
    """
    #Read data
    if human:
        DATA_CSV = 'data/'+state+'_2a.csv'
    else:
        DATA_CSV = 'data/'+state+'_2b.csv'
    data_points = pd.read_csv(DATA_CSV)
    #Shift carbon and year one row back
    nr1 = data_points['carb']
    nr1 = nr1.iloc[1:len(nr1)]
    nr2 = data_points['py']
    nr2 = nr2.iloc[1:len(nr2)]
    data_points = data_points.iloc[0:len(data_points.index)-1]
    nr1.index = np.arange(len(nr1.index))
    nr2.index = np.arange(len(nr2.index))
    #Now we can calculate difference in carbon
    if time:
        data_points.loc[:, 'growth'] = (nr1 - data_points['carb']) / (nr2 - data_points['py'])
    else:
        data_points.loc[:, 'growth'] = nr1
    data_points.loc[:, 'post_py'] = nr2
    data_points = data_points[data_points.post_py // 10000 == data_points.py // 10000]
    mode = stats.mode((data_points['post_py'] - data_points['py']).tolist()).mode[0]
    #Iteration 4 is same as 3 but ignores time steps other than the most common
    if called_as_r04:
        data_points = data_points[data_points.post_py - data_points.py == mode]  
    data_points.drop(['py', 'post_py'], axis=1, inplace=True)
    data_points.index = np.arange(len(data_points.index))
    data_points = data_points.loc[:, ['carb', 'lat', 'lon', 'growth']]
    data_points = data_points.as_matrix().tolist()
    for i, elem in enumerate(data_points):
        elem[0] = [x for x in elem]
        elem[0].pop()
        elem[1] = elem[-1]
        data_points[i] = elem[0:2]
    #Split data into 10 groups
    N_GROUPS = 10
    random.shuffle(data_points)
    groups = []
    prev_cutoff = 0
    for i in np.arange(N_GROUPS):
        next_cutoff = (i + 1) * len(data_points) / N_GROUPS
        groups.append(data_points[prev_cutoff:next_cutoff])
        prev_cutoff = next_cutoff
    min_mse = float("inf")
    #Create the model while performing cross-validation
    for i in np.arange(N_GROUPS):
        training = []
        test = []
        for j, group in enumerate(groups):
            if j == i:
                test = group
            else:
                training.extend(group)
        training = np.array(training).T.tolist()
        clf = linear_model.LinearRegression()
        clf.fit(training[0], training[1])
        coef = clf.coef_
        cons = clf.intercept_
        sq_error = 0.0
        for elem in test:
            predicted = sum(coef * elem[0]) + cons
            actual = elem[1]
            sq_error += (actual - predicted) ** 2
        mse = math.sqrt(sq_error/len(test))
        if mse < min_mse:
            min_mse = mse
    return min_mse

def analyze_r04(state, human, time):
    """
    Revision 4
    """
    return analyze_r03(state, human, time, called_as_r04=True)
