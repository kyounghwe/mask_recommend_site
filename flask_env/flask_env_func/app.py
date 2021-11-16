from io import BytesIO
from flask import Flask, render_template,request,session

#테스트용 임폿
#from flask import redirect,url_for

#데이터베이스에서 불러와서 현 데이터와 비교하기 
#from db_connect import db, db_connector
#from models import Member, mask

from db_connect import db, buffer,engine
import cgi

#이미지 데이터베이스에 저장
from PIL import Image
import pandas as pd 
import base64

form = cgi.FieldStorage()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ekdldksk@localhost:3306/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

db.init_app(app)


@app.route("/",methods=["GET","POST"])
def review():
    if request.method == 'POST':
        im = Image.open('img.png')
        im.save(buffer, format='png')
        img_str = base64.b64encode(buffer.getvalue())
        img_df = pd.DataFrame({'image_data':[img_str]})
        img_df.to_sql('images',con=engine,if_exists='append',index=False)
    else:
        img_df = pd.read_sql(sql='select * from images',con=engine)
        img_str = img_df['image_data'].values[0]
        img = base64.decodestring(img_str)
        im = Image.open(BytesIO(img))
        
    return im.show()
'''@app.route("/",methods=["GET","POST"])
def join():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        user_gender = request.form['gender']
        user_age = request.form['age-group']
        user_job = request.form['occupation']

        member = Member(user_id, user_pw,user_gender,user_age,user_job)
        db.session.add(member)
        db.session.commit()
        #테스트용
        return redirect(url_for('Mlist'))
    else:
       return render_template('join.html')'''

'''
@app.route("/login",methods=["GET","POST"])
def login():

    user_info = db_connector()

    if request.method == 'POST':
        ui = request.form['user_id']
        up = request.form['user_pw']
        try:
            if ui in user_info:
                if up in user_info:
                    session['logged_in'] = True
                    session['user'] = ui
                    return redirect(url_for('Mlist'))
                else:
                    return '비밀번호가 틀립니다.'
            return '아이디가 없습니다.'
        except:
            return f'{user_info}'
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('Mlist.html')

#확인용
@app.route('/list')
def Mlist():
    Mlist = Member.query.all()
#    if 'user' in session:
#        return render_template('join.html', Mlist=Mlist)
#    return redirect(url_for('login'))
    return render_template('Mlist.html',Mlist=Mlist)

@app.route('/excel')
def excel():
    csvlist = mask.query.all()
    return render_template('CSV.html',csvlist = csvlist)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000, debug=True)'''
 