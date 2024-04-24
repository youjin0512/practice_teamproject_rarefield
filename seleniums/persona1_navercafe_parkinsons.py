from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
webbrowser_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(webbrowser_manager_directory))
# Chromebrowser 실행
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException    # Element : 웹요소 찾지 못할 때 / Window : 창이 없거나 찾을 수 없을 때
# Chrome Webbrowser의 capabilities 속성 사용
capabilities = browser.capabilities
from selenium.webdriver.common.by import By
from selenium import webdriver

# Chromebrowser 실행
# from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException    # Element : 웹요소 찾지 못할 때 / Window : 창이 없거나 찾을 수 없을 때

# - 정보 획득
# from selenium.webbrowser.support.ui import Select      # Select : dropdown 메뉴 다루는 클래스
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

## dbmongo의 collection 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://trainings.iptime.org:48001/")
# database 연결
database = mongoClient["data_analysis"]
# collection 작업
collection = database['persona1_navercafe_parkinsons']
# 로그인 창
# browser.switch_to.frame('cafe_main')

# 로그인 창
browser.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
time.sleep(2)

##############################
##############################

#자바스크립트로 우회하여 아이디와 비밀번호 값 넘겨줌
browser.execute_script("document.getElementsByName('id')[0].value = \'" + my_id + "\'") 
browser.execute_script("document.getElementsByName('pw')[0].value = \'" + my_pw + "\'")

browser.find_element(by=By.CSS_SELECTOR, value='.btn_login').click() #로그인 버튼 클릭
time.sleep(1)

browser.get('https://cafe.naver.com/parkinson777') # 네이버 카페 접속(파킨슨병)
time.sleep(1)

browser.find_element(by=By.CSS_SELECTOR, value='#menuLink3').click() # 자유로운글 게시판 클릭
# #group9 > li:nth-child(3)
time.sleep(1)


browser.switch_to.frame('cafe_main') #프레임 전환
time.sleep(1)

browser.find_element(by=By.CSS_SELECTOR, value='#main-area > div:nth-child(4) > table > tbody > tr:nth-child(1) > td.td_article > div.board-list > div > a.article').click() # 게시글 클릭
time.sleep(1)


for i in range(100):
    try:
        title=browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleContentBox > div.article_header > div.ArticleTitle > div > h3').text # 글 제목 추출
        name=browser.find_element(by=By.CSS_SELECTOR, value='.nickname').text #작성자 추출
        date=browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleContentBox > div.article_header > div.WriterInfo > div.profile_area > div.article_info > span.date').text #작성일 추출
        contents=browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleContentBox > div.article_container > div.article_viewer > div > div.content.CafeViewer > div > div').text #글내용 추출
        
        
        # 댓글 영역 가져오기(리스트로 몽고db에 업로드)
        try:
            review = browser.find_elements(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > ul')  # 댓글 영역
            review_contents = browser.find_element(by=By.CSS_SELECTOR, value='div > div > div.comment_text_box > p > span')  # 댓글내용
        except:
            pass
        
        # print('<',i+1,'번째 글> : ',title)
        # print(title, name, date, contents)
        # print('')
        
        # data={
        #     'cafe' : '파킨슨병',  # 카페 이름
        #     'title' : title,
        #     'name' : name,
        #     'date' : date,
        #     'contents' : contents,
        #     'review' : review_contents
        # }
            
        # collection.insert_one(data)
        # # browser.find_element(by=By.CSS_SELECTOR, value='a.BaseButton.btn_next').click() #다음글 버튼 클릭
        # # time.sleep(3)
        
        
    
    except :
        pass
        # try:
        #     title=browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleContentBox > div.article_header > div.ArticleTitle > div > h3').text #글제목 추출
        #     name=browser.find_element(by=By.CSS_SELECTOR, value='.nickname').text #작성자 추출
        #     date=browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleContentBox > div.article_header > div.WriterInfo > div.profile_area > div.article_info > span.date').text #작성일 추출
        #     contents=browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleContentBox > div.article_container > div.article_viewer > div > div.content.CafeViewer > div > div').text #글내용 추출
        # except:
        #    contents= ""
        
        # collection.insert_one(data)
        
        # browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleTopBtns > div.right_area > a.BaseButton.btn_next.BaseButton--skinGray.size_default').click() #다음글 버튼 클릭


    browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleTopBtns > div.right_area > a.BaseButton.btn_next.BaseButton--skinGray.size_default').click() #이전글 옆다음글 버튼 클릭
    time.sleep(3)    
    
    data={
    'cafe' : '파킨슨병',  # 카페 이름
    'title' : title,
    'name' : name,
    'date' : date,
    'contents' : contents,
    'review' : review_contents
    }
        
    collection.insert_one(data)
    # browser.find_element(by=By.CSS_SELECTOR, value='a.BaseButton.btn_next').click() #다음글 버튼 클릭
    # time.sleep(3)    
        

browser.close()