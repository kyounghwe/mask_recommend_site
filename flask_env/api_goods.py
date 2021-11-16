from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from read_mysql import read_mask_page_data
from db_connect import db

goods = Blueprint('goods', __name__)

# 상품상세페이지
### 상품 클릭하면 그에 맞게 따로따로 정보가 나와야 함
@goods.route('/goods')
def goods_info():
    data = request.args.get('data')  # 클릭한 상품의 pk_id
    mask_info_list = read_mask_page_data(data)
    return render_template('goods.html', mask_info_list=mask_info_list)