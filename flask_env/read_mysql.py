import pymysql

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
            SELECT mask_name, mask_price, mask_star_rating, mask_img_link, pk_id
            FROM tb_mask_data
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
            SELECT mask_name, mask_price, mask_star_rating, mask_img_link, mask_purchase_link
            FROM tb_mask_data
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
            SELECT *
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
            from tb_mask_data
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

def get_my_review(data):
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='127.0.0.1',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''
            SELECT b.mask_name, a.star_rating, a.review_text, a.img, a.pk_id
            FROM tb_review AS a
            INNER JOIN tb_mask_data AS b
            ON a.mask_id = b.pk_id
            WHERE a.user_id LIKE '{data}'
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows

def get_my_zzim(data):
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='127.0.0.1',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''
            SELECT b.mask_name, a.pk_id
            FROM tb_zzim AS a
            INNER JOIN tb_mask_data AS b
            ON a.mask_id = b.pk_id
            WHERE a.user_id LIKE {data}
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows