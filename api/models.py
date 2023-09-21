from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class ToDo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.String(800),nullable=False)
    differ=db.Column(db.String(800),nullable=False)
    status=db.Column(db.String(800),nullable=True)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    date_deadline=db.Column(db.DateTime,nullable=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.rid'))

    def __repr__(self) -> str:
        return f"{self.title} - {self.desc} - {self.status} - {self.differ}"

class User(db.Model):
    __tablename__ = 'user'
    rid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique= True)
    email = db.Column(db.String(100),unique= True)
    password = db.Column(db.String(20))
    dob = db.Column(db.String(15))

    def __int__(self,unm,uem,pas,dob):
        self.username = unm
        self.email = uem
        self.password = pas
        self.dob = dob