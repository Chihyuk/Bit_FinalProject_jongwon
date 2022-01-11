# FindNewsCat.py
# 카테고리 별 번호
# 경제 sid1=101
# 금융 sid2=259
# 증권 sid2=258
# 산업/재계 sid2=261
# 중기/벤처 sid2=771
# 부동산 sid2=260
# 글로벌 경제 sid2=262
# 생활경제 sid2=310
# 경제 일반 sid2=263

# input url = 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=259&sid1=101&mid=shm&date=' 

url = 'https://news.naver.com/main/list.naver?mode=LS2D&' 

class FindNewsCat:
    def catInsert(url):
        # 경제 카테고리
        eco_sids = ['sid2=259&sid1=101', 'sid2=258&sid1=101', 'sid2=261&sid1=101', 'sid2=771&sid1=101', 'sid2=260&sid1=101', 'sid2=262&sid1=101', 'sid2=310&sid1=101', 'sid2=263&sid1=101']
        sidurls = []
        for n in range(len(eco_sids)):
            sidurls.append(url+eco_sids[n]+'&mid=shm&date=')
        return sidurls, eco_sids    # 카테고리 주소와 카테고리 번호 리턴
