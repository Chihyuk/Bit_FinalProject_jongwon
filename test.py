from selenium import webdriver
from selenium.webdriver.common.by import By

# driver = webdriver.Chrome()
# original_window = driver.current_window_handle
# driver.get("https://www.google.com")
# driver.find_element(By.CSS_SELECTOR, '[name="q"]').send_keys("webElement")

# # Get attribute of current active element
# attr = driver.switch_to.active_element.get_attribute("title")
# print(attr)

# # test = locate_with(By.TAG_NAME, 'input').below({By.XPATH:'/html/body/div[1]/div[2]/div/img'})
# # print(test)

# date = '1월7일(금)'
# month,  week = date.split('월')
# day, DofW = week.split('일')
# print(month, day, DofW)

# driver.switch_to.new_window('tab')
# driver.switch_to.new_window('tab')
# driver.get("https://www.google.com")
# driver.close()
# driver.switch_to.window(original_window)
# # driver.switch_to.new_window('window')

# driver.get('https://news.naver.com/main/read.naver?mode=LS2D&mid=shm&sid1=101&sid2=259&oid=215&aid=0001008051')
# js = driver.find_element(By.XPATH, '//*[@id="main_content"]/script[2]')
# import re
# url = 'https://news.naver.com/main/read.naver?mode=LS2D&mid=shm&sid1=101&sid2=259&oid=648&aid=0000005761'
# sid2 = re.compile('(sid2=)([0-9]*)')
# oid = re.compile('odi=[0-9]*')
# cd_id = url[sid2.search(url).start(2) : sid2.search(url).end(2)]
# print(cd_id)
# print(re.search('sid2=[0-9]*', url))
# test = []
# for i in [0,1,2,3,4,5]:
#     test.append(i)
# print(f'test = {test}')
# for i in test:
#     print(test.pop())

# tt = 'test'
# if tt == 'test':
#     print('tt')

# def tt():
#     for i in [0,1,2,3,4,5]:
#         yield i

# for j in range(10):
#     # print(tt.__next__())
#     print(next(tt()))

# s1 = "abcde"	#"c"
# s2 = "qwer"	#"we"

# # n = len(s2)-1
# # if n%2 == 0:
# #     print(s2[int(n/2):int((n/2)+1)])
# # else:
# #     print(s2[(n-1)//2:(n+1)//2+1])
# for i in ['abcde','qwer']:
#     print(i[(len(i)-1)//2:len(i)//2+1])
#     print([(len(i)-1)//2,len(i)//2+1])

import datetime

# t1 = datetime.datetime()
td = datetime.timedelta(hours=13)
print(td)