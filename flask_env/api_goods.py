''' api_goods.py

상품상세페이지 / 리뷰쓰기페이지 '''
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from read_mysql import read_mask_page_data, read_review_data, get_user, get_mask_name
from read_mysql_for_admin import make_zzim
from models import tb_review, tb_zzim
from db_connect import db, buffer, engine
import base64
from PIL import Image
import pandas as pd
import cgi

form = cgi.FieldStorage()
goods = Blueprint('goods', __name__)

# 상품상세페이지
@goods.route('/goods', methods=["GET","POST"])
def goods_info():
    if request.method == "GET":
        if request.args.get('data'):
            mask_id = request.args.get('data')  # 클릭한 상품의 pk_id
        else:
            mask_id = session['mask_id']
        mask_data_list = read_mask_page_data(mask_id)
        review_list = read_review_data(mask_id)
        option = []
        option_list = []
        for i in review_list:  # 5,6,7,8
            # 부드러움
            if i[5] == 1: option_list.append('매우뻣뻣')
            elif i[5] == 2: option_list.append('뻣뻣')
            elif i[5] == 3: option_list.append('보통')
            elif i[5] == 4: option_list.append('좋음')
            elif i[5] == 5: option_list.append('매우좋음')
            # 크기
            if i[6] == 1: option_list.append('매우작음')
            elif i[6] == 2: option_list.append('작음')
            elif i[6] == 3: option_list.append('보통')
            elif i[6] == 4: option_list.append('큼')
            elif i[6] == 5: option_list.append('매우큼')
            # 내구성
            if i[7] == 1: option_list.append('매우나쁨')
            elif i[7] == 2: option_list.append('나쁨')
            elif i[7] == 3: option_list.append('보통')
            elif i[7] == 4: option_list.append('좋음')
            elif i[7] == 5: option_list.append('매우좋음')
            # 숨쉬기
            if i[8] == 1: option_list.append('매우나쁨')
            elif i[8] == 2: option_list.append('나쁨')
            elif i[8] == 3: option_list.append('보통')
            elif i[8] == 4: option_list.append('좋음')
            elif i[8] == 5: option_list.append('매우좋음')
            option.append(option_list)
            option_list = []
        
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

        return render_template('goods.html', mask_data_list=mask_data_list, review_list=review_list, option=option, img_data=img_list, user_id=user_id)
    else:  # 찜
        mask_id = session['mask_id']
        user_id = session['user_pk_id']
        try:
            mask = tb_zzim.query.filter(tb_zzim.mask_id == mask_id).all()
            if mask:
                mask = tb_zzim.query.filter(tb_zzim.user_id == user_id).first()
                if mask:
                    flash('이미 찜한 상품입니다.')
                    return redirect(url_for('goods.goods_info'))
                else:
                    make_zzim(mask_id,user_id)
            else:
                make_zzim(mask_id,user_id)
        except:
            pass
        return redirect(url_for('goods.goods_info'))

@goods.route('/review', methods=["GET", "POST"])
def write_review():
    mask_id = session['mask_id']
    mask_name = get_mask_name(mask_id)[0][0]

    if request.method == "POST":
        if request.files['review_image']:
            tmp_img_data = request.files['review_image']
            im= Image.open(tmp_img_data)
            im.save(buffer, format='png')
            img = base64.b64encode(buffer.getvalue())

        else:
            tmp_img_data = 'static/img/no_image.png'
            im= Image.open(tmp_img_data)
            im.save(buffer, format='png')
            img = base64.b64encode(buffer.getvalue())

        user_id = session['user_pk_id']
        star_rating = float(request.form['star'])
        review_text = request.form['review_text']
        option1 = int(request.form['option1'])
        option2 = int(request.form['option2'])
        option3 = int(request.form['option3'])
        option4 = int(request.form['option4'])
        review = tb_review(mask_id, user_id, star_rating, review_text, option1, option2, option3, option4, img)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('goods.goods_info', data=session['mask_id']))
    else:
        return render_template('review.html', mask_data=mask_name)