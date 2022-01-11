# WebPageSql.py
from SqlCon import SqlCon
from WebPage import WebPage
import pymssql

class WebPageSql:
    # 구현시킬 것 :
    # 수집한 웹 페이지 정보를 추가
    # 수집한 웹 페이지의 정보에 따라 소프트코딩을 시켜줄 수 있다
    @staticmethod
    def AddPage(wpage):
        cursor = SqlCon.Cursor()
        query = str.format("insert into Webpage (title, url, description, mcnt) values('{0}','{1}','{2}',{3})",
                           wpage.title, wpage.url, wpage.description, wpage.mcnt)
        try:    # 같은 url을 수집할 경우 예외가 발생할 수 있다.
            cursor.execute(query)
            SqlCon.Commit()
        except:
            return False
        else:
            return True


    # 웹 페이지에 형태소 개수 정보 수정
    @staticmethod
    def UpdateMCnt(url, mcnt): 
        cursor = SqlCon.Cursor()
        query = str.format("update WebPage set mcnt={0} where (url='{1}')",mcnt,url)
        try:
           cursor.execute(query)
           SqlCon.Commit()
        except:
            return False
        else:
            return True

    # wid로 수집한 웹페이지 정보검색
    @staticmethod
    def FindPageByWid(wpage):
        cursor = SqlCon.Cursor()
        query = str.format("select title, url, description, mcnt from WebPage where (wid={0})", wid)
        try: 
            cursor.execute(query)
            row = cursor.fetchone()     # 검색 결과 중에 하나의 Row를 fetch하시오.
            SqlCon.Commit()
        except:
            return None
        else:
            return row

    # url로 wid 찾기
    @staticmethod
    def FindWid(url):
        cursor = SqlCon.Cursor()
        query = str.format("select wid from WebPage where (url='{0}')", url)
        try: 
            cursor.execute(query)
            row = cursor.fetchone()     # 검색 결과 중에 하나의 Row를 fetch하시오.
            SqlCon.Commit()
        except:
            return 0
        else:
            if row == None:
                return 0
            return row[0]
    
    # 수집한 웹페이지 개수 확인
    # 검색한 단어가 자주 발견되는 단어가 아닐 경우 주요키가 될 가능성이 높아 신빙성 검사를 수행해야 한다
    # => 전체 수집한 웹 페이지 중 몇개의 단어가 있는지 조사하여 희귀성 조사
    # => 그러기 위해 수집한 웹 페이지의 개수 확인해야 한다
    @staticmethod
    def TotalDocumentCount():
        cursor = SqlCon.Cursor()
        query = "select count(*) from WebPage"      # str.format은 변수와 문자열을 혼용하여 하나의 문자열을 만들 때 사용(여기는 하나라 생략)
        try: 
            cursor.execute(query)
            row = cursor.fetchone()     # 검색 결과 중에 하나의 Row를 fetch하시오.
            SqlCon.Commit()
        except:
            return None
        else:
            return row[0]