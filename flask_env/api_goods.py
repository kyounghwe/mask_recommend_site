''' api_goods.py

상품상세페이지 / 리뷰쓰기페이지 '''
from flask import Blueprint, render_template, request, session, redirect, url_for
from read_mysql import read_mask_page_data, read_review_data, get_user, get_mask_name
from models import tb_review
from db_connect import db, buffer, engine
import base64
from PIL import Image
import pandas as pd
import cgi

form = cgi.FieldStorage()
goods = Blueprint('goods', __name__)

# 상품상세페이지
@goods.route('/goods')
def goods_info():
    mask_id = request.args.get('data')  # 클릭한 상품의 pk_id
    mask_data_list = read_mask_page_data(mask_id)
    review_list = read_review_data(mask_id)
    ### 이미지 데이터 불러오기
    img_list=[]
    show = tb_review.query.all()
    img_df = pd.read_sql(sql='SELECT * FROM tb_review',con=engine)
    for i in range(len(show)):
        img_str = img_df['img'].values[i]
        stage2 = img_str.decode('utf-8')
        img_list.append(stage2)

    ### 이미 리뷰를 남긴 상품이면 리뷰를 또 남길 수 없게 하기 - 이미 리뷰를 작성하셨습니다 or 리뷰작성버튼비활성화
    if session.get('logged_in'):
        user_id = session['user_id']
        user_id = get_user(user_id)[0][0]
    else:
        user_id = None

    session['mask_id'] = mask_id
    session['user_pk_id'] = user_id

    return render_template('goods.html', mask_data_list=mask_data_list, review_list=review_list, img_data=img_list, user_id=user_id)

@goods.route('/review', methods=["GET", "POST"])
def write_review():
    mask_id = session['mask_id']
    mask_name = get_mask_name(mask_id)[0][0]

    if request.method == "POST":
        ###
        if request.files['review_image']:
            tmp_img_data = request.files['review_image']
        else:
            tmp_img_data = 'static/img/no_image.png'
        im= Image.open(tmp_img_data)
        im.save(buffer, format='png')
        img = base64.b64encode(buffer.getvalue())
        ###
        user_id = session['user_pk_id']
        star_rating = float(request.form['star'])
        review_text = request.form['review_text']
        option1 = int(request.form['option1'])
        option2 = int(request.form['option2'])
        option3 = int(request.form['option3'])
        option4 = int(request.form['option4'])
        review = tb_review(mask_id, user_id, star_rating, review_text, option1, option2, option3, option4, img)
        db.session.add(review)
        ### tb_mask_data 데이터베이스에서 해당 상품의 리뷰수와 별점을 업데이트 하는 코드 추가로 필요
        ## mask_data = temp_goods_info()
        db.session.commit()

        # 데이터 불러오기
        mask_data_list = read_mask_page_data(mask_id)
        review_list = read_review_data(mask_id)
        ### 이미지 데이터 불러오기
        img_list=[]
        show = tb_review.query.all()
        img_df = pd.read_sql(sql='SELECT * FROM tb_review',con=engine)
        for i in range(len(show)):
            img_str = img_df['img'].values[i]
            stage2 = img_str.decode('utf-8')
            img_list.append(stage2)
        return redirect(url_for('goods.goods_info', data=session['mask_id']))
        # return render_template('goods.html', mask_data_list=mask_info_list, review_list=review_list, img_data=img_list, user_id=user_id)
    else:
        return render_template('review.html', mask_data=mask_name)