import pymysql

def select_category(data):  # tb_mask_data테이블과 join해야함 - 마스크이름 얻기
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
            WHERE mask_category LIKE '{data}'
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows