# StageFinder - A venue recommendation system for bands

[StageFinder](http://stagefinder.site) is a web app that recommends venues for bands to perform in based on the band's musical style, fanbase, and desired location.  The recommendation system was built using python from listener playlists from last.fm and concert data from songkick.  The front-end was built using R/shiny with leaflet and displays a map with the top ten recommended venues within the map area.  This project was completed as part of the [Insight Data Science](https://www.insightdatascience.com/) program in June 2018.

### Method

50,000 user playlists were collected from [last.fm](http://last.fm) using the last.fm API.  These listener playlists were used to determine similarity among musical groups using cosine similarity.  Additionally, information on all concerts occurring in the United States over the past year were scraped from [Songkick](http://songkick.com) using python selenium, resulting in a dataframe of over 300,000 concert events.  These two data sources were combined in a custom collaborative filtering model to recommend venues to bands.  For each artist, the similarity to each other artist was used to assign values to all venue/artist interactions in the concert history dataframe.  These values were summed for each venue across all artists to create a final venue recommendation score (a high value for this score indicates that many very similar artists have played at that venue).  Finally, venue addresses were geolocated using the Google API to filter recommendations according to a given geographic area.  

### List of files and what they contain:

* ```songkick_scraper.py```: Thousands of concert events are scraped from the songkick webpage.

* ```get_lastfm_data.py```: Thousands of last.fm playlists are gathered and stored in a data frame using the Last.fm API.

* ```concert_data_prep.py```: The concert history data are cleaned up and prepared.  Geographic information on venues is extracted and addresses are geolocated.

* ```playlist_data_prep.py```: The lastfm playlist data are cleaned up and prepared.  Artist names are reconciled between the two datasets.

* ```app_prep.R```: The output of the analysis was reshaped to save memory for input into the Shiny app.

* ```app.R```: This is where the shiny app was created.  The app displays a map and recommendations are continuously updated based on the location shown in the map.
