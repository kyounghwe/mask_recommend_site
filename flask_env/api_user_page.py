''' api_user_page.py
로그인 된 회원만 들어갈 수 있는 페이지들
마이페이지 / 마이페이지-리뷰목록 / 마이페이지-찜목록 '''
from flask import Blueprint, render_template, request, redirect, url_for, session
from read_mysql import get_user, get_my_review, get_my_zzim
from read_mysql_for_admin import review_delete, modify_review_img, modify_review_content, zzim_delete

from db_connect import engine, buffer
import pandas as pd
import base64
from PIL import Image

user_page = Blueprint('user_page', __name__)

@user_page.route("/mypage")
def mypage():
    user_id = session['user_id']
    return render_template('my_page.html', user_id=user_id)

@user_page.route("/myreview", methods=["GET","POST"])
def myreview():
    if request.method == "GET":
        user_num_id = get_user(session['user_id'])[0][0]
        user_review_list = get_my_review(user_num_id)  # mask_id, star_rating, review_text, img, pk_id(리뷰)
        user_review_img = []
        for i in range(len(user_review_list)):
            user_review_img.append(user_review_list[i][-2].decode('utf-8'))  # 이미지 디코드
        return render_template('my_page_review.html', user_review_list=user_review_list, user_review_img=user_review_img)
    
    else:  # 삭제 버튼 누른 경우
        if request.form['delete']:
            r_id = request.form['r_id']
            review_delete(r_id)
        return redirect(url_for('user_page.myreview'))

@user_page.route("/modify_review", methods=["GET","POST"])
def modify_review():
    if request.method == 'POST':
        r_id = request.form['r_id']
        if not request.files.get('review_image'):
            img_data = '/root/mask/flask_env/static/img/no_image.png'
        else:
            tmp_img_data = request.files['review_image']
            im= Image.open(tmp_img_data)
            im.save(buffer, format='png')
            img_data = base64.b64encode(buffer.getvalue())
            modify_review_img(img_data,r_id)
        
        star = request.form['star']
        r_text = request.form['review_text']
        r_op1 = request.form['option1']
        r_op2 = request.form['option2']
        r_op3 = request.form['option3']
        r_op4 = request.form['option4']
        modify_review_content([star, r_text, r_op1, r_op2, r_op3, r_op4, r_id])
        return redirect(url_for('user_page.myreview'))
    elif request.method == 'GET':
        r_id = request.args.get('r_id')
        review_info = pd.read_sql(sql='SELECT * FROM tb_review where pk_id=%s'%r_id, con=engine)
        mask_id = review_info['mask_id'].values[0]
        return render_template('modify_review.html', mask_data=mask_id, r_id=r_id)

@user_page.route("/myzzim", methods=["GET","POST"])
def myzzim():
    if request.method == "GET":
        user_num_id = get_user(session['user_id'])[0][0]
        user_zzim_list = get_my_zzim(user_num_id)  # mask_name, pk_id(리뷰), pk_id(마스크)
        return render_template('my_page_zzim.html', user_zzim_list=user_zzim_list)
    
    else:  # 삭제 버튼 누른 경우
        if request.form['delete']:
            r_id = request.form['r_id']
            zzim_delete(r_id)
        return redirect(url_for('user_page.myzzim'))