library(shiny)
library(leaflet)
library(htmltools)

#setwd("~/Documents/Shiny/StageFinder")
setwd("~/Documents/Insight/Insight_project/Data")

#locations = read.csv("venue_location_df.csv")

user_df = read.csv("user_df.csv")
item_df = read.csv("item_df.csv")
pred = read.csv("mod_pred.csv")
colnames(pred) = 1:ncol(pred)
rownames(pred) = user_df$user

artistnames = as.character(user_df$user)

venue_vals_list = list()
venue_rank_list = list()

for(i in 1:length(artistnames)){
  if(i%%100==0) print(i)
  artistname = artistnames[i]
  pred_row = pred[artistname,]
  pred_row = pred_row[which(pred_row>0)]
  pred_row = pred_row[order(pred_row,decreasing=T)]
  venue_vals_list[[i]] = pred_row
  venue_rank_list[[i]] = as.numeric(names(pred_row))
}

setwd("~/Documents/Shiny")
save(venue_vals_list,file="venue_vals_list.RData")
save(venue_rank_list,file="venue_rank_list.RData")

