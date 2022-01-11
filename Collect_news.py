# Collect_news.py
#- 박종원 2022.01.11. -

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  # 이거 정보가 어디서 나온거지?
from selenium.webdriver.support.ui import WebDriverWait
from Article import Article
from NewsSql import NewsSql
from PressSql import PressSql

import re

class Collect_news:
    #네이버 뉴스는 10분마다 새로고침 된다!!!
    options = Options()
    # options.add_argument('headless') # 브라우저를 화면에 안띄운다.
    chrome = webdriver.Chrome(options=options)
    url = "https://news.naver.com/"
    chrome.implicitly_wait(3) # 브라우저가 웹페이지전체를 로드할때까지 최대 3초 기다리게 설정

    CAT2_link_list = []

    @staticmethod
    def openDriver(pick=None):
        ...
    
    @staticmethod
    def open_URL(url :str = None):
        if url == None:
            Collect_news.chrome.get(Collect_news.url)
        else:
            Collect_news.chrome.get(url)

    @staticmethod
    def set_CAT1() -> list:
        Collect_news.open_URL()
        CAT1_list = Collect_news.chrome.find_elements(By.CLASS_NAME, 'Nlist_item')[1:7]
        CAT1_link_list = []

        for CAT1 in CAT1_list:
            CAT1_link = CAT1.find_element(By.TAG_NAME, 'a')
            CAT1_link_list.append(CAT1_link.get_attribute('href'))
            # print(CAT1.text)

        return CAT1_link_list

    @staticmethod
    def set_CAT2():
        if Collect_news.CAT2_link_list == []:
            CAT1_link_list = Collect_news.set_CAT1()
            for CAT1 in CAT1_link_list:
                Collect_news.open_URL(CAT1)
                CAT2_list = Collect_news.chrome.find_elements(By.XPATH, '//*[@id="snb"]/ul/li')
                for CAT2 in CAT2_list:
                    CAT2.link = CAT2.find_element(By.TAG_NAME, 'a')
                    Collect_news.CAT2_link_list.append(CAT2.link.get_attribute('href'))
                    # print(CAT2.text)
        else:
            print('no more CAT2')

    @staticmethod
    def set_page(CAT2_link) -> list:
        Collect_news.open_URL(CAT2_link)
        page_link_list = [CAT2_link]
        page_list = Collect_news.chrome.find_element(By.CSS_SELECTOR, '#main_content > div.paging')  #.find_elements(By.CSS_SELECTOR, 'a.nclicks\(fls\.page\)')
        page_list = page_list.find_elements(By.TAG_NAME, 'a')
        for page in page_list:
            if re.match('[0-9]+',page.text):
                # print(re.match('[0-9]+',page.text))
                # print(page.text)
                page_link_list.append(page.get_attribute('href'))
            if page.text == '다음':
                page_link_list.extend(Collect_news.set_page(page.get_attribute('href')))

        return page_link_list

    @staticmethod
    def next_date(day :int) -> str:
        if day <= 0:
            print('0보다 큰 자연수를 입력하세요.')
            return
        next_day = Collect_news.chrome.find_element(By.XPATH, '//*[@id="main_content"]/div[4]/a[1]')
        yield next_day.get_attribute('href')
        # next_day.click()

        day += -1
        if day == 0:
            return
            
        next_day = Collect_news.chrome.find_element(By.XPATH, '//*[@id="main_content"]/div[4]/a[2]')
        yield next_day.get_attribute('href')
        # next_day.click()
        
        day += -1
        if day == 0:
            return
        
        while day > 0:
            next_day = Collect_news.chrome.find_element(By.XPATH, '//*[@id="main_content"]/div[4]/a[3]')
            yield next_day.get_attribute('href')
            # next_day.click()

    @staticmethod
    def read_one_news(link :str) -> Article():
        original_window = Collect_news.chrome.current_window_handle
        Collect_news.chrome.switch_to.new_window('tab')
        Collect_news.chrome.get(link)

        temp = Article()

        sid1 = re.compile('(sid1=)([0-9]*)')
        sid2 = re.compile('(sid2=)([0-9]*)')
        oid = re.compile('(oid=)([0-9]*)')
        
        temp.c_id = sid1.search(link).group(2)
        temp.cd_id = sid2.search(link).group(2)
        temp.press_num = oid.search(link).group(2)

        temp.press_name = Collect_news.chrome.find_element(By.XPATH, '//*[@id="main_content"]/div[1]/div[1]/a/img').get_attribute('title')

        temp.title = Collect_news.chrome.find_element(By.XPATH, '//*[@id="articleTitle"]').text
        temp.content = Collect_news.chrome.find_element(By.XPATH, '//*[@id="articleBodyContents"]').text  # ==> 요약본, 사진 정보를 삭제할것
        try:
            temp.pic_link = Collect_news.chrome.find_element(By.CSS_SELECTOR, '#articleBodyContents > span.end_photo_org').get_attribute('src')
        except:
            temp.pic_link = None
        temp.time = Collect_news.chrome.find_element(By.XPATH, '//*[@id="main_content"]/div[1]/div[3]/div/span').text
        temp.link =	Collect_news.chrome.find_element(By.LINK_TEXT, '기사원문').get_attribute('href')

        Collect_news.chrome.close()
        Collect_news.chrome.switch_to.window(original_window)

        return temp

    @staticmethod
    def read_one_page(page_link :str):  # yield 사용함
        Collect_news.open_URL(page_link)
        news_list = Collect_news.chrome.find_element(By.XPATH, '//*[@id="main_content"]/div[2]').find_elements(By.TAG_NAME, 'dl')
        for news in news_list:
            url = news.find_element(By.TAG_NAME, 'a').get_attribute('href')
            yield Collect_news.read_one_news(url)

    @staticmethod
    def periodic_Collect() -> None:
        Collect_news.set_CAT2()
        for CAT2 in Collect_news.CAT2_link_list:
            page_list = Collect_news.set_page(CAT2)
            for page in page_list:
                for article in Collect_news.read_one_page(page):
                    stop_check = NewsSql.insertNews(article)
                    if stop_check == False:
                        return

    @staticmethod
    def collect_all_press():
        Collect_news.open_URL()
        Collect_news.chrome.find_element(By.XPATH, '//*[@id="ct"]/div/section[1]/div[1]/ul/li[1]/a').click()
        press_list = Collect_news.chrome.find_element(By.CSS_SELECTOR, '#groupOfficeList > table > tbody').find_elements(By.TAG_NAME, 'a')
        for press in press_list:
            temp = Article()
            try:
                temp.press_num = re.search('(oid=)([0-9]*)',press.get_attribute('href')).group(2)
                temp.press_name = press.text
                PressSql.insertOnePress(temp)
            except:
                continue
            # print(temp.press_name, temp.press_num)

    @staticmethod
    def collect_past_news(day):
        Collect_news.set_CAT2()
        for CAT2 in Collect_news.CAT2_link_list:
            Collect_news.chrome.get(CAT2)
            for article in Collect_news.read_one_page(CAT2):
                # NewsSql.insertNews(article)
                print(article.title)
            for link in Collect_news.next_date(day):
                    # Collect_news.chrome.get(link)
                    page_list = Collect_news.set_page(link)
                    for page in page_list:
                        for article in Collect_news.read_one_page(page):
                            # stop_check = NewsSql.insertNews(article)
                            print(article.title)
                            # if stop_check == False:
                            #     return




if __name__ == "__main__":
    # Collect_news.set_page('https://news.naver.com/main/list.naver?mode=LS2D&sid2=259&mid=shm&sid1=101&date=20220106&page=11')
    # Collect_news.read_one_page('https://news.naver.com/main/list.naver?mode=LS2D&sid2=259&sid1=101&mid=shm&date=20220106&page=1')
    # Collect_news.collect_all_press()
    Collect_news.chrome.get('https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=101&sid2=259')
    Collect_news.collect_past_news(10)
