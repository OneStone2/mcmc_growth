import argparse
import os.path
import read
import analyze
import numpy as np
import sys

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("state", help="2-letter code for the US state")
    argparser.add_argument("--online", dest='online', const=True, default=False, action='store_const', help="Use FIA website")
    args = argparser.parse_args()
    args.state = [args.state]
    if args.state == ['US']:
        args.state = ['AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WV', 'WI']
    for state in args.state:
        if not (
            os.path.isfile('data/'+state+'_2a.csv') 
            or os.path.isfile('data/'+state+'_2a.csv')
        ):
            if not os.path.isfile('data/'+state+'_1.csv'):
                if args.online:
                    plots = read.parse(state, online=True)
                else:
                    plots = read.parse(state, online=False)
                read.cluster_prep_file(plots, state)
            read.clean(args.state, b=True)
        print 'Analyzing', state
        print analyze.analyze_r01(state, human=True, time=True)
        print analyze.analyze_r02(state, human=True, time=True)
        print analyze.analyze_r03(state, human=True, time=True)
        print analyze.analyze_r04(state, human=True, time=True)
