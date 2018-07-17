#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 09:31:15 2018

@author: claire
"""

'''This is code for getting playlist data from the last.fm api.  To use the
api you need an api key"

Example that works:
http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=rj&api_key=API_KEY_HERE&format=json


To look up playlists, I am using a list of 2M lastfm usernames that
I downloaded as a .csv file from this website:
https://opendata.socrata.com/Business/Two-Million-LastFM-User-Profiles/5vvd-truf
'''

#####################################################################
import pandas as pd
import requests
from time import sleep

usernames_df = pd.read_csv("Two_Million_LastFM_User_Profiles.csv")
usernames = usernames_df['Username']

stem = "http://ws.audioscrobbler.com/2.0/?method="
cap = "&api_key=API_KEY_HERE&format=json"

def get_user_recenttracks (username):

    '''Function that pulls the "recenttracks" for a given username, 
    extracts the artist, track title, and time of listen, and organizes 
    into a df for each user'''
    
    api_string = stem + "user.getrecenttracks&user=" + username + cap
    user_info = requests.get(api_string).json()
    
    if len(user_info) != 3:
    
        user_tracks = user_info["recenttracks"]["track"]
        num_tracks = len(user_tracks)
    
        if num_tracks > 0:
            
            username_list = [username] * num_tracks
            artists = []
            titles = []
            times = []
    
            for j in range(0, num_tracks):
                #print(j)
            
                try:
                    artist = user_tracks[j]["artist"]["#text"]
                except:
                    artist = "NA"
            
                try:
                    title = user_tracks[j]["name"]
                except:
                    title = "NA"
           
                try: 
                    time = user_tracks[j]["date"]["#text"]
                except:
                    time = "NA"
                
                artists.append(artist)
                titles.append(title)
                times.append(time)
            
            user_df = pd.DataFrame({
                    "username":username_list,
                    "artist":artists,
                    "title":titles,
                    "time":times})    
    
            return(user_df) 
            
        else:
            pass
            
    else:                   
         pass                 
        
#########################################################################
         
'''Here I am running through the usernames and adding the recenttracks 
dataframes to a list'''

user_recenttracks_list = []   

for i in range(61276,100000):
    if i%5 == 0:
        print(i)
        sleep(1)
    
    username = usernames[i]
    user_df = get_user_recenttracks(username)
    user_recenttracks_list.append(user_df)
    
    if i%1000 == 0:
        user_recenttracks_df = pd.concat(user_recenttracks_list)
        user_recenttracks_df.to_csv('user_recenttracks.csv',index=False)
                
user_recenttracks_df = pd.concat(user_recenttracks_list)
user_recenttracks_df.to_csv('user_recenttracks.csv',index=False)


