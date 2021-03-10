import random, itertools, collections, random
import pandas as pd
from collections import Counter
import sqlite3
import seaborn as sns
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pybaseball as pyb
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std
# import webscrap


FANTASY_STATS_HITTERS = ['R','RBI','AVG','HR']

FANTASY_STATS_PITCHERS = ['ERA','K/9','BB/9','HR/9','IP']


def create_next_stat(years= tuple,stat=str,position=0): 
    """This will get you a df with all stats shifted one year for predicting next years stats"""

    if position == 0: #0 for hitters; 1 for pitchers
        if type(years) == int:
            batters = pyb.batting_stats(years)
        else:
            batters = pyb.batting_stats(years[0],years[1])
        batters[f'{stat}/PA'] = batters[stat]/batters['PA']
        batters[f'{stat}_next_year'] = batters.sort_values(['Name', 'Season'], ascending=False).groupby('Name')[f'{stat}/PA'].shift()
        batters = batters.loc[batters[f'{stat}_next_year'].notnull()]
        batters = batters.fillna(0)

        return batters
    
    if position == 1:
        if type(years) == int:
            pitchers = pyb.pitching_stats(years)
        else:
            pitchers = pyb.pitching_stats(years[0],years[1])
        pitchers[f'{stat}_next_year'] = pitchers.sort_values(['Name', 'Season'], ascending=False).groupby('Name')[stat].shift()
        pitchers = pitchers.loc[pitchers[f'{stat}_next_year'].notnull()]
        pitchers = pitchers.fillna(0)
        
        return pitchers

def run_regression(df_fit,features,find,test=True,df_pred=None): 
    """
    Run this for multiple regression algorithms with multiple feature sets. Find the best feature set and algorithm for given 'y'
    Then predict and add to PD and use that to create graphs of features that were used to get the 'y' and highlight biggest jumps for this year predictions
    Write to file and look at graphs of players.

    """
    # Gradient Boost allows outliers to curve the data more, select quantile for identifying larger outliers
    # Alpha lower to allow for guys like Trout and guys with good seasons to get better predictions for "breakout years"
    reg = GradientBoostingRegressor(loss='quantile',alpha=.85,n_estimators=200,min_samples_split=10,max_depth=len(features))


    # Run the df_fit
    X = df_fit[features]
    y = df_fit[f'{find}_next_year']

    # Split the data for train and test
    X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=random.randint(1,99),test_size=.2)

    reg.fit(X_train,y_train) #fit with train
    if test: #if test is true then we will return the MEA of y_pred
        y_pred = reg.predict(X_test)
        mea = mean_absolute_error(y_pred,y_test)

        return mea

    elif test == False: #if we passed df_pred and test is false then we will run reg algernym
        """ ============ CAN BE USED IF YOU IMPLEMENT A NEW FEATURE =============
        df_fit['train_{}'.format(find)] = reg.predict(X) #append pred for fit data
        plt.figure(figsize=(10,8))
        sns.color_palette("Paired")
        plt.title("Training data for {}".format(find))
        sns.scatterplot(x=find,y=f'train_{find}',data=df_fit,hue='Name') #graph the difference between actual stat and fit stat pred
        """

        P = df_pred[features]

        y_pred = reg.predict(P)

        #For pitchers return rate stats and try to predict IP for the pitcher with age and other factors
        return y_pred #return array of pred stats, all will be rate stats, must multiply results by full season numbers

def regression_final(features,find,players,write_csv=None,position=0):
    """
    RUNS REGRESSION ON NOTEABLE PLAYERS
    PARAM: features: list of features that you want to run regression on
    PARAM: players: players you want to predict stats for
    PARAM: write_csv will write to a csv file

    IF NOT WRITE CSV THEN RETURN THE DF FOR TEST OR OTHER ANALYSIS
    
    """

    list_for_con = [] #list of df that will be concatted of noteable players

    pred_stats_ls = {}
    names = []


    for stat in find:
        
        print(f'Regression prediction on {stat}')
        for name in players:
            
            if name not in names:
                names.append(name)
                print('appending {}'.format(name))

        for name in names:

            print('Getting next year stat for {}'.format(name))

            if position == 0:
                
                df1 = create_next_stat(years=(2015,2020),stat=stat,position=position)# create next year stat for player I want to predict
                df_fit = df1 # create df to be fit into the model with all players from 2015-2020

                df2 = pyb.batting_stats(2019,2020)
                df_pred = df2.loc[df2['Name'] == name]
            
            elif position == 1:

                df1 = create_next_stat(years=(2015,2020),stat=stat,position=position)# create next year stat for player I want to predict
                df_fit = df1 # create df to be fit into the model with all players from 2015-2020

                df2 = pyb.pitching_stats(2019,2020)
                df_pred = df2.loc[df2['Name'] == name]

            if len(list_for_con) < len(names): #if it is full with all players skip
                list_for_con.append(df_pred)

        reg_df = pd.concat(list_for_con,axis=0) #create df for players to find regression
        
        if position == 0: #turn stats into rate stats for hitters, pitcher stats are already all rate stats
            reg_df[f'{stat}/PA'] = reg_df[stat]/reg_df['PA']
        
        else:
            pass

        pred = run_regression(df_fit, features, stat, test=False,df_pred=reg_df) # run regression for noteable players
        if position == 0:
            pred_stats_ls[stat] = [p *600 for p in pred] #Getting stats per PA so multiply by 600 PA for pred stats
        elif position == 1:
            pred_stats_ls[stat] = pred

        print(f'Got {stat} pred of {pred}')
        list_for_con = [] #reset list to remove duplicates
    for stat,pred in pred_stats_ls.items():
        reg_df[f'pred_{stat}_2021'] = pred #append in new col the pred stat
    
    if write_csv:
        reg_df.to_csv('/Users/jonnymurillo/Desktop/Python_Code/Baseball_2021/{}.csv'.format(write_csv))
        print("wrote {}".format(write_csv))

    else:
        return reg_df



if __name__ == '__main__':

    feat_1 = ['G','PA','OPS','BB%','K%','AVG','LD%','GB%','HR/FB','ISO','O-Swing%','Z-Swing%','Swing%','O-Contact%','Z-Contact%','Contact%','SwStr%','Barrel%','HardHit%']

    feat_2 = ['Age','xFIP','HR/FB','O-Swing%','Z-Swing%','Swing%','O-Contact%','Z-Contact%','Contact%','SwStr%','Barrel%','HardHit%']

    find = ['RBI','R','AVG','HR']

    csv_name = ['vet_comeback','bounceback','breakout']

    #list of players prepare to draft
    # pitchers = ['Clayton Kershaw','Dustin May','Gerrit Cole','Trevor Bauer','Luke Weaver','Zac Gallen','James Paxton']
    # hitters = ['Luke Voit']

    # conn = sqlite3.connect('/Users/jonnymurillo/baseball.db')

    df = pd.read_sql(sql= "SELECT * FROM hitters",con= conn)
    hitters = []

    for h in df['Name']:
        if h not in hitters:
            hitters.append(h)

    regression_final(features=feat_1,find=FANTASY_STATS_HITTERS,players=hitters,write_csv='HittersToLookAt',position=0)

    conn = sqlite3.connect('/Users/jonnymurillo/baseball.db')

    df2 = pd.read_sql(sql= "SELECT * FROM pitchers",con= conn)
    pitchers = []

    for h in df2['Name']:
        if h not in pitchers:
            pitchers.append(h)
            
    regression_final(features=feat_2,find=FANTASY_STATS_PITCHERS,players=pitchers,write_csv='PitchersToLookAt',position=1)

    
    
    

    
    

    





    






