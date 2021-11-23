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
    sql = 'SELECT mask_name, mask_price, mask_star_rating, mask_img_link, pk_id FROM tb_mask_data WHERE '
    sen = ''
    mask_category_list = ['mask_category','mask_blocking_grade','mask_function','mask_price']
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
        elif i == 3 and data[i]:
            sen_temp = f'''{mask_category_list[i]} between {data[i][0]} and {data[i][1]}'''
            if sen == '':
                sen = sen + sen_temp
            else:
                sen = sen + ' AND ' + sen_temp
    sql = sql + sen
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows