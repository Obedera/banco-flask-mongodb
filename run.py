#!/usr/bin/python

from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/bancodb'
mongo = PyMongo(app)


@app.route("/",methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        user = request.form
        user_bd = mongo.db.pessoa.find_one({'email':user.get('email'),'senha':user.get('senha')})
        if user_bd is not None:
            return render_template('user.html',user=user_bd)
        else:
            return render_template('index.html',msg='Login invalido')

    return render_template('index.html')

    
@app.route('/cadastro',methods = ['POST','GET'])
def cadastrar():
    if request.method == 'POST':
        user = request.form
        user_bd = mongo.db.pessoa.find_one({'email':user.get('email')})
        if user_bd is None:
            mongo.db.pessoa.insert({'nome' : user.get('nome'), 'sobrenome' : user.get('sobrenome'), 'email' : user.get('email'), 'senha' : user.get('senha'), 'saldo': 0})
            return render_template('index.html',msg='Faça seu login agora')
        else:
            return render_template('cadastro.html',msg='Usuário já cadastrado')
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)