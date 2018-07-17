#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 16:26:19 2018

@author: claire
"""

import pandas as pd
import numpy as np

## Combining data from the first 20,000 users
pl_df = pd.read_csv('user_recenttracks.csv')
pl_df = pl_df[['username','artist']]

pl_df = pl_df.drop_duplicates()
## About 50% of rows are lost here

artist_list = pl_df['artist']
artist_list = artist_list.drop_duplicates()
len(artist_list)
#182048

user_counts = pl_df.groupby('username')['artist'].count()
user_has5 = user_counts.loc[user_counts>=5].index
user_has5 = pd.Series(user_has5)
len(user_has5)
#52718

pl_df_filt = pl_df[pl_df['username'].isin(user_has5)]
pl_df_filt.shape
#(1217443, 2)

artist_counts = pl_df_filt.groupby('artist')['username'].count()
artist_has5 = artist_counts.loc[artist_counts>=5].index
artist_has5 = pd.Series(artist_has5)
len(artist_has5)
#29034

artist_has10 = artist_counts.loc[artist_counts>=10].index
artist_has10 = pd.Series(artist_has10)
len(artist_has10)
#16183

artist_has20 = artist_counts.loc[artist_counts>=20].index
artist_has20 = pd.Series(artist_has20)
len(artist_has20)
#8848

pl_df_filt = pl_df_filt[pl_df_filt['artist'].isin(artist_has20)]
pl_df_filt.shape
#(822235, 2)

pl_df_filt.to_csv('playlist_df_filt.csv',index=False)

###########################################################################

'''Bring in concert data and match artist names from listener dataset to 
artist names in the concert dataset.  Get as many matches as possible!'''

pl_df_filt = pd.read_csv('playlist_df_filt.csv')

'''This File has already been filtered to include only artist and venues
with at least 5 interactions'''
concert_df_filt = pd.read_csv('concert_df_filt.csv')

concert_df_filt.shape
#(174568, 2)

artist_concert_names = concert_df_filt['artist'].drop_duplicates()
len(artist_concert_names)
#13877

artist_playlist_names = pl_df_filt['artist'].drop_duplicates()
len(artist_playlist_names)
#8848

artist_both = artist_playlist_names[artist_playlist_names.isin(artist_concert_names)]
len(artist_both)
#2291

artist_playlist_only = artist_playlist_names[np.logical_not(artist_playlist_names.isin(artist_concert_names))]
artist_concert_only = artist_concert_names[np.logical_not(artist_concert_names.isin(artist_playlist_names))]

## From examining these lists, it seems like almost all of the artists that
## are present in the playlist data but not in the concert data are dead.

##########################################################################

## Create artist similarity

user_list = pl_df_filt['artist'].drop_duplicates()
item_list = pl_df_filt['username'].drop_duplicates()

'''Make unique mapping of artist name and venue name to integer'''

user_df = pd.DataFrame({
        'user':user_list,
        'user_id':range(1,(len(user_list)+1))})
        
item_df = pd.DataFrame({
        'item':item_list,
        'item_id':range(1,(len(item_list)+1))})

artist_pl_ind = user_df
listener_pl_ind = item_df

artist_pl_ind.to_csv("artist_pl_ind.csv",index=False)
listener_pl_ind.to_csv("listener_pl_ind.csv",index=False)

artist_df = pd.merge(pl_df_filt, user_df, left_on='artist', right_on='user', how='left')
artist_int = artist_df['user_id']
x = artist_int.value_counts()
min(x)

username_df = pd.merge(pl_df_filt, item_df, left_on='username', right_on='item', how='left')
username_int = username_df['item_id']
y = username_int.value_counts()
min(y)

df = pd.DataFrame({
        'user_id':artist_int,
        'item_id':username_int,
        'rating':1})

df.to_csv("playlist_df.csv",index=False)

artist_pl_ind = pd.read_csv("artist_pl_ind.csv")
listener_pl_ind = pd.read_csv("listener_pl_ind.csv")
df = pd.read_csv("playlist_df.csv")
df = df.drop("Unnamed: 0",axis=1)

n_users = df.user_id.unique().shape[0]
n_items = df.item_id.unique().shape[0]
print (str(n_users) + ' users')
print (str(n_items) + ' items')
#8848 users
#52256 items

ratings = np.zeros((n_users, n_items))
for row in df.itertuples():
    ratings[row[1]-1, row[2]-1] = row[3]
ratings

x = np.sum(ratings,axis=0)
min(x)
y = np.sum(ratings,axis=1)
min(y)

sparsity = float(len(ratings.nonzero()[0]))
sparsity /= (ratings.shape[0] * ratings.shape[1])
sparsity *= 100
sparsity
#0.17783395301639224
 
artist_listener_df = pd.DataFrame(ratings)
artist_listener_df.to_csv('artist_listener_df.csv',index=False)

def fast_similarity(ratings, kind='user', epsilon=1e-9):
    # epsilon is a small number for handling dived-by-zero errors
    if kind == 'user':
        sim = ratings.dot(ratings.T) + epsilon
    elif kind == 'item':
        sim = ratings.T.dot(ratings) + epsilon
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)

artist_similarity = fast_similarity(ratings, kind='user')
print (user_similarity[:12, :5])


def get_similar_artist(artistname):
    artist_ind = user_df.loc[user_df['user']==artistname]['user_id']
    artist_ind = int(artist_ind)-1
    simvals = list(artist_similarity[artist_ind,:])
    simvals[artist_ind] = 0
    simvals = pd.Series(simvals)
    simvals.index = user_df['user']
    simvals = simvals.sort_values(ascending=False)
    return(simvals[0:9])


artist_pl_ind.reset_index(drop=True,inplace=True)
in_concert = artist_pl_ind.loc[artist_pl_ind['user'].isin(artist_concert_names)].index
artist_similarity_filt = artist_similarity[:,in_concert]

in_concert_names = artist_pl_ind.loc[artist_pl_ind['user'].isin(artist_concert_names)]
in_concert_names.to_csv('in_concert_names.csv',index=False)

artist_similarity_df = pd.DataFrame(artist_similarity_filt)
artist_similarity_df.to_csv('artist_similarity_df.csv',index=False)

















