from datetime import datetime, timedelta
import requests
import json
import time


def daterange(s_date, e_date):
    for n in range(int ((e_date - s_date).days)):
        yield s_date + timedelta(n)


def getRes(url, params):
    """gets the results from requests, this is its own function to prevent
    errors"""

    try:
        res = requests.get(url, params=params)
    except Exception as e:
        print 1, e
        time.sleep(6)
        try:
            res = requests.get(url, params=params)
        except Exception as e:
            print 2, e
            time.sleep(30)
            try:
                res = requests.get(url, params=params)
            except Exception as e:
                print 3, e
                time.sleep(300)
                res = requests.get(url, params=params)
    return res


def downloadDateRange(s_date, e_date, o_file, api_key):
    """downloads data in the date range"""

    # intialize start time
    t_1 = datetime.now()
    # normally I would just use strftime("%Y%m%d") but because we want
    # to get dates before 1900 strftime doesn't work, that's pretty stupid
    # but this is a "fix"
    str_s_date = s_date.isoformat().split("T")[0].replace("-", "")
    str_e_date = e_date.isoformat().split("T")[0].replace("-", "")
    log_f = open("log.txt", "ab")

    for d in daterange(s_date, e_date):
        # make string date for the request
        str_date = d.isoformat().split("T")[0].replace("-", "")
        # initalize the max page for the while loop, this will be updated
        # as you iterate through the pages, the initalized value is arbitrary
        # but greater than 0 or stp
        mx_pg = 1
        stp = 0
        while(stp <= mx_pg):
            url = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
            params={"begin_date": str_date,
                    "end_date": str_date,
                    "page": stp,
                    "api-key": api_key}
            res = getRes(url, params)
            try:
                res_json = json.loads(res.text)["response"]
                # update the mx_pg using the number of hits returned
                mx_pg = res_json["meta"]["hits"] / 10
                # now get the actual data, iterate through the articles
                for a in res_json["docs"]:
                    with open(o_file, "a") as o_data:
                        json.dump(a, o_data)
                        o_data.write("\n")
                print datetime.now() - t_1, str_date, str_s_date, str_e_date, stp, mx_pg
                log_f.write("%s, %s, %s, %s, %s, %s\n" % (str(datetime.now() - t_1), str_date,
                                                          str_s_date, str_e_date, str(stp),
                                                          str(mx_pg)))
            except Exception as e:
                print e
                log_f.write("%s\n" % e)
            stp += 1
            time.sleep(8.7)
