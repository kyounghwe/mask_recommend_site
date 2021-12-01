import pymysql


def order_by_review_num():
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='ec2-54-180-30-125.ap-northeast-2.compute.amazonaws.com',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''
            SELECT pk_id, mask_name, mask_review_num
            FROM tb_mask_data
            ORDER BY mask_review_num DESC
            LIMIT 10
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows


def order_by_star_rating_review_num():
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='ec2-54-180-30-125.ap-northeast-2.compute.amazonaws.com',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''
            SELECT pk_id, mask_name, mask_star_rating, mask_review_num, mask_star_rating + mask_review_num*0.00005 as A
            FROM tb_mask_data
            WHERE mask_star_rating between 0 and 5
            ORDER BY A DESC
            LIMIT 20;
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows
