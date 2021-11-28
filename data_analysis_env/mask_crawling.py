from selenium import webdriver
from selenium.webdriver import ActionChains

import pandas as pd
import os
import re
import emoji

# 크롬 드라이버 경로
driver_path = r'C:\Users\chromedriver'

# 옵션 생성
# 백그라운드 실행 시 각 크롬드라이버에 options=options 추가
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 콤마 제거 및 정수형 변환
def cleaner(something):
    return int(something.replace(',', ''))

# 리뷰 특수문자, 이모지 제거
def cleanReview(review_list):
    string = " ".join(review_list)

    # 텍스트에 포함되어 있는 특수 문자 제거
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', string)
    
    # 텍스트에 포함되어 있는 이모지 제거 후 리턴
    return emoji.get_emoji_regexp().sub(u'', text)

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
                price_list = driver.find_elements_by_class_name(
                    'price_num__2WUXn')
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
                    if 'shopping.naver' in redirect_url:
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

                        # 구매링크
                        purchase_link = redirect_url

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

                        except:
                            main_func = None

                        try:
                            # 마스크 리뷰 위치로 스크롤
                            mask_review_end_xpath = dv.find_element_by_xpath(
                                '//*[@id="section_recommend"]/h3')
                            dv.implicitly_wait(10)
                            action = ActionChains(dv)
                            action.move_to_element(mask_review_end_xpath).perform()
                            
                            # 마스크 리뷰 리스트 생성
                            mask_review_list = []

                            # 동작 환경에 맞추어 대기시간 설정 (implicitly_wait)
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
                                            user_review = dv.find_element_by_xpath(
                                                mask_review_xpath).text
                                            mask_review_list.append(
                                                user_review.replace("\n", ""))
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
                                            user_review = dv.find_element_by_xpath(
                                                mask_review_xpath).text
                                            mask_review_list.append(
                                                user_review.replace("\n", ""))
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

                                        elif review_page == 12 and dv.find_element_by_xpath('//*[@id="section_review"]/div[3]/a[11]').text.replace('현재 페이지\n', '') == '20':
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
                                            user_review = dv.find_element_by_xpath(
                                                mask_review_xpath).text
                                            mask_review_list.append(
                                                user_review.replace("\n", ""))
                                            review_num += 1
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
                                            user_review = dv.find_element_by_xpath(
                                                mask_review_xpath).text
                                            mask_review_list.append(
                                                user_review.replace("\n", ""))
                                            review_num += 1
                                        except:
                                            break
                                # 리뷰가 없는 경우
                                except:
                                    mask_review_list = None

                    # smartstore인 경우 구매링크, 이미지, 별점, 리뷰수, 기능, 리뷰
                    elif 'smartstore.naver' in redirect_url:
                        try:
                            # 구매 링크
                            purchase_link = redirect_url

                            # 마스크 이미지
                            large_xpath = '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/img'
                            img_url = dv.find_element_by_xpath(
                                large_xpath).get_attribute('src')

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

                            # 마스크 기능 (해당 클래스 요소 중 2번째)
                            function_class = dv.find_elements_by_class_name('_1_UiXWHt__')[1]
                            # 해당 위치로 스크롤
                            dv.implicitly_wait(5)
                            action = ActionChains(dv)
                            action.move_to_element(function_class).perform()
 
                            func_span_list = function_class.find_elements_by_tag_name(
                                'td')
                                
                            for func in func_span_list:
                                if "1세" not in func.text and "2세" not in func.text and "3세" not in func.text and "4세" not in func.text and "5세" not in func.text and "6세" not in func.text:
                                    if "0개" not in func.text:
                                        main_func.append(func.text)
                        except:
                            purchase_link = redirect_url
                            main_func = None

                        try:   
                            # 리뷰
                            mask_review_end_xpath = dv.find_element_by_xpath(
                                '//*[@id="QNA"]/div/h3')

                            mask_review_page_xpath = dv.find_element_by_xpath(
                                '//*[@id="REVIEW"]/div/div[3]/div/div[2]/div/div')

                            # 해당 위치로 스크롤
                            dv.implicitly_wait(5)
                            action = ActionChains(dv)
                            action.move_to_element(
                                mask_review_end_xpath).perform()
                            
                            mask_review_list = []

                            # 리뷰가 있는 경우
                        
                            # review_page: 리뷰 page의 a태그 index  (1page=2, 2page=3,..., 10page=11, 이전버튼=1, 다음버튼=12)
                            review_page = 2
                            # 리뷰 크롤링 시작
                            while True:
                                # review_num: 리뷰의 li태그 index
                                review_num = 1
                                while True:
                                    try:
                                        mask_review_xpath = f'//*[@id="REVIEW"]/div/div[3]/div/div[2]/ul/li[{review_num}]/div/div/div/div[1]/div/div[1]/div[2]/div'
                                        user_review = dv.find_element_by_xpath(
                                            mask_review_xpath).text
                                        mask_review_list.append(
                                            user_review.replace("\n", ""))
                                        review_num += 1
                                    except:
                                        break
                                # 크롤링을 원하는 페이지까지 도달할때까지 반복, 페이지의 수가 원하는 페이지의 수 미만이라면 break
                                try:
                                    review_page += 1
                                    if review_page != 12:
                                        current_page = dv.find_element_by_xpath(
                                            '//*[@id="REVIEW"]/div/div[3]/div/div[2]/div/div/a[{}]'.format(review_page))
                                        current_page.click()
                                        review_num = 1
                                        dv.implicitly_wait(10)
                                        action = ActionChains(dv)
                                        action.move_to_element(
                                            mask_review_page_xpath).perform()
                                        
                                    # 크롤링 원하는 페이지 지정
                                    elif review_page == 12 and dv.find_element_by_xpath('//*[@id="REVIEW"]/div/div[3]/div/div[2]/div/div/a[11]').text.replace('현재 페이지\n', '') == '20':
                                        break
                                    # 다음 버튼 클릭
                                    else:
                                        next_page = dv.find_element_by_xpath(
                                            '//*[@id="REVIEW"]/div/div[3]/div/div[2]/div/div/a[12]')
                                        next_page.click()
                                        dv.implicitly_wait(10)
                                        action = ActionChains(dv)
                                        action.move_to_element(
                                            mask_review_page_xpath).perform()
                                        review_page = 2
                                        
                                except:
                                    break
                        # 리뷰가 없을 때
                        except:
                            mask_review_list = None
                    else:
                        review_number = 0
                        star_rating = 0.0
                        price = 0
                        category = None
                        protect_factor = None
                        func_result = None
                        img_url = None
                        purchase_link = None
                        mask_review_list = None

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

                if mask_review_list:
                    mask_review_list = cleanReview(mask_review_list)

                result = [mask_name, review_number,
                        star_rating, price, category, protect_factor, func_result, img_url, purchase_link, mask_review_list]
                mask.append(result)
                # 출력 테스트 코드
                print(redirect_url, len(mask_review_list))

            # DataFrame 변환 후 CSV Export
            data = pd.DataFrame(
                mask, columns=['Name', 'Review', 'Rating', 'Price', 'Category', 'Protect_factor', 'Mask_func', 'Mask_img', 'Purchase_link', 'Mask_review'])
            # 경로에 파일이 존재하는 경우 append, 존재하지 않는 경우 write mode 사용
            if not os.path.exists('mask_data.csv'):
                data.to_csv('mask_data.csv', index=False,
                            mode='w', encoding='utf-8-sig')
            else:
                data.to_csv('mask_data.csv', index=False, mode='a',
                            encoding='utf-8-sig', header=False)

mask_crawling(1, 1, 4)
