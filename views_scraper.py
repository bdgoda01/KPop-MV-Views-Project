import pandas as pd

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