from os import read
import urllib.request
import json
import csv
from datetime import timedelta
from datetime import datetime
import smtplib
from email.message import EmailMessage

def sendMail(text):
    EMAIL_ADDRESS = 'mailAddress'
    EMAIL_PASSWORD = 'password'
    SEND_TO_EMAIL = 'mailAddress'

    msg = EmailMessage()

    msg['Subject'] = 'subject'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = SEND_TO_EMAIL
    msg.set_content(text)

    with smtplib.SMTP_SSL('smtp.xxxx.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def getKeywordList(data):

    date = datetime.now().date()            # 조회날짜
    now = datetime.now()                    # 현재시간
    delTime = now - timedelta(hours=1)      # 예) 14:29분 조회 -> 13:00 데이터 출력
    dataTime = delTime.strftime('%H:00')

    NATEKEYWORDAPI = f"https://news.nate.com/today/keywordList?service_dtm={date}%20{dataTime}:00"

    request = urllib.request.Request(NATEKEYWORDAPI)
    response = urllib.request.urlopen(request)

    rescode = response.getcode()

    # api에 이상이 없을 경우
    if(rescode == 200):
        result = json.loads(response.read())

        for i in range(10):
            idx = str(i)
            keyword = result['data'][idx]['keyword_service']

            # keyword_service에 br태그가 있는 경우 없애기
            if '<br />' in keyword:
                keyword = keyword.replace("<br />", " ")

            data.append([{"keyword_dtm": result['data'][idx]['keyword_dtm'],
                         "keyword_sq": result['data'][idx]['keyword_sq'],
                          "keyword_name": result['data'][idx]['keyword_name'],
                          "keyword_service": keyword,
                          "score": result['data'][idx]['score'],
                          "mod_dtm": result['data'][idx]['mod_dtm'],
                          "create_dtm": result['data'][idx]['create_dtm']}])
        return data
    else:
        print("ERROR CODE :" + rescode)


def getNewsList(data):

    for i in range(10):
        sliceDtm = data[i][0]['keyword_dtm'][0:10]      # 키워드 날짜
        sliceDtm2 = data[i][0]['keyword_dtm'][11:19]    # 키워드 시간대
        keyword_sq = data[i][0]['keyword_sq']

        NATELISTAPI = f"https://news.nate.com/today/articleList?keyword_dtm={sliceDtm}%20{sliceDtm2}&keyword_sq={keyword_sq}"

        request = urllib.request.Request(NATELISTAPI)
        response = urllib.request.urlopen(request)

        rescode = response.getcode()

        list = {}

        if(rescode == 200):

            result = json.loads(response.read())

            for j in range(5):
                idx = str(j)

                list['article_title_' + idx] = result['data'][idx]['artc_title']
                list['article_url_' + idx] = result['data'][idx]['link_url']
                list['article_img_' + idx] = result['data'][idx]['img_url']

                data[i][0]['article_cnt'] = result['search_cnt']
                data[i][0]['search_link'] = result['search_link']
                data[i][0]['article_list'] = list

        else:
            print("ERROR CODE :" + rescode)

    with open('nate_today.txt', 'w', newline='', encoding='utf8') as f:
        # with open('C:\ProgramData/MySQL/MySQL Server 8.0/Uploads/nate_today.txt', 'w', newline='', encoding='utf8') as f:
        length = len(data)
        w = csv.writer(f)
        w.writerow(data[0][0].keys())

        for i in range(length):
            w.writerow(data[i][0].values())

        print("done")


data = []

getKeywordList(data)
getNewsList(data)
