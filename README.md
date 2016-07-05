# mcmc_growth
Monte Carlo Markov Chain Tree Growth

This project attempts to predict and model tree growth in a novel way.

# Installation

TODO

# Obtaining the data

This project uses an FIA dataset for the state of Maine.  To download them:
```
wget http://apps.fs.fed.us/fiadb-downloads/CSV/ME_PLOT.csv -O data/ME_PLOT.csv
wget http://apps.fs.fed.us/fiadb-downloads/CSV/ME_TREE.csv -O data/ME_TREE.csv
```


# Tips and tricks

## Starting an IPython notebook

    cd ~/workspace/mcmc_growth
    workon mcmc_growth
    jupyter notebook

## Updating requirements

    pip freeze > requirements.txt
