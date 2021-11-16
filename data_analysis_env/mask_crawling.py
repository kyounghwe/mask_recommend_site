from selenium import webdriver
from selenium.webdriver import ActionChains
import pandas as pd
import os

# import urllib.request
# import time

# 콤마 제거 및 정수형 변환
def cleaner(something):
    return int(something.replace(',', ''))

# # 마스크 이미지 담는 폴더 생성
# if not os.path.isdir('mask_img'):
#     os.mkdir('mask_img')

with webdriver.Chrome(r'/Users/krc/Downloads/chromedriver') as driver:
    # pagingIndex, 원하는 페이지 수 만큼 반복
    for i in range(1, 3):
        driver.get(
            'https://search.shopping.naver.com/search/all?frm=NVSHATC%27&origQuery=%EB%A7%88%EC%8A%A4%ED%81%AC&pagingIndex={}&pagingSize=20&productSet=total&query=%EB%A7%88%EC%8A%A4%ED%81%AC&sort=rel&timestamp=&viewType=list'.format(i))

        # 페이지 내 데이터 로딩 대기
        driver.implicitly_wait(5)

        # 페이지 스크롤 (페이지 당 60개 항목 끝까지)
        end_xpath = '//*[@id="__next"]/div/div[3]'
        some_tag = driver.find_element_by_xpath(end_xpath)
        action = ActionChains(driver)
        action.move_to_element(some_tag).perform()

        # 최종 마스크 데이터 리스트
        mask = []
        # # 마스크 이미지 담는 폴더 생성
        # if not os.path.isdir('mask_img\{}'.format(i)):
        #     os.mkdir('mask_img\{}'.format(i))
        # 페이지 당 개수를 기준으로 반복
        for x in range(1, 21):
            # x번째 마스크로 스크롤
            end_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{x}]/li/div[1]/div[2]/div[5]'
            some_tag = driver.find_element_by_xpath(end_xpath)
            action = ActionChains(driver)
            action.move_to_element(some_tag).perform()

            # 마스크 이미지 로딩 대기
            driver.implicitly_wait(5)

            # 마스크 이름
            name_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{x}]/li/div[1]/div[2]/div[1]'
            mask_name = driver.find_element_by_xpath(name_xpath).text

            # 마스크 리뷰 수
            review_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{x}]/li/div[1]/div[2]/div[5]'
            review_area = driver.find_element_by_xpath(review_xpath)

            # 마스크 별점
            star_path = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{x}]/li/div[1]/div[2]/div[5]'
            star = driver.find_element_by_xpath(star_path)

            # 마스크 가격
            price_list = driver.find_elements_by_class_name('price_num__2WUXn')
            price = price_list[x-1].text
            price = cleaner(price[:-1])

            # 카테고리
            category_path = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{x}]/li/div[1]/div[2]/div[3]'
            category = driver.find_element_by_xpath(category_path+'/a[3]').text

            # 마스크 기능 리스트
            main_func = []

            # 리뷰 수 Breakpoint
            # 리뷰-a태그 영역 따온 다음 text 속성이 리뷰면 em 텍스트 가져오기
            # xpath 접근법 /태그명[@속성명=속성값] 형태
            if '리뷰' in review_area.text:
                review_number = driver.find_element_by_xpath(
                    review_xpath+'/a[1]/em[@class="basicList_num__1yXM9"]').text
                review_number = cleaner(review_number)

            # 페이지 내 리뷰 수 없을 경우
            else:
                try:
                    # 마스크 이름 - a태그 - href의 url 정보 가져오기
                    url = driver.find_element_by_xpath(
                        name_xpath).find_element_by_tag_name('a').get_attribute('href')


                    # 가져온 url로 접속하여 리뷰 수 가져오기
                    with webdriver.Chrome(r'/Users/krc/Downloads/chromedriver') as dv:
                        dv.get('{}'.format(url))
                        driver.implicitly_wait(2)

                        # 리뷰 수 있는 곳으로 스크롤 후 리뷰 수 가져오기
                        some_tag = dv.find_element_by_xpath(
                            '//*[@id="content"]/div/div[3]/div[1]')

                        action = ActionChains(dv)
                        action.move_to_element(some_tag).perform()

                        review_location = dv.find_element_by_xpath(
                            '//*[@id="content"]/div/div[2]/div[1]/div[2]').text

                        review_number_find = review_location.find('사용자')
                        if review_number_find != -1:
                            review_number = review_location[3:review_number_find]
                            review_number = cleaner(review_number)
                        else:
                            review_number = 0
                except:
                    review_number = 0

            # 별점 Breakpoint
            # 별점 x.x 에서 점수만 선택
            if '리뷰별점' in star.text:
                star_rating = driver.find_element_by_xpath(
                    star_path+'/a/span/span[@class="basicList_star__3NkBn"]').text
                star_rating = float(star_rating[3:])

            # 페이지 내 별점 없을 경우
            else:
                try:
                    url = driver.find_element_by_xpath(
                        name_xpath).find_element_by_tag_name('a').get_attribute('href')

                    with webdriver.Chrome(r'/Users/krc/Downloads/chromedriver') as dv:
                        dv.get('{}'.format(url))
                        dv.implicitly_wait(5)

                        some_tag = dv.find_element_by_xpath(
                            '//*[@id="content"]/div/div[3]/div[1]')
                        action = ActionChains(dv)
                        action.move_to_element(some_tag).perform()

                        star_location = dv.find_element_by_xpath(
                            '//*[@id="content"]/div/div[2]/div[1]/div[2]').text
                        star_rating_find = star_location.find('평점')
                        if star_rating_find != -1:
                            star_rating = star_location[star_rating_find +
                                                        2:-3].strip('\n')
                            star_rating = float(star_rating)
                        else:
                            star_rating = float(0)
                except:
                    star_rating = float(0)

            # 마스크 이미지 가져오기
            # 마스크 이름을 기반으로 링크 정보 가져오기
            name_url = driver.find_element_by_xpath(
                name_xpath).find_element_by_tag_name('a').get_attribute('href')

            # 가격비교, 스토어 상품 링크에 들어가는 shopping을 기준으로 구분 (adcr은 공통, shopping은 독립적)
            # 스토어 상품이나 가격비교인 경우
            if 'shopping' in name_url:
                try:
                    with webdriver.Chrome(r'/Users/krc/Downloads/chromedriver') as dv:
                        dv.get('{}'.format(name_url))
                        dv.implicitly_wait(10)

                        # 스크롤 엔드포인트 지정
                        some_tag = dv.find_element_by_xpath(
                                '//*[@id="__next"]/div/div[2]/div[2]/div[2]')
                        action = ActionChains(dv)
                        action.move_to_element(some_tag).perform()
                        
                        # 열린 제품 페이지에서 이미지 링크 정보를 가져옴
                        large_xpath = '//*[@id="__next"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/div/img'
                        img_url = dv.find_element_by_xpath(
                            large_xpath).get_attribute('src')
                        
                        # 열린 제품 페이지에서 기타 정보를 가져옴
                        div_tag = dv.find_element_by_xpath(
                                '//*[@id="__next"]/div/div[2]/div[2]/div[1]/div[3]')
                        # action = ActionChains(dv)
                        # action.move_to_element(div_tag).perform()

                        func_span_list = div_tag.find_elements_by_class_name('top_cell__3DnEV')

                        for func in func_span_list :
                            some_func = func.text.split(':')[1].strip(' ')
                            main_func.append(some_func)
                except:
                    main_func.append(None)
            else:
                # 광고가 스토어에 연결되는 경우 이미지 링크 정보를 가져옴
                # 광고가 그 외 다른 사이트의 경우 각 사이트마다 레이아웃이 달라 가져올 수 없으므로 예외처리
                try:
                    with webdriver.Chrome(r'/Users/krc/Downloads/chromedriver') as dv:
                        dv.get('{}'.format(name_url))
                        dv.implicitly_wait(5)

                        some_tag = dv.find_element_by_xpath(
                            '//*[@id="content"]/div/div[3]/div[1]')
                        action = ActionChains(dv)
                        action.move_to_element(some_tag).perform()

                        # 광고인 경우 이미지 링크
                        large_xpath = '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/img'
                        img_url = dv.find_element_by_xpath(
                                large_xpath).get_attribute('src')

                        # 광고인 경우 마스크 기능                        
                        div_tag = dv.find_element_by_xpath('//*[@id="INTRODUCE"]/div/div[3]/div/div[2]/div')
                        func_span_list = div_tag.find_elements_by_tag_name('td')
                        func_span_list.pop(-1)

                        for func in func_span_list :
                            main_func.append(func.text)

                except :
                    img_url = None
                    main_func.append(None)

            ''' 기존 섬네일 이미지 링크 가져오는 코드        
            img_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{x}]/li/div/div[1]/div/a/img'
            img_url = driver.find_element_by_xpath(
                img_xpath).get_attribute('src')

            마스크 이미지 저장
            urllib.request.urlretrieve(
                img_url, '.\mask_img\{0}\{1}번 {2}.jpg'.format(i, x, mask_name))'''

            result = [mask_name, review_number,
                      star_rating, price, category, img_url, main_func]
            mask.append(result)

        # DataFrame 변환 후 CSV Export
        data = pd.DataFrame(
            mask, columns=['Name', 'Review', 'Rating', 'Price', 'Category', 'Mask_img', 'Mask_func'])
        # 경로에 파일이 존재하는 경우 append, 존재하지 않는 경우 write mode 사용
        if not os.path.exists('mask_data.csv'):
            data.to_csv('mask_data.csv', index=False,
                        mode='w', encoding='utf-8-sig')
        else:
            data.to_csv('mask_data.csv', index=False, mode='a',
                        encoding='utf-8-sig', header=False)
