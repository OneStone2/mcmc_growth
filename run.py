import argparse
import os.path
import read
import analyze
import numpy as np

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("state", help="2-letter code for the US state")
    argparser.add_argument("--online", dest='online', const=True, default=False, action='store_const', help="Use FIA website")
    args = argparser.parse_args()
    
    if not (
        os.path.isfile('data/'+args.state+'_2a.csv') 
        or os.path.isfile('data/'+args.state+'_2a.csv')
    ):
        if not os.path.isfile('data/'+args.state+'_1.csv'):
            if args.online:
                plots = read.parse(args.state, online=True)
            else:
                plots = read.parse(args.state, online=False)
            read.cluster_prep_file(plots, args.state)
        read.clean(args.state, b=True)

    N_REP = 1
    print 'Including human interaction:'
    sum = 0
    for i in np.arange(N_REP):
        sum += analyze.analyze_r01(args.state, human=True, time=True)
    print '[1]', sum / N_REP
    sum = 0
    for i in np.arange(N_REP):
        sum += analyze.analyze_r02(args.state, human=True, time=True)
    print '[2]', sum / N_REP
    sum = 0
    for i in np.arange(N_REP):
        sum += analyze.analyze_r03(args.state, human=True, time=True)
    print '[3]', sum / N_REP
    sum = 0
    for i in np.arange(N_REP):
        sum += analyze.analyze_r04(args.state, human=True, time=True)
    print '[4]', sum / N_REP
    print 'Excluding human interaction:'
    sum = 0
    for i in np.arange(N_REP):
        sum += analyze.analyze_r01(args.state, human=False, time=True)
    print '[1]', sum / N_REP
    sum = 0
    for i in np.arange(N_REP):
        sum += analyze.analyze_r02(args.state, human=False, time=True)
    print '[2]', sum / N_REP
    sum = 0
    for i in np.arange(N_REP):
        sum += analyze.analyze_r03(args.state, human=False, time=True)
    print '[3]', sum / N_REP
    sum = 0
    for i in np.arange(N_REP):
        sum += analyze.analyze_r04(args.state, human=False, time=True)
    print '[4]', sum / N_REP
