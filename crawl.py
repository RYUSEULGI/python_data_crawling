from os import read
import urllib.request
import json
import numpy as np


def getKeywordList(data):
    NATEKEYWORDAPI = "https://news.nate.com/today/keywordList"

    request = urllib.request.Request(NATEKEYWORDAPI)
    response = urllib.request.urlopen(request)

    rescode = response.getcode()

    if(rescode == 200):
        result = json.loads(response.read())
        for i in range(10):
            idx = str(i)
            data.append([{"keyword_dtm": result['data'][idx]['keyword_dtm'],
                         "keyword_sq": result['data'][idx]['keyword_sq'],
                          "keyword_name": result['data'][idx]['keyword_name'],
                          "score": result['data'][idx]['score'],
                          "mod_dtm": result['data'][idx]['mod_dtm'],
                          "create_dtm": result['data'][idx]['create_dtm']}])
        return data
    else:
        print("ERROR CODE :" + rescode)


def getNewsList(data):

    for i in range(10):

        sliceDtm = data[i][0]['keyword_dtm'][0:10]
        sliceDtm2 = data[i][0]['keyword_dtm'][11:19]
        keyword_sq = data[i][0]['keyword_sq']

        NATELISTAPI = f"https://news.nate.com/today/articleList?keyword_dtm={sliceDtm}%20{sliceDtm2}&keyword_sq={keyword_sq}"

        request = urllib.request.Request(NATELISTAPI)
        response = urllib.request.urlopen(request)

        rescode = response.getcode()

        if(rescode == 200):
            result = json.loads(response.read())

            for j in range(5):
                idx = str(j)
                data[i][0]['search_cnt'] = result['search_cnt']
                data[i][0]['search_link'] = result['search_link']
                data[i][0]['artc_title_' + idx] = result['data'][idx]['artc_title']
                data[i][0]['img_url_' + idx] = result['data'][idx]['img_url']
                data[i][0]['link_url_' + idx] = result['data'][idx]['link_url']
            return data
        else:
            print("ERROR CODE :" + rescode)


def getTxtFile(fname, data):

    with open(fname + '.txt', 'w', newline='', encoding='utf8') as f:
        length = len(data)
        w = csv.writer(f)
        w.writerow(data[0][0].keys())
        print(data[0][0].keys())

        for i in range(length):
            w.writerow(data[i][0].values())


data = []
getKeywordList(data)
getNewsList(data)
getTxtFile("nate_today_news", data)
