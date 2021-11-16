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
    sql = f'''
            SELECT mask_name, mask_price, mask_star_rating, mask_img
            FROM temp_mask_info
            WHERE pk_id LIKE {data}
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows