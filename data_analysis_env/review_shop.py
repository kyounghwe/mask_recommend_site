from selenium import webdriver
from selenium.webdriver import ActionChains

# 콤마 제거 및 정수형 변환

driver_path = r'C:\Users\chromedriver.exe'


def cleaner(something):
    return int(something.replace(',', ''))


with webdriver.Chrome(driver_path) as driver:
    # pagingIndex, 원하는 페이지 수 만큼 반복
    for i in range(1, 2):
        driver.get(
            'https://search.shopping.naver.com/search/all?frm=NVSHATT&origQuery=%EB%A7%88%EC%8A%A4%ED%81%AC&pagingIndex={}&pagingSize=60&productSet=total&query=%EB%A7%88%EC%8A%A4%ED%81%AC&sort=rel&spec=M10018852%7CM10811849%20M10018852%7CM10811848%20M10018852%7CM10907665%20M10018852%7CM10811847&timestamp=&viewType=list'.format(i))

        # 페이지 내 데이터 로딩 대기
        driver.implicitly_wait(2)

        # 페이지 스크롤 (페이지 당 마스크 개수만큼)
        end_xpath = '//*[@id="__next"]/div/div[3]'
        some_tag = driver.find_element_by_xpath(end_xpath)
        action = ActionChains(driver)
        action.move_to_element(some_tag).perform()

        for x in range(5, 6):
            # x번째 마스크로 스크롤
            end_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{x}]/li/div[1]/div[2]/div[5]'
            some_tag = driver.find_element_by_xpath(end_xpath)
            action = ActionChains(driver)
            action.move_to_element(some_tag).perform()
            # 마스크 이미지 로딩 대기
            driver.implicitly_wait(2)
            name_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{x}]/li/div[1]/div[2]/div[1]'

            # 마스크 이름을 기반으로 링크 정보 가져오기
            name_url = driver.find_element_by_xpath(
                name_xpath).find_element_by_tag_name('a').get_attribute('href')

            with webdriver.Chrome(driver_path) as dv:
                dv.get('{}'.format(name_url))
                dv.implicitly_wait(5)
                curren_url = dv.current_url

                if 'shopping' in curren_url:
                    mask_review_page_xpath = dv.find_element_by_xpath('//*[@id="section_review"]/div[3]')
                    action = ActionChains(dv)
                    action.move_to_element(
                        mask_review_page_xpath).perform()
                    dv.implicitly_wait(10)
                    
                    mask_review_list = []
                    review_page = 2

                    while True:
                        review_num = 1
                        pagination_num= dv.find_element_by_class_name('pagination_now__gZWGP').text.replace("현재 페이지", "")
                        dv.implicitly_wait(10)

                        if int(pagination_num) != 10:                        
                            while True:
                                try:
                                    mask_review_xpath = f'//*[@id="section_review"]/ul/li[{review_num}]/div[2]/div/p'
                                    mask_review = dv.find_element_by_xpath(
                                        mask_review_xpath).text
                                    mask_review_list.append(
                                    mask_review.replace("\n", ""))
                                    review_num += 1
                                except:
                                    break

                            if int(pagination_num) % 10 == 0:
                                if int(pagination_num) == 30:
                                    break
                                next_page = dv.find_element_by_xpath('//*[@id="section_review"]/div[3]/a[12]')
                                next_page.click()
                                review_num = 1
                                review_page = 2

                        if int(pagination_num) == 10:
                            while True:
                                try:
                                    mask_review_xpath = f'//*[@id="section_review"]/ul/li[{review_num}]/div[2]/div/p'
                                    mask_review = dv.find_element_by_xpath(
                                        mask_review_xpath).text
                                    mask_review_list.append(
                                    mask_review.replace("\n", ""))
                                    review_num += 1
                                except:
                                    break
                            try:
                                next_page = dv.find_element_by_xpath('//*[@id="section_review"]/div[3]/a[11]')
                                next_page.click()
                                review_num = 1
                                review_page = 2
                            except:
                                break
                        

                            # while True:
                            #     try:
                            #         mask_review_xpath = f'//*[@id="section_review"]/ul/li[{review_num}]/div[2]/div/p'
                            #         mask_review = dv.find_element_by_xpath(
                            #             mask_review_xpath).text
                            #         mask_review_list.append(
                            #             mask_review.replace("\n", ""))
                            #         # mask_review_list.append(mask_review.strip("\n"))
                            #         review_num += 1
                            #     except:
                            #         break
                            
                        else:
                            try:
                                review_page += 1
                                current_page = dv.find_element_by_xpath(
                                    '//*[@id="section_review"]/div[3]/a[{}]'.format(review_page))
                                current_page.click()
                                review_num = 1
                                action = ActionChains(dv)
                                action.move_to_element(
                                    mask_review_page_xpath).perform()
                                dv.implicitly_wait(5)
                            except:
                                break