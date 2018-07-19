library(shiny)
library(leaflet)
library(htmltools)

# Here is input list for testing the functions
# input <- list(
# 	artistname="Rodney Atkins", 
# 	map_bounds=data.frame(south=32.91677,north=46.37749,east=-82.70731,west=-108.635)
# )

## Read in all the data
user_df = read.csv("user_df.csv")
item_df = read.csv("item_df.csv")
load("venue_rank_list.RData")
locations = read.csv("venue_location.csv")
artistname_list = as.character(user_df$user)
locations$city_state = paste(locations$city,locations$state,sep=", ")

artistname_lower = tolower(artistname_list)
artistname_lower[547] = "Nothing"
names(venue_rank_list) = artistname_lower

## Set up the user interface
ui <- fluidPage(
  h2("StageFinder",align = "center"),
  h4("A venue recommendation system for bands",align = "center"),
  #h5(""),
  sidebarPanel(
    textInput("artistname", label = h5("Enter your band name and we will recommend some venues that are 
                                       suited to your musical style and fanbase"), value = ""),
    
    # Change to select input for testing
    #selectInput(inputId = "artistname", label=h5("Enter Artist Name"), selected = artistname_list[1],
    #	choices = artistname_list)
    #h5("Based on the selected area, here are the top 10 recommended venues for you"),
    tableOutput("table")
    ),
  mainPanel(
    leafletOutput("map")
  )
  
)

## Set up the dyanmic server component
server <- function(input, output) {
  
  #artistname = input$artistname (keep input as is)
  
  output$map <- renderLeaflet({
    leaflet() %>% setView(lng = -95, lat = 38, zoom = 4) %>% addTiles()
  }) 
  
  PointsInBounds <- reactive({
    
    # Require artist name input (MG)
    req(input$artistname)
    
    if (is.null(input$map_bounds)){
      
      rec_venue = NULL
      return(rec_venue)
      
    } else {
      
      if (input$artistname %in% artistname_list){
        
        bounds = input$map_bounds
        
        artist = tolower(input$artistname)
        reclist = venue_rank_list[[artist]]
        artist_venues = item_df[reclist,]
        colnames(artist_venues) = c("venue","id")
        locations_sub = locations[match(artist_venues$venue,locations$venue),]
        artist_venues = data.frame(artist_venues,locations_sub[,2:8])
        artist_venues = na.omit(artist_venues)
        
        recvals_filt = artist_venues[which(artist_venues$lat>=bounds$south&artist_venues$lat<=bounds$north),]
        recvals_filt = recvals_filt[which(recvals_filt$lon<=bounds$east&recvals_filt$lon>=bounds$west),]
        
        rec_venue = recvals_filt[1:10,]
        rec_venue = na.omit(rec_venue)
        
        return(rec_venue)
        
      } else {
        
        rec_venue = NULL
        return(rec_venue)
      }  
    }
  })
  
  ## Create the dynamic map
  observe({
    req(PointsInBounds())
    if(nrow(PointsInBounds())>0 & !is.null(PointsInBounds())){
      leafletProxy("map", data=PointsInBounds()) %>% clearMarkers() %>%
        addMarkers(lng = ~lon, lat = ~lat, label = ~htmlEscape(vname))
    }
  })
  
  ## Create the dynamic data frame
  observe({
    req(PointsInBounds())
    table_show = data.frame("Venue" = PointsInBounds()$vname,"City" = PointsInBounds()$city_state)
    output$table <- renderTable({
      table_show
    })
  })
  
}

shinyApp(ui, server)

#rsconnect::deployApp("~/Documents/Shiny/StageFinder_v2")


