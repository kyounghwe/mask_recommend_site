''' api_user.py

메인 / 회원가입 / 로그인 / 로그아웃 '''
from flask import Blueprint, render_template, request, redirect, url_for, session, make_response
from models import tb_user_info
from db_connect import db
from read_mysql import read_mask_data
from read_mysql_select import select_category, select_keyword

user = Blueprint('user', __name__)

# 메인 페이지
@user.route('/', methods=["GET", "POST", "PUT"])
def home():
    # 로그인 여부 확인
    if not session.get('logged_in'): session['check'] = 0
    
    # 쿠키로 선택한 카테고리 데이터 가져오기
    try:
        data = [
            request.cookies.get('mask_category'),
            request.cookies.get('mask_blocking_grade'),
            [request.cookies.get('mask_function_1'),request.cookies.get('mask_function_2'),request.cookies.get('mask_function_3'),request.cookies.get('mask_function_4'),request.cookies.get('mask_function_5'),request.cookies.get('mask_function_6'),request.cookies.get('mask_function_7'),request.cookies.get('mask_function_8')],
            request.cookies.get('mask_price'),
            request.cookies.get('recommend')
        ]
        mask_category = [data[0] if data[0] not in ['None', None] else ''][0]
        mask_blocking_grade = [data[1] if data[1] not in ['None', None] else ''][0]
        mask_function = []
        for i in data[2]:
            if i in ['None', None]:
                mask_function.append('')
            else:
                mask_function.append(i)
        try: 
            mask_price = list(map(int, data[3].split(":")))
        except:
            mask_price = ['','']
        if data[-1] in ['None', None]:
            recommend = ''
        else:
            recommend = data[-1]
    except:
        mask_category = ''
        mask_blocking_grade = ''
        mask_function = ['','','','','','','','']
        mask_price = ['','']
        recommend = ''

    # 선택한 카테고리로 마스크데이터 필터해서 가져오기
    checked_list = [mask_category, mask_blocking_grade, mask_function, mask_price, recommend]
    if checked_list[:-1] != ['', '', ['','','','','','','',''], ['','']]:
        mask_list = select_category(checked_list)
        checked_list_for_html = []
        for i in checked_list[:-1]:
            if not i:
                continue
            if type(i) is list:
                for j in i:
                    if j:
                        checked_list_for_html.append(j)
            else:
                checked_list_for_html.append(i)
        if checked_list[-2] != ['','']:
            if checked_list_for_html[-1] == 999999999:
                temp = "20000원 이상"
            elif checked_list_for_html[-1] == 1000:
                temp = "0 ~ 1000원"
            else:
                temp = " ~ ".join(list(map(str, checked_list_for_html[-2:]))) + '원'
            checked_list_for_html = checked_list_for_html[:-2]
            checked_list_for_html.append(temp)
            if checked_list[-1] == 'keyword1':
                checked_list_for_html.append('편안함')
            elif checked_list[-1] == 'keyword2':
                checked_list_for_html.append('빠른배송')
            elif checked_list[-1] == 'keyword3':
                checked_list_for_html.append('재구매')
            elif checked_list[-1] == 'keyword4':
                checked_list_for_html.append('가성비')
            elif checked_list[-1] == 'keyword5':
                checked_list_for_html.append('부드러움')
    elif checked_list[:-1] == ['', '', ['','','','','','','',''], ['','']] and checked_list[-1] != '':  # 카테고리 없고, 개인선호(추천)만 이용
        mask_list = select_keyword(checked_list[-1])
        checked_list_for_html = []
        if checked_list[-1] == 'keyword1':
            checked_list_for_html.append('편안함')
        elif checked_list[-1] == 'keyword2':
            checked_list_for_html.append('빠른배송')
        elif checked_list[-1] == 'keyword3':
            checked_list_for_html.append('재구매')
        elif checked_list[-1] == 'keyword4':
            checked_list_for_html.append('가성비')
        elif checked_list[-1] == 'keyword5':
            checked_list_for_html.append('부드러움')
    else:  # 선택한 카테고리가 없는 경우 마스크데이터 그냥 가져오기
        checked_list = None
        checked_list_for_html = None
        mask_list = read_mask_data()
    
    # 페이징
    page = request.args.get('page')
    if page != None:
        page = int(page)
        if session['page_num'] - page == 1 and session['page_num'] > 0:  # prev페이지로 갈 때
            session['page_num'] -= 1
        elif session['page_num'] - page == -1 and session['page_num'] < len(mask_list)//16:  # next페이지로 갈 때
            session['page_num'] += 1
    else:
        session['page_num'] = 0
    mask_list = mask_list[session['page_num']*16:session['page_num']*16 + 16]
    
    return render_template("main.html", check=session['check'], mask_list=mask_list, page_num=session['page_num'], checked_list=checked_list_for_html)

# 쿠키 세팅
@user.route("/setcookie", methods=["POST"])
def setcookie():
    if request.method == "POST":
        resp = make_response(redirect(url_for('user.home')))
        try: resp.set_cookie('mask_category', request.form.get('mask_category')) 
        except: resp.set_cookie('mask_category', 'None')
        try: resp.set_cookie('mask_blocking_grade', request.form.get('mask_blocking_grade'))
        except: resp.set_cookie('mask_blocking_grade', 'None')
        try: resp.set_cookie('mask_function_1', request.form.get('mask_function_1'))
        except: resp.set_cookie('mask_function_1', 'None')
        try: resp.set_cookie('mask_function_2', request.form.get('mask_function_2'))
        except: resp.set_cookie('mask_function_2', 'None')
        try: resp.set_cookie('mask_function_3', request.form.get('mask_function_3'))
        except: resp.set_cookie('mask_function_3', 'None')
        try: resp.set_cookie('mask_function_4', request.form.get('mask_function_4'))
        except: resp.set_cookie('mask_function_4', 'None')
        try: resp.set_cookie('mask_function_5', request.form.get('mask_function_5'))
        except: resp.set_cookie('mask_function_5', 'None')
        try: resp.set_cookie('mask_function_6', request.form.get('mask_function_6'))
        except: resp.set_cookie('mask_function_6', 'None')
        try: resp.set_cookie('mask_function_7', request.form.get('mask_function_7'))
        except: resp.set_cookie('mask_function_7', 'None')
        try: resp.set_cookie('mask_function_8', request.form.get('mask_function_8'))
        except: resp.set_cookie('mask_function_8', 'None')
        try: resp.set_cookie('mask_price', request.form.get('mask_price')) 
        except: resp.set_cookie('mask_price', 'None')
        try: resp.set_cookie('recommend', request.form.get('recommend')) 
        except: resp.set_cookie('recommend', 'None')
        return resp
# 쿠키 리셋
@user.route("/resetcookie", methods=["POST"])
def resetcookie():
    if request.method == "POST":
        resp = make_response(redirect(url_for('user.home')))
        resp.set_cookie('mask_category', 'None')
        resp.set_cookie('mask_blocking_grade', 'None')
        resp.set_cookie('mask_function_1', 'None')
        resp.set_cookie('mask_function_2', 'None')
        resp.set_cookie('mask_function_3', 'None')
        resp.set_cookie('mask_function_4', 'None')
        resp.set_cookie('mask_function_5', 'None')
        resp.set_cookie('mask_function_6', 'None')
        resp.set_cookie('mask_function_7', 'None')
        resp.set_cookie('mask_function_8', 'None')
        resp.set_cookie('mask_price', 'None')
        resp.set_cookie('recommend', 'None')
        return resp

# 회원가입 페이지
### 아이디와 비밀번호 조건 추가해야 함 -> 조건에 맞지 않으면 alert
### 비밀번호 저장할 때 암호화해서 집어넣기
@user.route('/join', methods=["GET", "POST"])
def join():
    if request.method == "POST":  # 회원가입 정보 기입 후 확인 -> 데이터베이스에 정보 저장
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        user_gender = request.form['gender']
        user_age = request.form['age-group']
        user_job = request.form['occupation']
        member = tb_user_info(user_id, user_pw, user_gender, user_age, user_job)
        db.session.add(member)
        db.session.commit()
        return redirect(url_for('user.login'))  # 회원가입 후 로그인 창으로 바로 이동
    else:
        return render_template('join.html')  # 회원가입 페이지

# 로그인 페이지
@user.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:  # 로그인 정보 입력
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        session['logged_in'] = False
        if user_id == None or user_pw == None:
            errMsg = '아이디와 비밀번호를 입력해주세요'
        try:
            user = tb_user_info.query.filter(tb_user_info.user_id == user_id).all()  # 아이디 비교
            if user:  # 아이디 존재할 때
                user = tb_user_info.query.filter(tb_user_info.user_pw == user_pw).first()  # 비밀번호 비교
                if user:  # 아이디, 비밀번호 일치 -> 로그인 성공
                    session['logged_in'] = True
                    session['user_id'] = user_id
                    session['check'] = 1
                    return redirect(url_for('user.home'))
                else:  # 아이디, 비밀번호 불일치
                    errMsg = '아이디 또는 비밀번호가 틀렸습니다'
            else: # 아이디 없을 때
                errMsg = '아이디 또는 비밀번호가 틀렸습니다'
        except:
            errMsg = '로그인에 실패하였습니다'
        return render_template('login.html', errMsg=errMsg)

### 로그인 한 상태로 창만 닫으면 다시 flask run 했을 때 로그인 된 상태로 접속된다.
### 로그아웃 기능을 이용해야만 로그아웃상태가 된다.
### 창을 닫으면 자동적으로 session 데이터가 제거되도록 할 수는 없을까? - 일단 패스하고 다른 기능부터 만든다.
@user.route('/logout')
def logout():
    session['logged_in'] = False
    session['user_id'] = None
    session['admin_id'] = None
    session['check'] = 0
    return redirect(url_for('user.home'))