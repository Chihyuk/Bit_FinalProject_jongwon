# PressSql.py

from SqlCon import SqlCon

class PressSql:
    @staticmethod
    def insertPress(press):
        try:
            for i in range(len(press.press_num)):
                cursor = SqlCon.Cursor()
                query = str.format("insert into Press (p_id, p_name) values({0}, '{1}')", press.press_num[i], press.press_name[i])

                try:    # 같은 url을 수집할 경우 예외가 발생할 수 있다.
                    cursor.execute(query)
                    SqlCon.Commit()
                except:
                    continue
        except:
            False
        else:
            True

    @staticmethod
    def insertOnePress(news):
        cursor = SqlCon.Cursor()
        query = str.format("insert into Press (p_id, p_name) values({0}, '{1}')", news.press_num, news.press_name)

        try:    # 같은 url을 수집할 경우 예외가 발생할 수 있다.
            cursor.execute(query)
            SqlCon.Commit()

        except:
            False
        else:
            True

    @staticmethod
    def findPressNumber(news):
        cursor = SqlCon.Cursor()
        query = str.format("select p_id from Press where (p_name='{0}')", news.press)
        try: 
            cursor.execute(query)
            row = cursor.fetchone()     # 검색 결과 중에 하나의 Row를 fetch하시오.
            SqlCon.Commit()
        except:
            return None
        else:
            return row[0]