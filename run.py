import argparse
import parser
import trim
import analyze_5
import analyze_cmeans
import os.path

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("state")
    argparser.add_argument("n_clusters", type=int)
    args = argparser.parse_args()
    if not os.path.isfile('data/'+args.state+'_raw.csv'):
        print 'Parsing data from '+args.state
        plots = parser.parse("data/"+args.state+"_TREE.csv")
        parser.cluster_prep_file(plots, 'data/'+args.state+'_raw.csv')
    print 'Data from '+args.state+' parsed'
    trim.clean('data/'+args.state+'_raw.csv')
    print 'Data cleaned'
    data_points = analyze_cmeans.cluster(
        in_file='data/forest.csv', n_clusters=args.n_clusters, norm='interval'
       )
    print 'Data clustered'
    group_year = analyze_cmeans.construct_groups(data_points, n_clusters=args.n_clusters)
    msm = analyze_cmeans.construct_msm(group_year)
    print msm
