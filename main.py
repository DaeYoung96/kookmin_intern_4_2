from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(1)
wait = WebDriverWait(driver, 10)

result = pd.DataFrame(columns=['username', 'phone', 'name', 'address', 'career', 'info_company', 'info_biz', 'key'])
result.to_csv('result.csv', encoding='CP949')
f = open('result.csv', 'w', encoding='CP949', newline='')
wr = csv.writer(f)
wr.writerow(['username', 'phone', 'name', 'address', 'career', 'info_company', 'info_biz', 'key'])
# 로그인
driver.get('https://www.makervil.com/user/inputLogin.do')
driver.find_element_by_name('user_id').send_keys('remigailard80')
driver.find_element_by_id('input_password').send_keys('@bolt123')
driver.find_element_by_class_name('btn-common').click()

# 기업리스트 페이지로 이동
driver.get('https://www.makervil.com/user/company/viewCompanyListMain.do')

start = time.time()

# 반복 시작
page = 1
# 5318
for i in range(2, 4, 1):
    # 확인하기 위한 페이지 출력
    print("page : ", page)
    # 해당 페이지 기업 리스트 20개 탐색 시작
    for j in range(1, 21, 1):
        list_xpath = '//*[@id="content"]/div[1]/div[1]/ul/li[' + str(j) + ']/div[2]'
        element = wait.until(EC.element_to_be_clickable((By.XPATH, list_xpath)))
        driver.find_element_by_xpath(list_xpath).click()

        # 확인하기 위한 파트너 번째 수
        print("list : ", j)

        print(driver.current_url)

        # 데이터 로딩까지 대기
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#go-info > ul > li:nth-child(5) > span:nth-child(2)')))
        
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

    # 20개의 리스트가 끝나면 다음 페이지로 이동
    driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/ul/li['+ str(i) +']/a').click()
    page += 1

print(time.time() - start)