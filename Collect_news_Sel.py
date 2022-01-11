# Collect_news_Sel.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from Article import Article

options = Options()
options.page_load_strategy = 'normal'
chrome = webdriver.Chrome(options=options)
url = "https://news.naver.com/"

chrome.implicitly_wait(3) # 브라우저가 웹페이지전체를 로드할때까지 최대 3초 기다리게 설정
chrome.get(url) # 설정된 url을 연다.

news_home = chrome.find_element(By.XPATH, '/html/body/section/header/div[1]/div/div/div[1]/div/h1/a/span') # 뉴스홈버튼을 지정한다.
economy = chrome.find_element(By.XPATH, '/html/body/section/header/div[2]/div/div/div[1]/div/div/ul/li[3]/a/span') # 경제버튼을 지정한다.
economy.click() # 경제버튼을 누른다.

finance = chrome.find_element(By.XPATH, '//*[@id="snb"]/ul/li[1]/a') # 금융 버튼을 지정한다.
finance.click() # 금융 버튼을 누른다.

# 기사 리스트 정보를 얻어온다.
news_list = chrome.find_element(By.ID, 'main_content').find_element(By.CSS_SELECTOR, '#main_content > div.list_body.newsflash_body').find_elements(By.TAG_NAME, 'li')

# Article개체를 담을 리스트를 준비한다.
article_list = []

for news in news_list:
    link = news.find_element(By.TAG_NAME, 'a').get_attribute('href')
    try:
        photo = news.find_element(By.CLASS_NAME, 'photo').text
        title = news.find_elements(By.TAG_NAME, 'a')[-1].text
    except:
        photo = None
        title = news.find_element(By.TAG_NAME, 'a').text
    mediaCom = news.find_element(By.CLASS_NAME, 'writing').text
    # print(link,photo,title,mediaCom)
    temp = Article()
    temp.link = link
    temp.photo = photo
    temp.title = title
    temp.mediaCom = mediaCom
    article_list.append(temp)

for article in article_list:
    chrome.get(article.link)
    date = chrome.find_element(By.CSS_SELECTOR, '#main_content > div.article_header > div.article_info > div > span').text
    content = chrome.find_element(By.ID, 'articleBodyContents').text
    article.date = date
    article.content = content
    