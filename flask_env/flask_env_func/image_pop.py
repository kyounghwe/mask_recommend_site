from io import BytesIO
from flask import Flask, render_template,request,session,redirect,url_for,Response

from db_connect import db, buffer,engine
import cgi

#이미지 데이터베이스에 저장
from models import images
import base64
import pandas as pd
from PIL import Image

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
        pic = request.files['pic']
        if not pic:
            return "업로드 되지 않았습니다"

        im= Image.open(pic)
        im.save(buffer,format='png')
        img_str = base64.b64encode(buffer.getvalue())
        img_df = pd.DataFrame({'image_data':[img_str]})
        img_df.to_sql('images',con=engine,if_exists='append',index=False)

        return redirect(url_for('review'))
    else:
        img=[]
        show = images.query.all()
        img_df = pd.read_sql(sql='SELECT * FROM images',con=engine)
        for i in range(len(show)):
            img_str = img_df['image_data'].values[i]
            stage2 = img_str.decode('utf-8')
            img.append(stage2)
        return render_template('Mlist.html',show=img)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000, debug=True)

    