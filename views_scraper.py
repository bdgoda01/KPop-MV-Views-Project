import pandas as pd
import links_scraper
from bs4 import BeautifulSoup
import requests

#need to make custom functions to operate on my data
#
# 
# ONLY NEED MORE THAN 1!!!
#
#
#function 1: gets the year w/lowest view increase
#function 2: gets total views by artist by year
#function 3: gets the year w/highest view increase
#function 4: gets the music video w/highest view increase in a year
#function 5: gets the artist w/highest view increase in a year

#need to make a requirements txt

#need to make plots
#plot 1: line chart of top 5 most viewed kpop music videos for total views across time (years)
#link: https://datatofish.com/line-chart-python-matplotlib/
#plot 2: line chart total views by year for the artist w/most total views across mvs & time (years)
#add lines for top 3 mvs for that artist?
#figure out formatting to get numbers w/commas



url = "https://kworb.net/youtube/video/9bZkp7q19f0.html"
views_dfs = pd.read_html(url)
yearlyViews_df = views_dfs[1]
monthlyViews_df = views_dfs[2]

yearlyViews_df.rename(columns={"Views":"Views (string)"}, inplace=True)
monthlyViews_df.rename(columns={"Views":"Views (string)"}, inplace=True)

def yearlyViewCleanup(original_df):
    yearlyViews_years = []
    yearlyViews_viewsDiff = []
    yearlyViews_yearCount = []
    yearlyViews_viewTotal = []
    for i in range(len(original_df)):
        yearlyViews_yearCount.append(i+1)
        yearlyViews_years.append(original_df.loc[i, "Year"])
        yrViews_str = original_df.loc[i, "Views (string)"]
        yrViews_int = int(yrViews_str[1:].replace(',',''))
        yearlyViews_viewsDiff.append(yrViews_int)
        if i == 0:
            yearlyViews_viewTotal.append(yrViews_int)
        else:
            yearlyViews_viewTotal.append((yearlyViews_viewTotal[i-1] + yrViews_int))
    
    clean_df = pd.DataFrame({"Year": yearlyViews_years, "Approx. Total Views": yearlyViews_viewTotal, "Approx. Views Increase": yearlyViews_viewsDiff}, index=yearlyViews_yearCount)
    clean_df.rename_axis("Year Count", inplace=True)
    return clean_df

def getViews():
    videoViewLinks_df = links_scraper.scrapeURLS("https://kworb.net/youtube/topvideos_korean.html")
    videoViewInfo = {}
    for i in range(len(videoViewLinks_df)):
        videoRank = i + 1
        videoViewInfo[videoRank] = {}
        artist = 'PSY'
        mvName = 'Gangnam Style'
        totalViews = 4000000000
        yearlyViews = 1
        monthlyViews = 2
        videoViewInfo[videoRank]['artist'] = artist
        videoViewInfo[videoRank]['mvName'] = mvName
        videoViewInfo[videoRank]['totalViews'] = totalViews
        videoViewInfo[videoRank]['yearlyViews'] = yearlyViews
        videoViewInfo[videoRank]['monthlyViews'] = monthlyViews
    #for every url in videoViewLinks_df, make a new df with the yearlyViews, get the total view count from videoViewLinks_df, get the MVName from that df, get the artist name using bs4
    #returns a dictionary (index: {Artist: "artist name", MVName: "mv name", totalViews: #, YearlyViews: yearlyViews_df, MonthlyViews: monthlyViews_df })

cleanYearlyViews_df = yearlyViewCleanup(yearlyViews_df)



