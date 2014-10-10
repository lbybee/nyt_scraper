import json
import csv
from datetime import datetime


def loadFile(f_name):
    """loads the data from the file and takes the key stuff"""

    r_f = open(f_name, "rb")
    r_data = r_f.read().split("\n")
    rj_data = [json.loads(r) for r in r_data[:-1]]
    rjf_data = [{"text": r["lead_paragraph"],
                 "date": datetime.strptime(r["pub_date"][0:10], "%Y-%m-%d"),
                 "id": r["_id"]}
                for r in rj_data]
    rjf_data = [r for r in rjf_data if r["text"] is not None]
    return rjf_data


def loadAllFiles(f_list):
    """iterates through all the files in the file list and gets
    the data"""

    # first list
    i_list = []
    id_list = []
    for f in f_list:
        f_t = loadFile(f)
        i_list.extend(f_t)
    # clean list
    c_list = []
    for f in i_list:
        if f["id"] not in id_list:
            id_list.append(f["id"])
            c_list.append(f)
    return c_list


def joinData(item_list):
    """takes in a list of news items and joins them by month"""

    news_dict = {}
    for r in item_list:
        str_date = r["date"].strftime("%Y%m")
        if str_date not in news_dict:
            news_dict[str_date] = ""
        news_dict[str_date] += " %s" % r["text"]
    return news_dict


def writeToCsv(news_dict, f_name):
    """writes a news dictionary to a csv"""

    f_data = open(f_name, "wb")
    writer = csv.writer(f_data)
    for k in news_dict:
        writer.writerow([k, news_dict[k].replace(",", "")])
    f_data.close()
