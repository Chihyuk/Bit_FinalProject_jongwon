# NewsSql.py

from SqlCon import SqlCon
from PressSql import PressSql
# from Article import Article

class NewsSql:
    # news의 변수 : title, content, time, link, pic_link, press, p_id, cd_id

    # News 테이블 내용 넣기
    @staticmethod
    def insertNews(news):
        cursor = SqlCon.Cursor()
        # 없는 언론사일 수 있으니 insert
        PressSql.insertOnePress(news)
        # 언론사 번호를 어떻게 넣냐
        query = str.format("insert into News (p_id, cd_id, n_title, nd_img, n_input, o_link) values({0}, {1}, '{2}', '{3}', '{4}', '{5}')", news.press_num, news.cd_id, news.title, news.pic_link, news.time, news.link)

        try:    # 같은 url을 수집할 경우 예외가 발생할 수 있다.
            cursor.execute(query)
            SqlCon.Commit()
        except:
            False
        else:
            True

    # News 테이블 n_id 얻기
    @staticmethod
    def findnidNumber(news):
        cursor = SqlCon.Cursor()
        query = str.format("select n_id from News where (o_link='{0}')", news.link)
        try: 
            cursor.execute(query)
            row = cursor.fetchone()     # 검색 결과 중에 하나의 Row를 fetch하시오.
            SqlCon.Commit()
        except:
            return None
        else:
            return row[0]

    # 뉴스 내용 넣기
    @staticmethod
    def insertDescNews(news):
        cursor = SqlCon.Cursor()
        nid = NewsSql.findnidNumber(news)
        query = str.format("insert into N_content (n_id, n_content) values({0}, '{1}')", nid, news.content)

        try:    # 같은 url을 수집할 경우 예외가 발생할 수 있다.
            cursor.execute(query)
            SqlCon.Commit()
        except:
            False
        else:
            True
