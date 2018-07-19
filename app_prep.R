## Earlier experimentation showed that the free tier of the shinyapps.io could not handle any large files (I had tried and
## failed to upload data which was about half GB in size).  So it is important to format the data to be as small as possible.  
## Instead of using the entire matrix of recommendation scores for each artist/venue combination, I put the data into a list 
## and store as an RData file.  

## The list only needs to contain the non-zero values for each artist.  I stored this two ways: 1) storing all the 
## non-zero values and the index of the venues they belong to, and 2) storing only the index of the venues in the order
## of recommendation.  The first option stored the data in about 6 MB and the second option stored the data in about 2 MB.
## I used the second option in the implementation of the app.

## Read in files
user_df = read.csv("user_df.csv")
item_df = read.csv("item_df.csv")
pred = read.csv("mod_pred.csv")

## Fix row and col names and variables
colnames(pred) = 1:ncol(pred)
rownames(pred) = user_df$user
artistnames = as.character(user_df$user)

## Create the two types of R lists that store the venue data for each artist
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

save(venue_vals_list,file="venue_vals_list.RData")
save(venue_rank_list,file="venue_rank_list.RData")
