'''
mysql
    -> try_mysql 데이터베이스
        -> tb_user_info 테이블 *
        -> tb_goods_info 테이블 (temp)
        -> tb_review 테이블
        -> tb_zzim 테이블
'''
from flask import Flask
from db_connect import db

from api_user import user
from api_goods import goods
from api_user_page import user_page
from api_admin_page import admin_page

app = Flask(__name__)
db.init_app(app)

# 'mysql+pymysql://root:<나의mysql비밀번호>@localhost:3306/<내가쓰려는데이터베이스이름>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:3-[z>g9UNk[f-X&EKdW&@localhost:3306/try_mysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the random string'  # session 실행하려면 시크릿키 필요!

app.register_blueprint(user)
app.register_blueprint(goods)
app.register_blueprint(user_page)
app.register_blueprint(admin_page)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
