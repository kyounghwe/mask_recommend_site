from selenium import webdriver
from selenium.webdriver import ActionChains
import pandas as pd
import os


# 크롬 드라이버 경로
driver_path = r'/Users/krc/Downloads/chromedriver'

# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")

# 콤마 제거 및 정수형 변환


def cleaner(something):
    return int(something.replace(',', ''))

def mask_crawling(start, end, page):
    with webdriver.Chrome(driver_path, options=options) as driver:
        # pagingIndex를 통해 크룰링 할 페이지 수 설정 (start, end+1)
        for i in range(start, end+1):
            driver.get(
                'https://search.shopping.naver.com/search/all?frm=NVSHATT&origQuery=%EB%A7%88%EC%8A%A4%ED%81%AC&pagingIndex={}&pagingSize=60&productSet=total&query=%EB%A7%88%EC%8A%A4%ED%81%AC&sort=rel&spec=M10018852%7CM10811849%20M10018852%7CM10811848%20M10018852%7CM10907665%20M10018852%7CM10811847&timestamp=&viewType=list'.format(i))

            # 페이지 내 데이터 로딩 대기
            driver.implicitly_wait(5)

            # 페이지 스크롤 (페이지 당 마스크 개수만큼, Footer 영역까지)
            end_xpath = '//*[@id="__next"]/div/div[3]'
            some_tag = driver.find_element_by_xpath(end_xpath)
            action = ActionChains(driver)
            action.move_to_element(some_tag).perform()

            # 최종 마스크 데이터 리스트
            mask = []

            # 한 페이지에서 원하는 마스크 개수 만큼 설정 (start, end+1)
            for x in range(1, page+1):
                # x번째 마스크로 스크롤
                end_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{x}]/li/div[1]/div[2]/div[5]'
                some_tag = driver.find_element_by_xpath(end_xpath)
                action = ActionChains(driver)
                action.move_to_element(some_tag).perform()

                # 마스크 이미지 로딩 대기
                driver.implicitly_wait(10)

                # 마스크 이름
                name_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{x}]/li/div[1]/div[2]/div[1]'
                mask_name = driver.find_element_by_xpath(name_xpath).text

                # 마스크 리뷰 수
                review_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{x}]/li/div[1]/div[2]/div[5]'
                review_area = driver.find_element_by_xpath(review_xpath)

                # 마스크 별점
                star_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{x}]/li/div[1]/div[2]/div[5]'
                star = driver.find_element_by_xpath(star_xpath)

                # 마스크 가격
                price_list = driver.find_elements_by_class_name('price_num__2WUXn')
                price = price_list[x-1].text
                price = cleaner(price[:-1])

                # 카테고리
                category_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{x}]/li/div[1]/div[2]/div[3]'
                category = driver.find_element_by_xpath(
                    category_xpath+'/a[3]').text

                # 마스크 기능 리스트
                main_func = []

                # 마스크 이름을 기반으로 링크 정보 가져오기
                name_url = driver.find_element_by_xpath(
                    name_xpath).find_element_by_tag_name('a').get_attribute('href')

                # 마스크 이름으로부터 리디렉션되는 링크를 열고, 주소를 확인하여 가격비교와 네이버스토어 제품을 구분
                # .current.url 의 경우 해당 driver가 접속한 url을 가져옴
                with webdriver.Chrome(driver_path, options=options) as dv:
                    dv.get('{}'.format(name_url))
                    dv.implicitly_wait(10)
                    redirect_url = dv.current_url

                # shopping인 경우, 최저가 링크, 이미지, 마스크 기능, 차단지수
                    if 'shopping' in redirect_url:
                        # 메인페이지에서 리뷰 수, 별점 가져오기
                        # 네이버 쇼핑 메인페이지에 리뷰 수와 별점이 있을 경우
                        if '리뷰' in review_area.text and '리뷰별점' in star.text:
                            review_number = driver.find_element_by_xpath(
                                review_xpath+'/a[1]/em[@class="basicList_num__1yXM9"]').text
                            review_number = cleaner(review_number)

                            star_rating = driver.find_element_by_xpath(
                                star_xpath+'/a/span/span[@class="basicList_star__3NkBn"]').text
                            star_rating = float(star_rating[3:])
                        # 네이버 쇼핑 메인페이지에 리뷰 수만 있을 경우
                        elif '리뷰' in review_area.text and '리뷰별점' not in star.text:
                            review_number = driver.find_element_by_xpath(
                                review_xpath+'/a[1]/em[@class="basicList_num__1yXM9"]').text
                            review_number = cleaner(review_number)
                            star_rating = float(0)
                        # 네이버 쇼핑 메인페이지에 별점만 있을 경우
                        elif '리뷰' not in review_area.text and '리뷰별점' in star.text:
                            review_number = 0
                            star_rating = driver.find_element_by_xpath(
                                star_xpath+'/a/span/span[@class="basicList_star__3NkBn"]').text
                            star_rating = float(star_rating[3:])
                        # 네이버 쇼핑 메인페이지에 둘다 없을 경우
                        else:
                            review_number = 0
                            star_rating = float(0)

                        # 마스크 이미지, 차단지수, 기능, 최저가 사이트 url
                        try:
                            # 정보 영역으로 스크롤
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

                            func_span_list = div_tag.find_elements_by_class_name(
                                'top_cell__3DnEV')

                            for func in func_span_list:
                                some_func = func.text.split(':')[1].strip(' ')
                                main_func.append(some_func)

                            # 구매링크
                            purchase_link = name_url

                        except:
                            main_func = None

                    # smartstore인 경우 구매링크, 이미지, 마스크 기능, 차단지수, 별점, 리뷰수
                    elif 'smartstore' in redirect_url:
                        try:
                            # 구매 링크
                            purchase_link = name_url

                            # 마스크 이미지
                            large_xpath = '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/img'
                            img_url = dv.find_element_by_xpath(
                                large_xpath).get_attribute('src')

                            # 마스크 차단지수 및 기능
                            protect_factor_xpath = dv.find_element_by_xpath(
                                '//*[@id="INTRODUCE"]/div/div[3]/div/div[2]/div/table/tbody/tr[1]/td[2]')
                            mask_function_xpath = dv.find_element_by_xpath(
                                '//*[@id="INTRODUCE"]/div/div[3]/div/div[2]/div/table/tbody/tr[2]/td[2]')
                            # 해당 위치로 스크롤
                            action = ActionChains(dv)
                            action.move_to_element(mask_function_xpath).perform()
                            dv.implicitly_wait(10)

                            # 광고인 경우 마스크 기능
                            div_tag = dv.find_element_by_xpath(
                                '//*[@id="INTRODUCE"]/div/div[3]/div/div[2]/div')
                            func_span_list = div_tag.find_elements_by_tag_name(
                                'td')
                            func_span_list.pop(-1)

                            for func in func_span_list:
                                if "1세" not in func.text and "2세" not in func.text and "3세" not in func.text and "4세" not in func.text and "5세" not in func.text and "6세" not in func.text:
                                    if "0개" not in func.text:
                                        main_func.append(func.text)

                            # 별점
                            star_location = dv.find_element_by_xpath(
                                '//*[@id="content"]/div/div[2]/div[1]/div[2]').text
                            star_rating_find = star_location.find('평점')
                            if star_rating_find != -1:
                                star_rating = star_location[star_rating_find +
                                                            2:-3].strip('\n')
                                star_rating = float(star_rating)
                            else:
                                star_rating = float(0)

                            # 리뷰 수
                            review_location = dv.find_element_by_xpath(
                                '//*[@id="content"]/div/div[2]/div[1]/div[2]').text

                            review_number_find = review_location.find('사용자')
                            if review_number_find != -1:
                                review_number = review_location[3:review_number_find]
                                review_number = cleaner(review_number)
                            else:
                                review_number = 0
                        except:
                            purchase_link = name_url
                            main_func = None
                            star_rating = float(0)
                            review_number = 0
                    else:
                        purchase_link = name_url
                        main_func = None
                        star_rating = float(0)
                        review_number = 0

                if main_func:
                    main_func.sort()

                    if len(main_func) != 0:
                        if "KF" in main_func[0]:
                            protect_factor = main_func[0]
                            main_func = main_func[1:]

                            mask_func = "@".join(main_func)
                            func_result = mask_func.replace(", ", "@")
                        else:
                            protect_factor = None
                            mask_func = "@".join(main_func)
                            func_result = mask_func.replace(", ", "@")
                    else:
                        protect_factor = None
                        func_result = None
                else:
                    protect_factor = None
                    func_result = None

                result = [mask_name, review_number,
                        star_rating, price, category, protect_factor, func_result, img_url, purchase_link]
                mask.append(result)

            # DataFrame 변환 후 CSV Export
            data = pd.DataFrame(
                mask, columns=['Name', 'Review', 'Rating', 'Price', 'Category', 'Protect_factor', 'Mask_func', 'Mask_img', 'Purchase_link'])
            # 경로에 파일이 존재하는 경우 append, 존재하지 않는 경우 write mode 사용
            if not os.path.exists('mask_data.csv'):
                data.to_csv('mask_data.csv', index=False,
                            mode='w', encoding='utf-8-sig')
            else:
                data.to_csv('mask_data.csv', index=False, mode='a',
                            encoding='utf-8-sig', header=False)

mask_crawling(10,11,10)
