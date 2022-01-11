# WebPage.py
from EHHelper import EHHelper   # 앞으로 모든 프로젝트에 사용 예정

class WebPage:
    # 생성자
    def __init__(self,url,title,description,links):
        # 사이트 주소
        self.url = url
        # 페이지 제목
        self.title = EHHelper.RemoveTagAndSpecialCh(title)
        # 페이지 내용
        self.description = EHHelper.RemoveTagAndSpecialCh(description)
        # 페이지 내부 하이퍼링크 목록
        self.links = links
        # 페이지 내용의 형태소 개수
        self.mcnt=0

    # WebPage 개체를 생성하는 정적 메서드
    # url: 사이트 주소
    # cpage: 수집한 웹 페이지(요청 결과를 BeautifulSoup으로 변환한 개체)
    # 반환: WebPage 개체
    @staticmethod
    def MakeWebPage(url,cpage):
        try:
            # 제목 얻어오기(tag까지 얻어오기 때문에 .text 사용)
            title = cpage.title.text        
            # 하이퍼링크 태그 목록을 전수 조사
            atags = cpage.find_all('a')
            # http or https 하이퍼링크만 추출하기(파일 다운로드 등 필터링)
            links = WebPage.ExtractionUrls(atags)
        except:
            return None # 예외가 발생하면 결측치 반환
        else:           # 예외가 발생되지 않은 경우 웹페이지 생성
            return WebPage(url,title,cpage.text,links)

    # 하이퍼링크 태그 목록 중에 http or https 링크를 제외한 나머지 필터링 (정적)메서드
    # atags: 하이퍼링크 태그 목록
    # 반환: 필터링 이후 목록
    @staticmethod
    def ExtractionUrls(atags):
        links = []            # 반환할 리스트
        for atag in atags:
            # 다운로드 어트리뷰트가 있는지 확인
            # 파일을 다운로드 받는 태그가 아닐 때
            if atag.has_attr('download') == False:
                try:
                    link = atag['href']     # href의 있는 경우 링크를 얻어오기               
                except:
                    # continue 사용 이유 : href가 없어 예외가 발생된 경우에도 
                    # 뒤에 있는 하이퍼링크들도 조사를 해야하기 때문에 continue를 사용한다.
                    continue        
                else:
                    #link = WebPage.ExtractionUrl(link)
                    #print(link)
                    #if link.find("mode=LSD&mid=shm&sid1=101") and link.find("news.naver.com/main/"):
                    #if str.startswith(link,'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101') or str.startswith(link,'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=101') or str.startswith(link,'https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=101') or str.startswith(link,'http://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101') or str.startswith(link,'http://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=101') or str.startswith(link,'http://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=101'): # https도 http로 시작한다
                    if link.startswith('https://news.naver.com/main/read.naver?mode=LS2D&mid=shm&sid1=101') or link.startswith('http://news.naver.com/main/read.naver?mode=LS2D&mid=shm&sid1=101'):
                       links.append(link)
        return links

    # url에 페이지 조각이나 쿼리 문자열이 있을 때 사이트 주소만 추출하는 정적 메서드
    # url: 사이트 주소(페이지 조작이나 쿼리 문자열 포함)
    # 반환: 사이트 주소만 추출한 문자열
    @staticmethod
    # #은 자기 자신을 의미하기 때문에 배제시켜야 한다.
    # 링크(베너 등)에 id가 포함된 경우 수집할 때 배제되어야 한다.
    # 이러한 것들을 배제시키기 위한 메소드
    def ExtractionUrl(url):
        index = url.find('#') # 페이지 조각
        # find 메소드는 찾으면 url인덱스 반환 못찾으면 -1 반환
        # index 메소드는 찾으면 url인덱스 반환 못찾으면 예외 발생
        if index !=-1: # 찾았을 때
            url = url[:index]   # # 이전 내용만 사이트 주소로 인식, # 뒤는 잘라버려라
        index = url.find('?') # 쿼리 문자열일 때
        if index !=-1: # 찾았을 때
            url = url[:index]   # ? 내용 이전까지 내용만 저장
        return url

    