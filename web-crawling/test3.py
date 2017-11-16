# 인터넷 기사 댓글 가져오기 test_lab

from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time     # 웹 페이지 로딩 시 시간 딜레이가 필요
from konlpy.tag import Twitter
from collections import Counter

# 웹페이지에 바로 request를 보내는 방식이 아닌 컴퓨터 상의 램에 headless browser를 띄워서 browser를 조정해 데이터를 주고 받는 방법
# http://www.edaily.co.kr/news/news_detail.asp?newsId=02699446616091608&mediaCodeNo=257&OutLnkChk=Y


# 매개변수 : 기사 URL, 댓글 html태그 이름, 댓글 태그 속성, 댓글 태그 속성 명, 댓글 더보기 버튼이 있는경우 더보기 버튼 태그 속성명
def getCommentFromURL(url, tagName, attrType, attrName, moreButton) :
    try :
        driver = webdriver.PhantomJS()  # 브라우저를 킴
        driver.get(url)      # 매개변수 URL로 웹페이지를 이동
        time.sleep(3)       # 동적 웹페이지 요소들이 모두 로딩되기 위해 시간을 기다림

        """
         # more_button = driver.find_element_by_class_name(moreButton)  # 댓글 '더보기' 버튼이 있는지 확인하기 위한 변수
        while more_button:      # 더보기 버튼이 존재하면 계속 댓글의 끝까지 버튼을 클릭한다.
            print('button yes')
            click = more_button.click()
            time.sleep(3)
        """


        # tmp = driver.find_elements_by_class_name("txt_cont")
        # tmp2 = driver.find_element_by_tag_name("div")

        page = bs(driver.page_source, 'html.parser')    # driver 객체를 BeautifulSoup와 연계 사용
        page.prettify()         # html페이지 코드를 깔끔하게 정리

        """
        # more_button = page.find('a', attrs={'class' : 'u_cbox_btn_more'})
        print(more_button)
        more_button.click()
        """

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


# 매개변수 : 단어를 추출할 문장, 추출할 최대 단어 갯수
def getKeyword(text, ntags=50) :
    spliter = Twitter()             # konlpy의 Twitter객체
    nouns = spliter.nouns(text)     # nouns 함수를 통해 text에서 명사만 추출
    count = Counter(nouns)
    return_list = []                # 배열

    # most_common 메소드는 정수를 입력받아 객체 안의 명사중 빈도수
    # 큰 명사부터 순서대로 입력받은 정수 갯수만큼 저장되어있는 객체 반환
    # 명사와 사용된 갯수를 return_list 배열에 저장
    for n, c in count.most_common(ntags):
        temp = {'tag' : n, 'count' : c }     # tag : 단어, count : 빈도 수
        return_list.append(temp)

    return return_list


def main():
    url = 'http://news.naver.com/main/read.nhn?oid=001&sid1=102&aid=0009685173&mid=shm&viewType=pc&mode=LSD&nh=20171115120651'
    comment = getCommentFromURL(url, 'span', 'class', 'u_cbox_contents', 'u_cbox_btn_more')

    print(comment)

    keyword = getKeyword(comment,100)

    print(keyword)

if __name__ == '__main__':
    main()


