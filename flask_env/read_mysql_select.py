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
        elif i == 3 and data[i][1]:
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

# def save_selected_category(temp):
#     data = []
#     for i in temp:
#         if type(i) is list:
#             for j in i:
#                 if j == None:
#                     data.append('')
#                 else:
#                     data.append(j)
#         else:
#             if i == None:
#                 data.append('')
#             else:
#                 data.append(i)
#     a = data[0]
#     b = data[1]
#     c = data[2]
#     d = data[3]
#     e = data[4]
#     f = data[5]
#     g = data[6]
#     h = data[7]
#     i = data[8]
#     j = data[9]
#     k = data[10]
#     mask_db = pymysql.connect(
#         user='root',
#         passwd='5452tulahyo12!A',
#         host='127.0.0.1',
#         db='try_mysql',
#         charset='utf8'
#     )
#     cursor = mask_db.cursor()
#     sql = f'''
#             TRUNCATE selected_category
#         '''
#     cursor.execute(sql)
#     mask_db.commit()
#     sql = f'''
#             INSERT INTO selected_category VALUES("{a}","{b}","{c}","{d}","{e}","{f}","{g}","{h}","{i}","{j}","{k}")
#         '''
#     cursor.execute(sql)
#     mask_db.commit()
#     mask_db.close()
#     return None

def get_selected_category():
    mask_db = pymysql.connect(
        user='root',
        passwd='5452tulahyo12!A',
        host='127.0.0.1',
        db='try_mysql',
        charset='utf8'
    )
    cursor = mask_db.cursor()
    sql = f'''
            SELECT * FROM selected_category
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    mask_db.close()
    return rows