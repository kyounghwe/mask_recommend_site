from flask import Flask, render_template,request,session,redirect,url_for

from db_connect import db, db_connector
import cgi

from models import Zzim

form = cgi.FieldStorage()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ekdldksk@localhost:3306/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

db.init_app(app)

@app.route('/login', methods=['GET','POST'])  
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

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/',methods=['GET','POST'])
def zzim_in():
    if request.method == 'POST':
        
        if request.form.get("zzim_btn"):
            goods_info = request.form['r_op1']
            user_info = session['user']
            
            zzim_info = Zzim(user_info,goods_info)
            db.session.add(zzim_info)
            db.session.commit()
            return redirect(url_for('zzim_in'))
        else:
            return render_template('zzim.html')
    return render_template('zzim.html')





if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000, debug=True)
