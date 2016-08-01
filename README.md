# mcmc_growth
Forest Modeling for Carbon Sequestration

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
All the command must be performed on the application folder.

To execute iterations 1-4:
```
python run.py [--online] state
```
state code is a 2-letter code for the state (e.g. ME)

state=US if you want to run the model for all contiguous states.

--online is to download the required files on the fly.

Note that this program doesn't output the model, only the RMSE.

```
python update.py [--online] state
```
Run this program after changing the read.py file.

To execute iterations 5-8:
```
rstudio
```

Open analyze.R and execute Source.

This program outputs RMSE but stores the models as mdlxy, where x is the iteration number and y represents human interaction (a) or not (b).

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
