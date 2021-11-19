'''
마스크 메인페이지에 넣을 마스크이미지, 마스크이름, 가격, 별점을 mysql 데이터베이스에서 불러오는 코드
api_user.py에서 home과 관련됨
'''
import pymysql
import pandas as pd

def read_mask_data():
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='127.0.0.1',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''
            SELECT mask_name, mask_price, mask_star_rating, mask_img, pk_id
            FROM temp_mask_info
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows

def read_mask_page_data(data):
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='127.0.0.1',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    # 나중에 구매링크 컬럼도 끝에 추가하기
    sql = f'''
            SELECT mask_name, mask_price, mask_star_rating, mask_img
            FROM temp_mask_info
            WHERE pk_id LIKE {data}
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows

def read_review_data(data):  # 리뷰데이터: 이미지 뺀 나머지 컬럼 모두 불러옴
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='127.0.0.1',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''
            SELECT pk_id, mask_id, user_id, star_rating, review_text, option1, option2, option3, option4
            FROM tb_review
            WHERE mask_id LIKE {data}
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows

def get_mask_name(data):
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='127.0.0.1',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''
            select mask_name
            from temp_mask_info
            where pk_id LIKE {data}
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows

def get_user(data):
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='127.0.0.1',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''
            SELECT pk_id 
            FROM tb_user_info 
            WHERE user_id LIKE '{data}'
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows

def get_my_review(data):  # temp_mask_info테이블과 join해야함 - 마스크이름 얻기
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='127.0.0.1',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''
            SELECT mask_id, star_rating, review_text, img
            FROM tb_review 
            WHERE user_id LIKE '{data}'
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows