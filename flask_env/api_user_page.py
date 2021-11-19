''' api_user_page.py
로그인 된 회원만 들어갈 수 있는 페이지들
마이페이지 / 마이페이지-리뷰목록 / 마이페이지-찜목록 '''
from flask import Blueprint, render_template, request, redirect, url_for, session
from read_mysql import get_user, get_mask_name, get_my_review
# 유저 테이블, 리뷰 테이블, 찜 테이블 필요
from models import tb_user_info
from db_connect import db

user_page = Blueprint('user_page', __name__)

@user_page.route("/mypage")
def mypage():
    user_id = session['user_id']
    return render_template('my_page.html', user_id=user_id)

@user_page.route("/myreview")
def myreview():
    user_num_id = get_user(session['user_id'])[0][0]
    user_review_list = get_my_review(user_num_id)  # mask_id, star_rating, review_text, img
    return render_template('my_page_review.html', user_review_list=user_review_list)