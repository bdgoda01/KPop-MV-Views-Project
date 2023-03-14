import pandas as pd

#need to make custom functions to operate on my data
#function 1: gets the year w/lowest view increase
#function 2: gets total views by artist by year
#function 3: gets the year w/highest view increase
#function 4: gets the music video w/highest view increase in a year
#function 5: gets the artist w/highest view increase in a year

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

yearlyViews_df["Views"] = 0
monthlyViews_df["Views"] = 0

yearlyViews_years = []
yearlyViews_viewsDiff = []
yearlyViews_yearCount = []
yearlyViews_viewTotal = []

#turn this into a function to meet project requirements!

for i in range(len(yearlyViews_df)):
    yearlyViews_yearCount.append(i+1)
    yearlyViews_years.append(yearlyViews_df.loc[i, "Year"])
    yrViews_str = yearlyViews_df.loc[i, "Views (string)"]
    yrViews_int = int(yrViews_str[1:].replace(',',''))
    yearlyViews_viewsDiff.append(yrViews_int)
    if i == 0:
        yearlyViews_viewTotal.append(yrViews_int)
    else:
        yearlyViews_viewTotal.append((yearlyViews_viewTotal[i-1] + yrViews_int))


cleanYearlyViews_df = pd.DataFrame({"Year": yearlyViews_years, "Approx. Total Views": yearlyViews_viewTotal, "Approx. Views Increase": yearlyViews_viewsDiff}, index=yearlyViews_yearCount)
cleanYearlyViews_df.rename_axis("Year Count", inplace=True)
print(cleanYearlyViews_df)

""" for i in range(12):
    mthViews_str = monthlyViews_df.loc[i, "Views (string)"]
    monthlyViews_df.loc[i, "Views"] = int(mthViews_str[1:].replace(',',''))

print(yearlyViews_df.head()) """