# 코알라유니브 스터디: 공공공공공경경 - 고주형
# 네이버 신지도 데이터 수집하기
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.get("https://map.kakao.com/")
#driver.maximize_window()

# 팝업 창 제거
#driver.find_element(By.CSS_SELECTOR,"button#intro_popup_close").click()

# test

search_box = driver.find_element(By.ID,"search.keyword.query")
#print(search_box.get_attribute("outerHTML"))
search_box.send_keys("서울 교차로")
time.sleep(2)
search_box.send_keys(Keys.ENTER)
time.sleep(2)
total_places = int(driver.find_element(By.ID,"info.search.place.cnt").get_attribute("textContent").replace(',',''))
more_btn = driver.find_element(By.ID, "info.search.place.more")
driver.execute_script("arguments[0].click();",more_btn)
i = 0
page_n = 1
with open('./street.txt','w',encoding='utf-8') as f:
    f.write("-------------------------------------------------\n")
while True:
    time.sleep(2)
    print("++++++++page no"+str(page_n)+"++++++++++++++++++++")
    cur_items = driver.find_elements(By.CLASS_NAME, "PlaceItem.clickArea")
    cnt = 0
    for item in cur_items:
        cnt += 1
        street_name = item.find_element(By.CLASS_NAME, "link_name").get_attribute("textContent")
        print("교차로 명: "+street_name)
        street_addr = item.find_element(By.CSS_SELECTOR, "p[data-id='address']").get_attribute("textContent")
        print("주소: "+street_addr)
        with open('./street.txt','a',encoding='utf-8') as f:
            f.write("교차로 명: "+street_name+"\n")
            f.write("주소: "+street_addr+"\n")
            f.write("-------------------------------------------------\n")
    i += cnt
    print("cnt: "+str(cnt)+", i: "+str(i))
    #time.sleep(2)
    if page_n == 5:
        next_page_btn = driver.find_element(By.ID, "info.search.page.next")
        driver.execute_script("arguments[0].click();",next_page_btn)
        time.sleep(2)
        page_n = 1
    else:
        page_n += 1
        page_num = "info.search.page.no"+str(page_n)
        page_btn = driver.find_element(By.ID, page_num)
        print("page class: "+page_btn.get_attribute("class"))
        if page_btn.get_attribute("class") != "INACTIVE HIDDEN":
            driver.execute_script("arguments[0].click();",page_btn)
        else:
            print("end of page parsing")
            break
with open('./street.txt','a',encoding='utf-8') as f:
    f.write("-------------------------------------------------\n")

# 크롭 웹페이지를 닫음
driver.close()