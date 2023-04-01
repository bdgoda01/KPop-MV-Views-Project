# KPop-MV-Views-Project
This python project analyzes the historical view counts of the Top 100 Viewed K-Pop music videos. It displays artists with the Top 10 highest Yearly Average View Count as well as the Total Views Growth of the KPop Artist with the most views. Using data from kworb.net, I built two web scrapers. The first gathers the Top 300 KPop music video titles and links to the webpage with detailed historical views of each video. The second scraper gathers the yearly views of each music video using the links from the first web scraper. The program then cleans up, analyzes, and displays the data. Instead of using a static file, I chose to build the web scrapers so that as views increase on videos, the program can be run at any point in time and will reflect the latest view counts.

#Required Packages
The required packages needed to run this project are listed in requirements.txt 

#Project Requirements/Features
1. Scrape data from anywhere on the internet
2. Use custom functions to perform specific operations to clean or manipulate the data
3. Write custom functions to operate on the data (I also used basic calculations with Pandas and built-in Python functions)
4. Make 2 basic plots with matplotlib
5. This README file

#Key Take Aways
Through this project, I learned that PSY is the most viewed KPop artist and, on average, gains the most views per year at the moment. Blackpink is a close second for average yearly view gains. Surprisingly, BTS is in 4th. The data may be more skewed towards artists with less music videos in the Top 100 as they would have less years with low yearly view increases, compared to artists with many music videos who have a higher chance of having many years with low yearly view increases.



