# Collect_naver_news.py  -박종원 2022.01.07-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from Article import Article
import re

class Collect_naver_news:
    #네이버 뉴스는 10분마다 새로고침 된다!!!
    options = Options()
    options.page_load_strategy = 'normal'
    chrome = webdriver.Chrome(options=options)
    url = "https://news.naver.com/"
    chrome.implicitly_wait(3) # 브라우저가 웹페이지전체를 로드할때까지 최대 3초 기다리게 설정

    CAT1_link_list = []
    CAT2_link_list = []

    @staticmethod
    def openURL(url :str = "https://news.naver.com/") -> None:  # 브라우저를 연다.
        Collect_naver_news.chrome.get(url) # 설정된 url로 브라우저를연다.
        Collect_naver_news.step_check = 0

    @staticmethod
    def set_CAT1_link() -> list:
        Collect_naver_news.openURL()
        politics = Collect_naver_news.chrome.find_element(By.LINK_TEXT, '정치').get_attribute('href')
        economy = Collect_naver_news.chrome.find_element(By.LINK_TEXT, '경제').get_attribute('href')
        society = Collect_naver_news.chrome.find_element(By.LINK_TEXT, '사회').get_attribute('href')
        life_culture = Collect_naver_news.chrome.find_element(By.LINK_TEXT, '생활/문화').get_attribute('href')
        it_sci = Collect_naver_news.chrome.find_element(By.LINK_TEXT, 'IT/과학').get_attribute('href')
        world = Collect_naver_news.chrome.find_element(By.LINK_TEXT, '세계').get_attribute('href')

        CAT1_link_list = [politics,economy,society,life_culture,it_sci,world]
        Collect_naver_news.step_check = 1
        Collect_naver_news.CAT1_link_list = CAT1_link_list

    @staticmethod
    def set_CAT2_link() -> list:
        if Collect_naver_news.CAT1_link_list == []:
            Collect_naver_news.set_CAT1_link()
        for CAT1 in Collect_naver_news.CAT1_link_list:
            Collect_naver_news.chrome.get(CAT1)   
            CAT2_list = Collect_naver_news.chrome.find_element(By.XPATH, '//*[@id="snb"]/ul').find_elements(By.TAG_NAME, 'a')
            # CAT2_link_list = []
            for CAT2 in CAT2_list:
                # CAT2_link_list.append(CAT2.get_attribute('href'))
                Collect_naver_news.CAT2_link_list.append(CAT2.get_attribute('href'))

            # Collect_naver_news.CAT2_link_list.append(CAT2_link_list)

        Collect_naver_news.step_check = 2

    @staticmethod
    def set_page_link() -> list:  # 현재 페이지의 링크는 미포함
        if Collect_naver_news.step_check != 2:
            Collect_naver_news.set_CAT2_link()
        page_link_list  = []
        while True:
            page_list = Collect_naver_news.chrome.find_element(By.XPATH, '//*[@id="main_content"]').find_element(By.CLASS_NAME, 'paging').find_elements(By.TAG_NAME, 'a')
            for page in page_list:
                page_link_list.append(page.get_attribute('href'))

            try:
                Collect_naver_news.chrome.find_element(By.LINK_TEXT, '다음')
                Collect_naver_news.openURL(page_link_list.pop(-1))
            except:
                break
        return page_link_list

    @staticmethod  # 작동하는 시점의 날부터 입력한(설정한) 일(day)수만큼 페이지를 넘기는 기능 -> 과거데이터 수집용(처음 한번만 사용할듯).
    def next_date(day :int) -> str:
        if Collect_naver_news.step_check != 2:
            Collect_naver_news.set_CAT2_link()

        # current_date = Collect_naver_news.chrome.find_element(By.CSS_SELECTOR, '#main_content > div.pagenavi_day > span.viewday')
        if day <= 0:
            print('0보다 큰 자연수를 입력하세요.')
            return
        next_day = Collect_naver_news.chrome.find_element(By.XPATH, '//*[@id="main_content"]/div[4]/a[1]')
        # next_day.click()
        yield next_day.get_attribute('href')

        day += -1
        if day == 0:
            return
            
        next_day = Collect_naver_news.chrome.find_element(By.XPATH, '//*[@id="main_content"]/div[4]/a[2]')
        # next_day.click()
        yield next_day.get_attribute('href')
        
        day += -1
        if day == 0:
            return
        
        while day > 0:
            next_day = Collect_naver_news.chrome.find_element(By.XPATH, '//*[@id="main_content"]/div[4]/a[3]')
            yield next_day.get_attribute('href')

    @staticmethod
    def read_one_page() -> list:
        if Collect_naver_news.step_check != 2:
            Collect_naver_news.set_CAT2_link()
         # 기사 리스트 정보를 얻어온다.
        news_list = Collect_naver_news.chrome.find_element(By.ID, 'main_content').find_element(By.CSS_SELECTOR, '#main_content > div.list_body.newsflash_body').find_elements(By.TAG_NAME, 'li')

        # Article개체를 담을 리스트를 준비한다.
        article_list = []

        for news in news_list:
            link = news.find_element(By.TAG_NAME, 'a').get_attribute('href')
            try:
                photo = news.find_element(By.CLASS_NAME, 'photo').get_attribute('src')
                title = news.find_elements(By.TAG_NAME, 'a')[-1].text
            except:
                photo = None
                title = news.find_element(By.TAG_NAME, 'a').text
            mediaCom = news.find_element(By.CLASS_NAME, 'writing').text
            category1 = Collect_naver_news.chrome.find_element(By.XPATH, '//*[@id="lnb"]').find_element(By.CLASS_NAME, 'on').find_element(By.CLASS_NAME, 'tx').text
            category2 = Collect_naver_news.chrome.find_element(By.XPATH, '//*[@id="snb"]/ul').find_element(By.CLASS_NAME, 'on').text
            # print(link,photo,title,mediaCom)
            temp = Article()
            temp.link = link
            temp.photo = photo
            temp.title = title
            temp.mediaCom = mediaCom
            temp.category1 = category1
            temp.category2 = category2
            article_list.append(temp)

        for article in article_list:
            Collect_naver_news.chrome.get(article.link)
            try:
                date = Collect_naver_news.chrome.find_element(By.CSS_SELECTOR, '#main_content > div.article_header > div.article_info > div > span').text
                content = Collect_naver_news.chrome.find_element(By.ID, 'articleBodyContents').text
                article.date = date
                article.content = content
            except:
                continue

        return article_list

    @staticmethod
    def update_all_cat_news_oneday() -> Article:
        if Collect_naver_news.CAT2_link_list == []:
            print('카테고리 항목이 없습니다.')
            return
                
        Collect_naver_news.openURL()
        for cat2 in Collect_naver_news.CAT2_link_list:
            Collect_naver_news.chrome.get(cat2)
            page_list = Collect_naver_news.set_page_link()
            Collect_naver_news.read_one_page_v2()
            for page in page_list:
                Collect_naver_news.chrome.get(page)
                Collect_naver_news.read_one_page_v2()


    @staticmethod
    def read_news_one(link :str) -> None: # 기사 하나 정보얻기
        original_window = Collect_naver_news.chrome.current_window_handle
        temp = Article()

        try:
            temp.CAT1 = Collect_naver_news.chrome.find_element(By.CSS_SELECTOR, '#lnb > ul > li.on').text
            temp.CAT2 = Collect_naver_news.chrome.find_element(By.CCS_SELECTOR, '#snb > ul > li.on').text
            sid2 = re.compile('(sid2=)([0-9]*)')
            oid = re.compile('(odi=)([0-9]*)')
            temp.cd_id = link[sid2.search(link).start(2) : sid2.search(link).end(2)]
            temp.p_id = link[oid.search(link).start(2) : oid.search(link).end(2)]
        except:
            print('카테고리를 선택해주세요')
            temp.CAT1 = None
            temp.CAT2 = None     
            temp.cd_id = None
            temp.p_id = None

        Collect_naver_news.chrome.switch_to.new_window('tab')
        Collect_naver_news.chrome.get(link)

        temp.title	= Collect_naver_news.chrome.find_element(By.XPATH, '//*[@id="articleTitle"]').text
        temp.content	= Collect_naver_news.chrome.find_element(By.XPATH, '//*[@id="articleBodyContents"]').text  # ==> 요약본, 사진 정보를 삭제할것
        temp.photo	= Collect_naver_news.chrome.find_element(By.CSS_SELECTOR, '#articleBodyContents > span.end_photo_org').get_attribute('src')
        temp.date	= Collect_naver_news.chrome.find_element(By.XPATH, '//*[@id="main_content"]/div[1]/div[3]/div/span').text
        temp.originallink	=	Collect_naver_news.chrome.find_element(By.LINK_TEXT, '기사원문').get_attribute('href')

        Collect_naver_news.chrome.close()
        Collect_naver_news.chrome.switch_to.window(original_window)

        return temp

    @staticmethod
    def read_one_page_v2():
        if Collect_naver_news.step_check != 2:
            Collect_naver_news.set_CAT2_link()

        news_list = Collect_naver_news.chrome.find_element(By.ID, 'main_content').find_element(By.CSS_SELECTOR, '#main_content > div.list_body.newsflash_body').find_elements(By.TAG_NAME, 'li')

        for news in news_list:
            link = news.find_element(By.TAG_NAME, 'a').get_attribute('href')
            article = Collect_naver_news.read_news_one(link)
            yield article



if __name__ == "__main__" :
    # Collect_naver_news.set_CAT1_link()
    # print(Collect_naver_news.update_all_cat_news_oneday())
    # print(Collect_naver_news.read_news_one('https://news.naver.com/main/read.naver?mode=LS2D&mid=shm&sid1=101&sid2=259&oid=277&aid=0005027340'))
    # Collect_naver_news.test()
    Collect_naver_news.set_CAT2_link()
    for article in Collect_naver_news.update_all_cat_news_oneday():
        print(article.title)
