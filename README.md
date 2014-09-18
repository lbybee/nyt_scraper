nyt_scraper
===========

This is a script I use for scraping articles from the New York Times for a given date range.  It includes three functions, **daterange**, **getRes**, and **downloadDateRange**.

# Functions

**daterange**(s_date, e_date)

This just produces a list of datetime objects that can be iterated over between the start and end date represented by s_date and e_date respectively.

**getRes**(url, params)

This is an internal function that makes the request to the API.  It is its own function to isolate the error checking from everything else.

**downloadDateRange**(s_date, e_date, o_file, api_key)

This is what does the majority of the work.  It takes in a starting date, and ending date, and output file and an API key.  I then iterates over all the dates between the start date and end date and gets all the articles for those dates.  To do that it first finds the number of articles for each date, calculate the total number of pages for the number of articles and iterates over all the pages to grab all the articles.  It will store each of the resulting json objects in the output file.  It just appends to the output file which isn't the cleanest way to store the data but does make the processes fairly resilient because if it goes down for any reason you can just pick up where you left off.

# Downloading the Data

To download the data you simply run the script, initialize the start and end date objects and run the **downloadDateRange** function on the date range.  As an example

        d1 = datetime(2013, 1, 1, 1, 1)
        d2 = datetime(2013, 2, 1, 1, 1)
        key = "apikeyhere"
        output = "01-02-2013.json"
        downloadDateRange(d1, d2, output, key)
        
This will then download all the articles form January to February of 2013 to the file "01-02-2013.json".  If the process crashes for any reason it can easily be restarted by replacing the start date by the last date that the **downloadDateRange** was able to reach.  This is made easy because for each article **downloadDateRange** prints the total run time, the current date, the starting date, the end date, the current page, and the total number of pages.

Alternatively, you could run the script download_nyt_data.py from the command line.  An example of this would be

        python download_nyt_data.py ../results 01-02-2013.json apikey 2013 1 1 2013 2 1
        
This would download the data to the results directory in the output file for all dates between January and February of 2013.
