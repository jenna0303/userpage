#SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

#사용자 정보를 저장하기 위한 SQLAlchemy 선언
db = SQLAlchemy()

#db테이블 정의
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), nullable = False) #사용자 이름을 저장하기 위한 username, null 불가
    userage = db.Column(db.String(32), nullable = False) #사용자 나이를 저장하기 위한 userage, null 불가
    profile_image = db.Column(db.String(100)) #사진은 파일시스템에 저장 후 그 파일의 이름만 DB에 저장할 예정