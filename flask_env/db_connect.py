#이미지 데이터베이스에서 읽기
# import io
# import os
# import PIL
from io import BytesIO

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pymysql

db = SQLAlchemy()

conn = pymysql.connect(host='127.0.0.1', user='root', password='5452tulahyo12!A', database='try_mysql', port=3306, charset='utf8')
cursor = conn.cursor()

#이미지 저장
buffer = BytesIO()
engine = create_engine('mysql+pymysql://root:5452tulahyo12!A@localhost:3306/try_mysql', echo=False)

# def db_connector():
#     sql = '''SELECT * FROM try_mysql.tb_user_info'''
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     conn.close()
#     return str(result)

# def Mask_CSV():
#     mask = '''SELECT * FROM try_mysql.tb_mask_data'''
#     cursor.execute(mask)
#     r = cursor.fetchall()
#     conn.close()
#     return r