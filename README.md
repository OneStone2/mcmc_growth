# mcmc_growth
Monte Carlo Markov Chain Tree Growth

This project attempts to predict and model tree growth in a novel way.

# Installation

```
# Initial install:
sudo pip install virtualenvwrapper
echo "export WORKON_HOME=~/Envs" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
echo "add r" >> ~/.bashrc.mine
source ~/.bashrc
mkvirtualenv mcmc_growth
pip install -r requirements.txt


# After logging out of DebAthena, to re-initialize env:
sudo pip install virtualenvwrapper
source ~/.bashrc
workon mcmc_growth
```

# Operation
```
python run.py [--online] state
```
state code is a 2-letter code for the state (e.g. ME)

state=US if you want to run the model for all contiguous states.

--online is to download the required files on the fly.

```
python update.py [--online] state
```
Run this program after changing the read.py file.

# Obtaining the data

Sometimes, the connection the the FIA database is unstable.

To download them manually:
```
wget http://apps.fs.fed.us/fiadb-downloads/CSV/ME_PLOT.csv -O data/ME_PLOT.csv
wget http://apps.fs.fed.us/fiadb-downloads/CSV/ME_TREE.csv -O data/ME_TREE.csv
wget http://apps.fs.fed.us/fiadb-downloads/CSV/ME_COND.csv -O data/ME_COND.csv
```
For other states, replace ME with the corresponding state code.


# Tips and tricks

## Starting an IPython notebook

    cd ~/workspace/mcmc_growth
    workon mcmc_growth
    jupyter notebook

## Updating requirements

    pip freeze > requirements.txt
