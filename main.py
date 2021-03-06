from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1920, 1080))
display.start()

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(1)
wait = WebDriverWait(driver, 20)
result = pd.DataFrame(columns=['username', 'phone', 'name', 'address', 'career', 'info_company', 'info_biz', 'key'])
result.to_csv('result 44.csv', encoding='CP949')
f = open('result 44.csv', 'w', encoding='CP949', newline='')
wr = csv.writer(f)
wr.writerow(['username', 'phone', 'name', 'address', 'career', 'info_company', 'info_biz', 'key'])
# 로그인
driver.get('https://www.makervil.com/user/inputLogin.do')
driver.find_element_by_name('user_id').send_keys('remigailard80')
driver.find_element_by_id('input_password').send_keys('@bolt123')
driver.find_element_by_class_name('btn-common').click()

start_url = 'https://www.makervil.com/user/company/viewCompanyListMain.do?CompanySearch=&area=44'

# 기업리스트 페이지로 이동
driver.get(start_url)
# 6페이지부터 시작
# driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/ul/li[6]/a').click()

start = time.time()

# 반복 시작
page = 1
tmp = 2
flag = False
cnt = 0
# 5318
for i in range(0, 74, 1):
    # 확인하기 위한 페이지 출력
    print("page : ", page)
    # 해당 페이지 기업 리스트 20개 탐색 시작
    for j in range(1, 21, 1):
        time.sleep(0.5)
        list_xpath = '//*[@id="content"]/div[1]/div[1]/ul/li[' + str(j) + ']/div[2]'
        wait.until(EC.presence_of_element_located((By.XPATH, list_xpath)))
        driver.find_element_by_xpath(list_xpath).click()

        while True:
            if driver.current_url == 'https://www.makervil.com/user/company/viewCompanyListMain.do':
                driver.find_element_by_xpath(list_xpath).click()
            else:
                break

        # 확인하기 위한 파트너 번째 수
        print("list : ", j)

        print(driver.current_url)

        # 데이터 로딩까지 대기
        time.sleep(0.5)
        
        # 해당 링크로 들어와서 크롤링
        html = driver.page_source
        bs = BeautifulSoup(html, 'html.parser')

        # 키워드 파싱
        username = bs.select('#go-info > ul > li:nth-child(5) > span:nth-child(2)')
        phone = bs.select('#go-info > ul > li:nth-child(3) > span:nth-child(2)')
        name = bs.select('#content > div > ul > li > div.com-info > div.name > span:nth-child(1)')
        address = bs.select('#go-way > p')
        career = bs.select('#go-info > ul > li:nth-child(1) > span:nth-child(2)')
        info_company = bs.select('#content > div > ul > li > div.com-info > div.text')
        info_biz = bs.select('#go-info > ul > li:nth-child(2) > span.category')
        key = bs.select('#content > div > ul > li > div.com-info > div.key')


        username = str(username).replace('[<span>', '').replace('</span>]', '')
        phone = str(phone).replace('[<span>', '').replace('</span>]', '')
        name = str(name).replace('[<span>', '').replace('</span>]', '')
        address = str(address).replace('[<p class="add-list">', '').replace('</p>]', '')
        career = str(career).replace('[<span>', '').replace('</span>]', '')
        info_company = str(info_company).replace('[<div class="text">', '').replace('</div>]', '')
        info_biz = str(info_biz).replace('[<span class="category">\n', '').replace('<span>', '').replace('</span>\n', '/').replace('</span>]', '')
        key = str(key).replace('[<div class="key">', '').replace(' ', '').replace('\t', ''). replace('\n', '').replace('</div>]', '')

        # 엑셀에 저장
        wr.writerow([username, phone, name, address, career, info_company, info_biz, key])

        # 뒤로가기 실행
        driver.back()
        while True:
            if driver.current_url == 'https://www.makervil.com/user/company/viewCompanyListMain.do' or driver.current_url == start_url:
                break
            else:
                driver.back()

    # 20개의 리스트가 끝나면 다음 페이지로 이동
    time.sleep(0.3)
    next_page_xpath = '//*[@id="content"]/div[1]/div[2]/ul/li['+ str(tmp) +']/a'
    wait.until(EC.presence_of_element_located((By.XPATH, next_page_xpath)))
    driver.find_element_by_xpath(next_page_xpath).click()

    if flag == False:
        tmp += 1

    if flag == True:
        if tmp == 8:
            tmp = 4
            cnt += 1
        else:
            tmp += 1

    if page == 5:
        tmp = 4
        flag = True
        cnt += 1



    page += 1
    print("tmp : ", tmp)

print(time.time() - start)
print(cnt)
