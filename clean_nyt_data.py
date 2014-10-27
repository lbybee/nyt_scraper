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


def fastLoad(f_list):
    """loads all the files and removes the duplicates quickly"""

    data_list = []
    t_1 = datetime.now()
    for i, f in enumerate(f_list):
        t_data = loadFile(f)
        data_list.extend(t_data)
        data_list = [dict(r) for r in set([tuple(d.items()) for d in data_list])]
        print i, datetime.now() - t_1, "removing duplicates..."
    print "Done removing duplicates."
    return data_list




def fullLoad(f_list):
    """fully loads a file and makes it into a dictionary"""

    t_1 = datetime.now()

    id_list = []
    data_dict = {}

    for i, f in enumerate(f_list):
        
        i_t_1 = datetime.now()

        r_f = open(f, "rb")
        r_data = r_f.read().split("\n")

        ln_r_data = len(r_data)

        for j, r in enumerate(r_data[:-1]):
            j_r = json.loads(r)
            if j_r["_id"] not in id_list:
                id_list.append(j_r["_id"])
                date = datetime.strptime(j_r["pub_date"][0:10], "%Y-%m-%d")
                if date not in data_dict:
                    data_dict[date] = ""
                data_dict[date] += " %s" % j_r["lead_paragraph"]
                print (j * 100.) / ln_r_data, datetime.now() - t_1, datetime.now() - i_t_1, i 
    return data_dict


def loadAllFiles(f_list):
    """iterates through all the files in the file list and gets
    the data"""

    t_1 = datetime.now()

    # first list
    i_list = []
    id_list = []
    for f in f_list:
        f_t = loadFile(f)
        i_list.extend(f_t)
    # clean list
    ln_i_list = len(i_list)
    c_list = []
    for i, f in enumerate(i_list):
        if f["id"] not in id_list:
            id_list.append(f["id"])
            c_list.append(f)
        print (i * 100.) / ln_i_list, datetime.now() - t_1, i
    return c_list



def cleanCList(c_list, decade_l):
    """cleans a list of files and splits into decade files"""

    ln_c_list = len(c_list)
    t_1 = datetime.now()
    decade_dict = {}
    for d in decade_l:
        decade_dict[d] = []
    for i, c in enumerate(c_list):
        c["date"] = c["date"].strftime("%Y-%m-%d")
        for d in decade_l:
            if d in c["date"]:
                decade_dict[d].append(c)
        print (i * 100.) / ln_c_list, datetime.now() - t_1
    for d in decade_l:
        output_f = open("clean_%s.json" % d, "wb")
        json.dump(decade_dict[d], output_f)


def fullCleanList(f_list, decade_l):
    """does the full cleaning"""

    data = fastLoad(f_list)
    cleanCList(data, decade_l)


def joinData(item_list):
    """takes in a list of news items and joins them by month"""

    t_1 = datetime.now()
    news_dict = {}
    ln_item_list = len(item_list)
    for i, r in enumerate(item_list):
        str_date = r["date"].strftime("%Y-%m")
        if str_date not in news_dict:
            news_dict[str_date] = ""
        news_dict[str_date] += " %s" % r["text"]
        print (i * 100.) / ln_item_list, datetime.now() - t_1
    return news_dict


def writeToMonthCsv(news_dict):
    """writes each date to its own file"""

    for k in news_dict:
        output_f = open(k + ".csv", "wb")
        writer = csv.writer(output_f)
        writer.writerow([news_dict[k].replace(",", "").encode("utf-8")])
        output_f.close()


def writeToCsv(news_dict, f_name):
    """writes a news dictionary to a csv"""

    f_data = open(f_name, "wb")
    writer = csv.writer(f_data)
    for k in news_dict:
        writer.writerow([k, news_dict[k].replace(",", "")])
    f_data.close()


def fullDecadeRun(f_list, decade_l):
    """takes in a file list and decade list and writes
    each decade to a monthly file"""

    data = fastLoad(f_list)
    data_dict = joinData(data)
    for d in decade_l:
        d_dict = {}
        d_f = "monthly_%s.csv" % d
        for t_d in data_dict:
            if d in t_d:
                d_dict[t_d] = data_dict[t_d]
        writeToCsv(d_dict, d_f)


def fullRunAll(f_list):
    """does everything"""

    data = fastLoad(f_list)
    data_dict = joinData(data)
    writeToMonthCsv(data_dict)
