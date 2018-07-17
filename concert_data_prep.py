#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 13:53:31 2018

@author: claire
"""

import pandas as pd


'''Pull up all the scraped files from songkick and clean them up'''
'''At this point I'm just going to work with the concert data'''

concert_df = pd.read_csv('concert_df.csv')
concert_df4 = pd.read_csv('concert_df_US4.csv')
concert_df = pd.concat([concert_df,concert_df4])
concert_df.to_csv('concert_df.csv',index=False)

concert_df = concert_df.drop(['isfest','festival','date'],axis=1)
concert_df = concert_df.drop_duplicates()
concert_df.reset_index(drop=True,inplace=True)
concert_df.shape
#(228201, 2)


''' Many of the concerts have more than one artist playing.  Need to 
separate their names and then add them back to the dataframe'''

dict_array=[]

for i in range(0,len(concert_df)):
    a = concert_df.artist[i]
    a_split = a.split(',')
    
    if len(a_split) > 1:
        for j in range(0,len(a_split)):
            a_sub = a_split[j].strip()
            if a_sub.startswith('and '):
                a_sub = a_sub[4:]
            dict_row = {'artist':a_sub,
                        'venue':concert_df.venue[i]}
            dict_array.append(dict_row)
            
    else:
        dict_row = {'artist':a,
                    'venue':concert_df.venue[i]}
        dict_array.append(dict_row)
        
concert_df_expand = pd.DataFrame(dict_array)
concert_df_expand = concert_df_expand.drop_duplicates()
artist_blanks = concert_df_expand.loc[concert_df_expand['artist']==''].index
concert_df_expand = concert_df_expand.drop(index = artist_blanks)
concert_df_expand.reset_index(drop=True,inplace=True)
concert_df_expand.shape
#(363369, 2)

concert_df_expand.to_csv('concert_df_expand.csv',index=False)

######################################################################

venue_list = concert_df_expand['venue']
venue_unique = venue_list.drop_duplicates()
len(venue_unique)
#37298

venue_counts = concert_df_expand.groupby(['venue'])['artist'].count()
venue_has5 = venue_counts.loc[venue_counts>=5].index
venue_has5 = pd.Series(venue_has5)
len(venue_has5)
#8981

concert_df_filt = concert_df_expand[concert_df_expand['venue'].isin(venue_has5)]
concert_df_filt.shape
#(318427, 2)

artist_counts = concert_df_filt.groupby(['artist'])['venue'].count()
artist_has5 = artist_counts.loc[artist_counts>=5].index
artist_has5 = pd.Series(artist_has5)
len(artist_has5)
#13877

concert_df_filt = concert_df_filt[concert_df_filt['artist'].isin(artist_has5)]
concert_df_filt.reset_index(drop=True,inplace=True)
concert_df_filt.shape
#(174568, 2)

concert_df_filt.to_csv('concert_df_filt.csv',index=False)


#########################################################################

'''Create the geographic info for the venues to be used'''

def paste_strings(sl):
    out = ''
    for s in sl:
        out += s
    return(out)

dict_array=[]

for i in range(0,len(venue_has5)):
    v = venue_has5[i]
    v_split = v.split(',')
    n = len(v_split)
    
    dict_row = {'venue':v,
                'vname':paste_strings(v_split[0:(n-3)]),
                'city':v_split[n-3].strip(),
                'state':v_split[n-2].strip(),
                'country':v_split[n-1].strip()} 

    dict_array.append(dict_row)

venue_address = pd.DataFrame(dict_array)
venue_address = venue_address.loc[venue_address['country']=='US']
venue_address = venue_address.loc[venue_address['vname']!='Unknown venue']
venue_address.shape
#(8641, 5)

venue_address.to_csv('venue_address.csv',index=False)



'''Geolocate the venues'''

import geopy
from geopy.geocoders import Nominatim, GoogleV3
import numpy as np
from time import sleep

venue_address = pd.read_csv('venue_address.csv')
venue_list = venue_address['venue']

venue_geo_df = pd.read_csv('venue_geo.csv')
geocode_list = venue_list.loc[np.logical_not(venue_list.isin(venue_geo_df['venue']))]
geocode_list.reset_index(drop=True,inplace=True)

geolocator = GoogleV3()

dict_array = []

for i in range(0,len(geocode_list)):
    
    if i % 10 == 0:
        print(i)
        
    v = geocode_list[i]
    sleep(1)
    
    try:
        location = geolocator.geocode(v)
        lon = location.longitude
        lat = location.latitude
        
        dict_row = {'venue':v,
                    'lon':lon,
                    'lat':lat} 
        
        dict_array.append(dict_row)
        
    except:
        pass
           
venue_geo_df4 = pd.DataFrame(dict_array)
venue_geo_df4.to_csv('venue_geo_df4.csv',index=False)

## Google gave way less NaNs than Nominatim
## Doing this slowly at least keeps it from crashing
## About 100 per min at Insight

venue_geo_df = venue_geo_df[['venue','lon','lat']]
venue_geo_df4 = venue_geo_df4[['venue','lon','lat']]
venue_geo_df = pd.concat([venue_geo_df,venue_geo_df4])
venue_geo_df = venue_geo_df.drop_duplicates() 
venue_geo_df = venue_geo_df.dropna()
venue_geo_df.shape
#(7884, 3)
venue_geo_df.to_csv('venue_geo.csv',index=False)

'''Merge together all the location info into a single dataframe'''

venue_location = pd.merge(venue_geo_df, venue_address, left_on='venue', right_on='venue', how='left')
venue_location.to_csv('venue_location.csv',index=False)







