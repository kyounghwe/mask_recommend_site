import pymysql

def order_by_review_num():
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='0.0.0.0',
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
        host='0.0.0.0',
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

def review_delete(data):
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='0.0.0.0',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''DELETE FROM tb_review where pk_id={data}'''
    cursor.execute(sql)
    mask_db.commit()
    mask_db.close()
    return None

def review_delete(data):
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='0.0.0.0',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''DELETE FROM tb_review where pk_id={data}'''
    cursor.execute(sql)
    mask_db.commit()
    mask_db.close()
    return None

def modify_review_img(data1,data2):
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='0.0.0.0',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''UPDATE tb_review SET img={data1} where pk_id={data2}'''
    cursor.execute(sql)
    mask_db.commit()
    mask_db.close()
    return None

def modify_review_content(data):
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='0.0.0.0',
        db='try_mysql',
        charset='utf8'
    )
    print(data)
    cursor = mask_db.cursor()
    sql = f'''
            UPDATE tb_review 
            SET star_rating = {data[0]},
                review_text = "{data[1]}",
                option1 = {data[2]},
                option2 = {data[3]},
                option3 = {data[4]},
                option4 = {data[5]}
            WHERE pk_id = {data[6]}
        '''
    cursor.execute(sql)
    mask_db.commit()
    mask_db.close()
    return None

def zzim_delete(data):
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='0.0.0.0',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''DELETE FROM tb_zzim where pk_id={data}'''
    cursor.execute(sql)
    mask_db.commit()
    mask_db.close()
    return None

def make_zzim(data1, data2):
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='0.0.0.0',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f''' INSERT INTO tb_zzim(mask_id, user_id) VALUES({data1}, {data2})'''
    cursor.execute(sql)
    mask_db.commit()
    mask_db.close()
    return None