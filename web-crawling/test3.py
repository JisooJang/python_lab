# 인터넷 기사 댓글 가져오기 test_lab

from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time     # 웹 페이지 로딩 시 시간 딜레이가 필요

# 웹페이지에 바로 request를 보내는 방식이 아닌 컴퓨터 상의 램에 headless browser를 띄워서 browser를 조정해 데이터를 주고 받는 방법
# http://www.edaily.co.kr/news/news_detail.asp?newsId=02699446616091608&mediaCodeNo=257&OutLnkChk=Y



def getCommentFromURL(url, tagName, attrType, attrName) :
    try :
        driver = webdriver.PhantomJS()  # 브라우저를 킴
        driver.get(url)      # 매개변수 URL로 웹페이지를 이동
        time.sleep(3)       # 동적 웹페이지 요소들이 모두 로딩되기 위해 시간을 기다림

        more_button = driver.find_element_by_class_name('u_cbox_btn_more')      # 댓글 '더보기' 버튼이 있는지 확인하기 위한 변수

        while more_button:      # 더보기 버튼이 존재하면 계속 댓글의 끝까지 버튼을 클릭한다.
            print('button yes')
            more_button.click()
            time.sleep(3)

        # tmp = driver.find_elements_by_class_name("txt_cont")
        # tmp2 = driver.find_element_by_tag_name("div")

        page = bs(driver.page_source, 'html.parser')    # driver 객체를 BeautifulSoup와 연계 사용
        page.prettify()         # html페이지 코드를 깔끔하게 정리

        temp = page.find_all(tagName, attrs={attrType: attrName})
        # test case =>      temp = page.find_all('span', attrs={'span': 'u_cbox_contents'}
        comment_list = ''

        # more_button = page.find_all('a', attrs={'class': 'u_cbox_btn_more'})    # 댓글 '더보기' 버튼이 있는지 확인하기 위한 변수

        for tmp in temp :
            comment_list += tmp.get_text().strip() + '\n'

        return comment_list

    except Exception as e :
        print(e)

    finally :
        driver.close()


comment = getCommentFromURL('http://news.naver.com/main/hotissue/read.nhn?mid=hot&sid1=100&cid=1060622&iid=49624083&oid=437&aid=0000165578&ptype=052&m_view=1&includeAllCount=true&m_url=%2Fcomment%2Fall.nhn%3FserviceId%3Dnews%26gno%3Dnews437%2C0000165578%26sort%3Dlikability',
                            'span', 'class', 'u_cbox_contents')

print(comment)


