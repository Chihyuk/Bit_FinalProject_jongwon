# CandidateSql.py
from SqlCon import SqlCon
from WebPageSql import WebPageSql
import pymssql

# 수집후보 테이블과 상호작용하는 클래스
class CandidateSql:
    # 후보사이트 등록 메소드
    # url : 수집 대상 사이트 주소
    # depth : seed 사이트에서 상대적 깊이
    # 동일한 url이 들어가거나 수집된 페이지가 수집되면 안된다.
    @staticmethod
    def AddCandidate(url,depth):
        cursor = SqlCon.Cursor()
        if WebPageSql.FindWid(url) != 0:    # 이미 수집한 사이트
            return False
        query = str.format("insert into Candidate (url,depth) values('{0}',{1})", url, depth)
        try: 
            cursor.execute(query)
            SqlCon.Commit()
        except:
            return False
        else:
            return True

    # 수집해야 할 후보 사이트 ID 확인 메소드
    # 최소값에 해당하는 ID를 가져와야 한다
    @staticmethod
    def GetCandidateID():
        cursor = SqlCon.Cursor()
        query = str.format("select MIN(id) from Candidate")     # MIN 내장함수 사용
        try: 
            cursor.execute(query)
            row = cursor.fetchone()
            SqlCon.Commit()
        except:
            return 0
        else:
            if row:             # row에 값이 있는 경우 return row[0]
                return row[0]
            return 0            # 검색 결과가 없는 경우 return 0 => candidate table에 결과가 없음

    # 후보사이트 삭제 메소드
    @staticmethod
    def Remove(id):
        cursor = SqlCon.Cursor()
        query = str.format("delete from Candidate where id={0}", id)
        try: 
            cursor.execute(query)
            SqlCon.Commit()
            # delete, drop은 commit이 필요 없다 (rollback이 안되는 쿼리이기 때문)
        except:
            return False
        else:
            return True

    # 수집해야 할 후보 사이트 검색 메소드(ID 확인 및 삭제 후 반환)
    @staticmethod
    def GetCandidate():
        id = CandidateSql.GetCandidateID()      # 수집해야할 사이트 ID 검색
        if id == 0:         # 수집해야 할 사이트가 없을 때
            return "",-1    # 앞은 url, 뒤는 depth

        # 사이트 주소와 depth를 주기위해 쿼리문 작성
        cursor = SqlCon.Cursor()
        query = str.format("select url, depth from Candidate where id={0}", id)
        try: 
            cursor.execute(query)
            row = cursor.fetchone()
            SqlCon.Commit()
        except:             # 예외가 발생했을 때
            return "",-1
        else:
            if row:         # 검색 결과가 있을 때
                CandidateSql.Remove(id)     # 수집 후보 테이블에서 삭제
                return row[0], row[1]       # 사이트 주소아 depth 반환
            return "",-1                    # 검색 결과가 없을 때
