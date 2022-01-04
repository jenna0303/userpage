from flask import Flask, json, render_template, redirect, request, url_for, jsonify, Response
from sqlalchemy.orm.session import Session
from werkzeug.utils import secure_filename
from models import db
import os
from models import Users
app = Flask(__name__)

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'GET' : #GET은 페이지가 나오도록 요청하기 위함
        return render_template("register.html")
    else: #POST는 등록 버튼 클릭 시 데이터를 가져오기 위함
        #사용자 정보 생성하기
        username = request.form.get('username')
        userage = request.form.get('userage')

        #이미지 파일 받아와서 경로에 저장하기
        img = request.files['file']
        save_to = f'static/profile_imgs/{img.filename}' #지정경로에 파일이름 그대로 저장하기
        img.save(save_to)
        userface = img.filename #데이터베이스에 저장하기 위해 변수에 파일 이름을 삽입

        ###SQLAlchemy
        users = Users()
        #값을 저장한다.
        users.username = username
        users.userage = userage
        users.profile_image = userface
        db.session.add(users)
        db.session.commit()

        ###txt : 읽기모드로 파일을 연 후, DB에 저장된 정보를 불러와서 업데이트하는 방식 (new line으로 파일에 추가하는 것과 같음)
        f = open('./user.txt', 'w', encoding='utf-8') #읽기모드로 user.txt를 연다.
        users = Users.query.all() #DB 정보를 가져온다
        for data in users:
            #txt 파일 저장 예시: username ㅇㅇㅇ userage ㅇㅇㅇ userface ㅇㅇㅇ(.png)
            f.write('username '+ data.username + ' userage ' + data.userage + ' userface ' + data.profile_image)
            f.write('\n')
        f.close()

        #사용자 등록 후 목록 페이지로 이동해야함. 
        return redirect(url_for('list'))

@app.route('/list', methods=['GET','POST'])
def list():
    if request.method == 'GET':
            return render_template("list.html") #페이지 요청 시, 목록 페이지 띄우기
    else:
        selectType = request.form.get('selectType')
        txtlist = []
        #DB로 조회하길 원할 경우
        if selectType == 'DB' :
            return render_template("db_list.html", Users = Users.query.all())
        #파일로 조회하길 원할 경우
        else:
            f = open('./user.txt','r',encoding='utf-8')
            lines = f.readlines()
            for line in lines:
                item = line.split(" ")
                user_name = item[item.index("username")+1]
                txtlist.append(user_name)
            print(txtlist)
            return render_template("txt_list.html", data = txtlist)

@app.route('/detail/<userName>', methods=['GET'])
def detail(userName):
                if request.method == 'GET':
                    #dusers: users 테이블 중에 특정 사용자의 행을 가져와서 저장한다.
                    dusers = Users.query.filter(Users.username == userName).one()
                    #특정 사용자의 저장 파일 명을 가져와서 경로를 지정한다.
                    base_path = './static/profile_imgs/{dusers.profile_image}'
                    #json 형태로 가져온다.
                    p_response = request.get(base_path).json
                    #Users 테이블에 저장된 값 중에서, 사용자 이름과 일치하는 행만 가져온다.
                    return render_template("register.html", files = p_response)



if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True     # 사용자에게 원하는 정보를 전달완료했을때가 TEARDOWN, 그 순간마다 COMMIT을 하도록 한다.라는 설정
    #여러가지 쌓아져있던 동작들을 Commit을 해주어야 데이터베이스에 반영됨. 이러한 단위들은 트렌젝션이라고함.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # True하면 warrnig메시지 유발

    db.init_app(app) #초기화 후 db.app에 app으로 명시적으로 넣어줌
    db.app = app
    db.create_all()   # 이 명령이 있어야 생성됨.


    app.run(host='127.0.0.1', port=5000, debug=True) 


