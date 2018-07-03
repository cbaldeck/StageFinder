'''Scrape the songkick website, grabbing concert information for all concerts
in the US over the past year.'''

from selenium import webdriver
from time import sleep
from random import randrange
from parsel import Selector
import pandas as pd

'''Functions to scrape out the concerts or festivals from one page of the 
songkick search results'''

def scrape_concerts():
    '''This function will go through a single page of the songkick search
    results, scrape out all the concerts, and return the info as a dataframe'''
    
    page_dates = []
    page_artists = []
    page_venues = []
    
    for j in range(1,11):
        
        ## Grab date, artist, and venue info
        Date = sel.xpath("/html/body/div[@class='container']/div[@class='row']/div[@class='col-8 primary']/div[@class='component search event-listings events-summary']/ul/li[@class='concert event']["+str(j)+"]/div[@class='subject']/p[@class='date']/strong/time/text()").extract()

        if Date == []:
            break
        
        Artist1 = sel.xpath("/html/body/div[@class='container']/div[@class='row']/div[@class='col-8 primary']/div[@class='component search event-listings events-summary']/ul/li[@class='concert event']["+str(j)+"]/div[@class='subject']/p[@class='summary']/a/strong/text()").extract()
        Artist2 = sel.xpath("/html/body/div[@class='container']/div[@class='row']/div[@class='col-8 primary']/div[@class='component search event-listings events-summary']/ul/li[@class='concert event']["+str(j)+"]/div[@class='subject']/p[@class='summary']/a/text()").extract()
        Venue = sel.xpath("/html/body/div[@class='container']/div[@class='row']/div[@class='col-8 primary']/div[@class='component search event-listings events-summary']/ul/li[@class='concert event']["+str(j)+"]/div[@class='subject']/p[@class='location']/text()").extract()
        
        ## Cleaning names
        Date = Date[0]
        Artist1 = Artist1[0]
        
        if Artist2[0] != ' ':
            Artist2 = Artist2[0]
            Artist = Artist1 + Artist2
        else:
            Artist = Artist1
        
        Venue = Venue[0].replace('\n','')
        Venue = Venue.strip()
        
        ## Attach data to list
        page_dates.append(Date)
        page_artists.append(Artist)
        page_venues.append(Venue)

    ## Create dataframe and return
    page_concert_df = pd.DataFrame({
        "date":page_dates,
        "isfest":0,
        "festival":"NA",
        "artist":page_artists,     
        "venue":page_venues})   
    
    return(page_concert_df)
    
    
    
def scrape_festivals():
    '''This function will go through a single page of the songkick search
    results, scrape out all the festivals, and return the info as a data frame'''

    page_dates = []
    page_festivals = []
    page_artists = []
    page_venues = []
    
    for j in range(1,11):
        
        ## Grab date, artist, and venue info
        Date = sel.xpath("/html/body/div[@class='container']/div[@class='row']/div[@class='col-8 primary']/div[@class='component search event-listings events-summary']/ul/li[@class='festival-instance event']["+str(j)+"]/div[@class='subject']/p[@class='date']/strong/time/text()").extract()
        
        if Date == []:
            break
        
        Festival = sel.xpath("/html/body/div[@class='container']/div[@class='row']/div[@class='col-8 primary']/div[@class='component search event-listings events-summary']/ul/li[@class='festival-instance event']["+str(j)+"]/div[@class='subject']/p[@class='summary']/a/strong/text()").extract()
        Artist = sel.xpath("/html/body/div[@class='container']/div[@class='row']/div[@class='col-8 primary']/div[@class='component search event-listings events-summary']/ul/li[@class='festival-instance event']["+str(j)+"]/div[@class='subject']/p[@class='summary']/a/text()").extract()
        Venue = sel.xpath("/html/body/div[@class='container']/div[@class='row']/div[@class='col-8 primary']/div[@class='component search event-listings events-summary']/ul/li[@class='festival-instance event']["+str(j)+"]/div[@class='subject']/p[@class='location']/text()").extract()
        
        ## Cleaning names
        Date = Date[0]
        Festival = Festival[0]
        Artist = Artist[1].replace('\n','')
        Artist = Artist.strip()
        Venue = Venue[0].replace('\n','')
        Venue = Venue.strip()
        
        ## Attach data to list
        page_dates.append(Date)
        page_festivals.append(Festival)
        page_artists.append(Artist)
        page_venues.append(Venue)
        
    ## Create dataframe and return    
    page_festival_df = pd.DataFrame({
        "date":page_dates,
        "isfest":1,
        "festival":page_festivals,
        "artist":page_artists,
        "venue":page_venues})   
    
    return(page_festival_df)


#########################################################################
     
'''Get songkick data for concerts occurring over the last year, in the US. 
Loop through the months, using these as the search terms in songkick.  
Songkick returns several thousand pages of concerts that occured in the 
requested month.  Adding "US" to the search query generally restricts the 
results to concerts in the United States (but isn't perfect).'''
    
months = ["june+2017+US","july+2017+US","august+2017+US","september+2017+US",
          "october+2017+US","november+2017+US","december+2017+US",
          "january+2018+US","february+2018+US","march+2018+US","april+2018+US",
          "may+2018+US"]

stem = "https://www.songkick.com/search?utf8=%E2%9C%93&type=initial&query="

concert_list = []
festival_list = []

for i in range(0,12):
    
    ## Create url for the search results
    month = months[i]
    month_main = stem + month
    print(month)

    ## Open url in chrome
    driver = webdriver.Chrome()
    driver.get(month_main)
    sel = Selector(text=driver.page_source)

    ## Scrape the first page
    page_concert_df = scrape_concerts()
    page_festival_df = scrape_festivals()
    
    concert_list.append(page_concert_df)
    festival_list.append(page_festival_df)
    
    ## Attempt to click to the next page, scrape content, and continue until
    ## there are no more pages.
    flag = 2
    while(flag > 0):
        
        print(flag)
        sleep(randrange(3, 5)) 
        
        try:
            click_button = driver.find_element_by_xpath("/html/body/div[@class='container']/div[@class='row']/div[@class='col-8 primary']/div[@class='component search event-listings events-summary']/div[@class='pagination']/a[@class='next_page']")
            click_button.click()
            
        except:
            flag = 0
            driver.close()    
            
        sel = Selector(text=driver.page_source)
            
        page_concert_df = scrape_concerts()
        page_festival_df = scrape_festivals()
            
        concert_list.append(page_concert_df)
        festival_list.append(page_festival_df)
            
        ## Periodically write to file in case of crash
        if flag % 10 == 0 :
            concert_df = pd.concat(concert_list)
            festival_df = pd.concat(festival_list)
    
            concert_df.to_csv('concert_df_US.csv',index=False)
            festival_df.to_csv('festival_df_US.csv',index=False)
                
        flag = flag + 1
     
## Final data gathering and writing to file                
concert_df = pd.concat(concert_list)
festival_df = pd.concat(festival_list)
    
concert_df.to_csv('concert_df_US.csv',index=False)
festival_df.to_csv('festival_df_US.csv',index=False)            
       
            