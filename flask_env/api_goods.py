from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
# from models import tb_user_info
# from db_connect import db

goods = Blueprint('goods', __name__)

# 상품상세페이지
### 상품 클릭하면 그에 맞게 따로따로 정보가 나와야 함
@goods.route('/goods')
def goods_info():
    return render_template('goods.html')