import pymysql


def select_category(data):
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='ec2-54-180-30-125.ap-northeast-2.compute.amazonaws.com',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    if data[-1] == '':  # 추천 안함
        sql = 'SELECT mask_name, mask_price, mask_star_rating, mask_img_link, pk_id FROM tb_mask_data WHERE '
        sen = ''
        mask_category_list = [
            'mask_category', 'mask_blocking_grade', 'mask_function', 'mask_price']
        for i in range(len(mask_category_list)):
            if i < 2 and data[i]:
                sen_temp = f'''{mask_category_list[i]} LIKE "{data[i]}"'''
                if sen == '':
                    sen = sen + sen_temp
                else:
                    sen = sen + ' AND ' + sen_temp
            elif i == 2 and data[i]:
                for j in range(8):
                    if data[i][j]:
                        sen_temp = f'''{mask_category_list[i]} LIKE "%{data[i][j]}%"'''
                        if sen == '':
                            sen = sen + sen_temp
                        else:
                            sen = sen + ' AND ' + sen_temp
            elif i == 3 and data[i][1]:
                sen_temp = f'''{mask_category_list[i]} between {data[i][0]} and {data[i][1]}'''
                if sen == '':
                    sen = sen + sen_temp
                else:
                    sen = sen + ' AND ' + sen_temp
        sql = sql + sen
    else:  # join, orderby 들어가야 함
        sql = 'SELECT B.mask_name, B.mask_price, B.mask_star_rating, B.mask_img_link, B.pk_id FROM tb_review_keyword as A JOIN tb_mask_data as B ON A.pk_id = B.pk_id WHERE '
        sen = ''
        mask_category_list = [
            'mask_category', 'mask_blocking_grade', 'mask_function', 'mask_price']
        for i in range(len(mask_category_list)):
            if i < 2 and data[i]:
                sen_temp = f'''B.{mask_category_list[i]} LIKE "{data[i]}"'''
                if sen == '':
                    sen = sen + sen_temp
                else:
                    sen = sen + ' AND ' + sen_temp
            elif i == 2 and data[i]:
                for j in range(8):
                    if data[i][j]:
                        sen_temp = f'''B.{mask_category_list[i]} LIKE "%{data[i][j]}%"'''
                        if sen == '':
                            sen = sen + sen_temp
                        else:
                            sen = sen + ' AND ' + sen_temp
            elif i == 3 and data[i][1]:
                sen_temp = f'''B.{mask_category_list[i]} between {data[i][0]} and {data[i][1]}'''
                if sen == '':
                    sen = sen + sen_temp
                else:
                    sen = sen + ' AND ' + sen_temp
        sen = sen + f' ORDER BY A.{data[-1]} DESC'
        sql = sql + sen
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows


def select_keyword(data):
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='ec2-54-180-30-125.ap-northeast-2.compute.amazonaws.com',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''
        SELECT B.mask_name, B.mask_price, B.mask_star_rating, B.mask_img_link, B.pk_id
        FROM tb_review_keyword as A
        JOIN tb_mask_data as B
        ON A.pk_id = B.pk_id
        ORDER BY A.{data} DESC
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows
