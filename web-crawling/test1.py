from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
import csv

def getFinancialRatioUS(symbol, item):
    try:
        url = r'http://finviz.com/quote.ashx?t={}'.format(symbol.lower())   # query-string URL 사용가능. {}안에 symbol값이 들어간다.
        req = Request(url)
        html = urlopen(req).read()
        soup = bs(html, 'html.parser')
        pb = soup.find(text=item)   # 매개변수의 item값으로 웹페이지의 html태그 내 글자에서 찾는다.
        pb_ = pb.find_next(class_='snapshot-td2').text
        return pb_
    except Exception as e:
        print(e)

def getCommentFromURL():
    try:
        url2 = 'http://www.edaily.co.kr/news/news_detail.asp?newsId=02699446616091608&mediaCodeNo=257&OutLnkChk=Y'
        html = urlopen(url2)
        soup = bs(html, 'lxml')
        pb = soup.find('div', attrs={'class': 'txt_cont'})
        pb_ = pb.find_next(class_='snapshot-td2').text
        return pb_
    except Exception as e:
        print(e)


psr = getCommentFromURL()
print(psr)
