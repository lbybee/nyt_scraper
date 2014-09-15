nyt_scraper
===========

This is a script I use for scraping articles from the New York Times for a given date range.  It includes three functions, '''daterange''', '''getRes''', and '''downloadDateRange'''.

# Functions

'''daterange'''(s_date, e_date)

This just produces a list of datetime objects that can be iterated over between the start and end date represented by s_date and e_date respectively.
