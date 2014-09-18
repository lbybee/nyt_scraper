from datetime import datetime
import nyt_scraper as nyt
import sys
import os

directory = sys.argv[1]
f_name = sys.argv[2]
api_key = sys.argv[3]
s_y = sys.argv[4]
s_m = sys.argv[5]
s_d = sys.argv[6]
e_y = sys.argv[7]
e_m = sys.argv[8]
e_d = sys.argv[9]


d1 = datetime(s_y, s_m, s_d, 1, 1)
d2 = datetime(e_y, e_m, e_d, 23, 59)

# update f_name with directory
f_name = os.path.join(directory, f_name)
nyt.downloadDateRange(d1, d2, f_name, api_key)
