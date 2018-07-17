# StageFinder

I created a website (stagefinder.site) to recommend venues to bands based on their musical style, fanbase and desired location.  The project was created using python and R/shiny with data from listeners’ last.fm playlists as well as concert data scraped from songkick.  I used people's last.fm playlists to determine similarity among musical groups.  This information was combined with concert history data (who has played where) in a collaborative filtering model to create the recommendations.  I also geolocated the venues in order to provide recommendations which are restricted to a given geographic area.   

Here is a list of files and what they contain:

get_lastfm_data.py: Thousands of lastfm playlists are gathered and stored in a data frame using the Last.fm api.
songkick_scraper.py: Thousands of concert events are scraped from the songkick webpage
concert_data_prep.py: The concert history data are cleaned up and prepared.  Geographic information is extracted and addresses are geolocated.
playlist_data_prep.py: The lastfm playlist data are cleaned up and prepared.  Artist names are reconciled between the two datasets.
app.R: This is where the shiny app was created.  The app displays a map and recommendations are continuously updated based on the location shown in the map.
