import pandas as pd
import links_scraper
from bs4 import BeautifulSoup
import requests
import re
import time
import random
import matplotlib.pyplot as plot
import matplotlib as mpl

#need to make custom functions to operate on my data
#
# 
# ONLY NEED MORE THAN 1!!!

#function 1: gets total views of MVs in the Top 300 K-Pop MVs by Artist (i.e. add total views by artists in my dataset)
#function 2: calculates average # of total yearly views for each Artist (based on MVs in the Top 300) -- use mean function on yearlyViews df

#need to make a requirements txt

#need to make plots
#plot 1: bar chart of artists w/ top 10 average # of views per video per year 
#link: https://datatofish.com/line-chart-python-matplotlib/
#plot 2: line chart total views by year for the artist w/most total views across mvs in the top 300 & time (years)
#figure out formatting to get numbers w/commas


def getArtistName(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    backToLink = soup.find(href=re.compile("/artist/")).text
    artistName = backToLink[8:]
    
    return artistName

def getYears(annualViews_df):
    yearCount = []
    for i in range(len(annualViews_df)):
        yearCount.append(i+1)
    return yearCount

#Cleaning up Views (original data has views written like this for example: "~100,000")
#need Views in an acceptable format with type int to perform mathematical operations on the data
def convertViewsToInt(annualViews_df):
    viewsPerYear = []
    for i in range(len(annualViews_df)):
        viewsPerYr_str = annualViews_df.loc[i, 'Views (string)']
        viewsPerYr_int = int(viewsPerYr_str[1:].replace(',', ''))
        viewsPerYear.append(viewsPerYr_int)
    return viewsPerYear

#Calculates the Total Views of the MV by Year
def calculateTotalViews(viewsPerYear):
    totalViews = []
    for i in range(len(viewsPerYear)):
        if i == 0:
            totalViews.append(viewsPerYear[i])
        else:
            totalViews.append((totalViews[i-1] + viewsPerYear[i]))
    return totalViews

def getAnnualViewInfo(url):
    annualViews_df = pd.read_html(url)[1]
    annualViews_df.rename(columns={"Views":"Views (string)"}, inplace=True)

    cleanAnnualViews_df = pd.DataFrame()
    #adds Year and Year Count to new clean Annual Views dataframe
    cleanAnnualViews_df['Year'] = list(annualViews_df['Year'])
    cleanAnnualViews_df['Year Count'] = getYears(annualViews_df)

    #cleans up Views from original df/converts Views to int
    viewsPerYear = convertViewsToInt(annualViews_df)
    cleanAnnualViews_df['Annual Views'] = viewsPerYear

    #calculates Total Views per year
    cleanAnnualViews_df['Total Views'] = calculateTotalViews(viewsPerYear)
    return cleanAnnualViews_df

def getViews():
    allVideoViewLinks_df = links_scraper.scrapeURLS("https://kworb.net/youtube/topvideos_korean.html")
    videoViewLinks_df = allVideoViewLinks_df.iloc[:100,:]
    videoViews_df = pd.DataFrame(columns=['MV Name', 'Artist', 'Year', 'Year Count', 'Annual Views', 'Total Views'])

    for i in range(len(videoViewLinks_df)):
        time.sleep(random.randint(0,3))
        
        mvName = videoViewLinks_df.at[i, 'Video']
        
        videoViewsURL = videoViewLinks_df.at[i, 'Link']
        artist = getArtistName(videoViewsURL)

        annualViews_df = getAnnualViewInfo(videoViewsURL)
        for i in range(len(annualViews_df)):
            year = annualViews_df.at[i, 'Year']
            yearCount = annualViews_df.at[i, 'Year Count']
            viewsPerYear = annualViews_df.at[i, 'Annual Views']
            totalViews = annualViews_df.at[i, 'Total Views']
            videoViews_df.loc[len(videoViews_df.index)] = [mvName, artist, year, yearCount, viewsPerYear, totalViews]
    
    return videoViews_df

def calculateArtistTotalViews(artists, videoViews_df):
    viewsByArtist = []
    for i in range(len(artists)):
        viewsByArtist.append(videoViews_df.loc[videoViews_df['Artist'] == artists[i], 'Annual Views'].sum())
    return viewsByArtist

def calculateArtistYrlyAvgViews(artists, videoViews_df):
    yearlyAvgViews = []
    for i in range(len(artists)):
        maxYrCount = videoViews_df.loc[videoViews_df['Artist'] == artists[i], 'Year Count'].max()
        avgViewsPerYr = 0
        for a in range(maxYrCount-1):
            avgViewsPerYr += videoViews_df.loc[(videoViews_df['Artist'] == artists[i]) & (videoViews_df['Year Count'] == (a+1)), 'Annual Views'].mean()
        yearlyAvgViews.append((avgViewsPerYr // maxYrCount))
    return yearlyAvgViews

def getViewsByArtist(videoViews_df):
    topArtistViews_df = pd.DataFrame(columns=['Artist', 'Total Views', 'Avg Yearly Views'])
    topArtists = list(videoViews_df['Artist'].unique())
    topArtistViews_df['Artist'] = topArtists
    topArtistViews_df['Total Views'] = calculateArtistTotalViews(topArtists, videoViews_df)
    topArtistViews_df['Avg Yearly Views'] = calculateArtistYrlyAvgViews(topArtists, videoViews_df)

    return topArtistViews_df

def displayArtistAvgViews(yrlyAvg_df):
    sortedYrlyAvg_df = yrlyAvg_df.sort_values(by='Avg Yearly Views', ascending=False)
    topArtistsAvgViews_df = sortedYrlyAvg_df.iloc[:10,:]
    ax = topArtistsAvgViews_df.plot.bar(x="Artist", y="Avg Yearly Views", rot =70)
    plot.xlabel("Artist", size=15)
    plot.ylabel("Average Yearly Views", size=15)
    plot.title("Average Yearly Views on Top 300 Kpop MVs by Artist", size=20)
    plot.ticklabel_format(style='plain', axis='y')
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

    plot.show(block=True)

def displayMostViewedArtist(artist, yearlyViews_df):
    ax = yearlyViews_df.plot(x='Year', y='Total Views')
    plot.xlabel('Year', size=15)
    plot.ylabel('Total Views', size=15)
    title = 'Total Views Over Time for Most Viewed K-Pop Artist - ' + artist
    plot.title(title, size=20)
    plot.ticklabel_format(style='plain', axis='y')
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    
    plot.show(block=True)

def mostViewedArtist(topViewedByArtist_df, allVideoViews_df):
    sortedTopViewedArtist_df = topViewedByArtist_df.sort_values(by='Total Views', ascending=False)
    mostViewedArtist = sortedTopViewedArtist_df.at[0, 'Artist']

    year = allVideoViews_df.loc[allVideoViews_df['Artist'] == mostViewedArtist, 'Year'].min()
    topArtistViews_df = pd.DataFrame(columns=['Year', 'Total Views'])
    while year <= 2023:
        annualTotalViews = allVideoViews_df.loc[(allVideoViews_df['Artist'] == mostViewedArtist) & (allVideoViews_df['Year'] == year), 'Total Views'].sum()
        topArtistViews_df.loc[len(topArtistViews_df.index)] = [year, annualTotalViews]
        year += 1
    
    displayMostViewedArtist(mostViewedArtist, topArtistViews_df)
    

topVideoViews_df = getViews()
topArtistViews_df = getViewsByArtist(topVideoViews_df)
displayArtistAvgViews(topArtistViews_df)
mostViewedArtist(topArtistViews_df, topVideoViews_df)
