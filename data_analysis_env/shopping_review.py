from selenium import webdriver
from selenium.webdriver import ActionChains


# 콤마 제거 및 정수형 변환

driver_path = r'C:\Users\Starter\chromedriver.exe'


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
                redirect_url = dv.current_url

                if 'shopping.naver' in redirect_url:
                    # 스크롤 엔드포인트
                    mask_review_end_xpath = dv.find_element_by_xpath(
                        '//*[@id="section_recommend"]/h3')
                    dv.implicitly_wait(10)
                    action = ActionChains(dv)
                    action.move_to_element(mask_review_end_xpath).perform()
                    
                    mask_review_list = []

                    try:
                        mask_review_page_xpath = dv.find_element_by_xpath(
                            '//*[@id="section_review"]/div[3]')
                        page_num = mask_review_page_xpath.text
                        page_num = page_num.replace('현재 페이지', '')
                        page_num = page_num.replace('다음', '')

                        if dv.find_element_by_xpath('//*[@id="section_review"]/div[3]/a[11]').text == '다음':
                            # 1~10 page 까지 크롤링
                            review_page = 1
                            while True:
                                review_num = 1
                                while True:
                                    try:
                                        mask_review_xpath = f'//*[@id="section_review"]/ul/li[{review_num}]/div[2]/div[1]/p'
                                        mask_review = dv.find_element_by_xpath(
                                            mask_review_xpath).text
                                        mask_review_list.append(
                                            mask_review.replace("\n", ""))
                                        review_num += 1
                                    except:
                                        break

                                review_page += 1

                                if review_page != 11:
                                # if dv.find_element_by_xpath('//*[@id="section_review"]/div[3]/a[{}]'.format(review_page)).text.replace('현재 페이지\n', '') != '11':
                                    current_page = dv.find_element_by_xpath(
                                        '//*[@id="section_review"]/div[3]/a[{}]'.format(review_page))
                                    current_page.click()
                                    review_num = 1
                                    dv.implicitly_wait(10)
                                    action = ActionChains(dv)
                                    action.move_to_element(
                                        mask_review_page_xpath).perform()
                                    
                                else:
                                    break
                            # 다음 버튼 클릭
                            next_page = dv.find_element_by_xpath(
                                '//*[@id="section_review"]/div[3]/a[11]')
                            next_page.click()
                            dv.implicitly_wait(10)
                            action = ActionChains(dv)
                            action.move_to_element(
                                mask_review_page_xpath).perform()
                            

                            # 11page부터 페이지 하나씩 넘기면서 크롤링, 다음 버튼 없으면 break
                            review_page = 2
                            while True:
                                review_num = 1
                                while True:
                                    try:
                                        mask_review_xpath = f'//*[@id="section_review"]/ul/li[{review_num}]/div[2]/div[1]/p'
                                        mask_review = dv.find_element_by_xpath(
                                            mask_review_xpath).text
                                        mask_review_list.append(
                                            mask_review.replace("\n", ""))
                                        review_num += 1
                                    except:
                                        break
                                try:
                                    review_page += 1
                                    if review_page != 12:
                                        current_page = dv.find_element_by_xpath(
                                            '//*[@id="section_review"]/div[3]/a[{}]'.format(review_page))
                                        current_page.click()
                                        review_num = 1
                                        dv.implicitly_wait(10)
                                        action = ActionChains(dv)
                                        action.move_to_element(
                                            mask_review_page_xpath).perform()

                                    elif review_page == 12 and dv.find_element_by_xpath('//*[@id="section_review"]/div[3]/a[11]').text.replace('현재 페이지\n', '') == '30':
                                        break

                                    else:
                                        next_page = dv.find_element_by_xpath(
                                            '//*[@id="section_review"]/div[3]/a[12]')
                                        next_page.click()
                                        dv.implicitly_wait(10)
                                        action = ActionChains(dv)
                                        action.move_to_element(
                                            mask_review_page_xpath).perform()
                                        review_page = 2
                                except:
                                    break
                    # 10page 이후로 없는 경우
                    except:
                        # review page index가 2이상 9이하일 경우
                        try:
                            mask_review_page_xpath = dv.find_element_by_xpath(
                                '//*[@id="section_review"]/div[3]')
                            page_num = mask_review_page_xpath.text
                            page_num = page_num.replace('현재 페이지', '')
                            page_num = page_num.replace('다음', '')
                            review_page = 1
                            while True:
                                review_num = 1
                                while True:
                                    try:
                                        mask_review_xpath = f'//*[@id="section_review"]/ul/li[{review_num}]/div[2]/div[1]/p'
                                        mask_review = dv.find_element_by_xpath(
                                            mask_review_xpath).text
                                        mask_review_list.append(
                                            mask_review.replace("\n", ""))
                                        review_num += 1
                                        print(review_page, review_num, mask_review)
                                    except:
                                        break

                                review_page += 1
                                if review_page > int(page_num[-1]):
                                    break
                                else:
                                    current_page = dv.find_element_by_xpath(
                                        '//*[@id="section_review"]/div[3]/a[{}]'.format(review_page))
                                    current_page.click()
                                    review_num = 1
                                    dv.implicitly_wait(5)
                                    action = ActionChains(dv)
                                    action.move_to_element(
                                        mask_review_page_xpath).perform()
                                    

                        # reivew page index가 없는 경우
                        except:
                            # 리뷰가 있는 경우
                            try:
                                review_num = 1
                                while True:
                                    try:
                                        mask_review_xpath = f'//*[@id="section_review"]/ul/li[{review_num}]/div[2]/div[1]/p'
                                        mask_review = dv.find_element_by_xpath(
                                            mask_review_xpath).text
                                        mask_review_list.append(
                                            mask_review.replace("\n", ""))
                                        review_num += 1
                                    except:
                                        break
                            # 리뷰가 없는 경우
                            except:
                                mask_review_list = None
