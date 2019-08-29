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
            conta = mongo.db.conta.find_one({'id_user':user_bd['_id']})
            return render_template('user.html',user=user_bd,conta=conta)
        else:
            return render_template('index.html',msg='Login invalido')

    return render_template('index.html')

    
@app.route('/cadastro',methods = ['POST','GET'])
def cadastrar():
    if request.method == 'POST':
        user = request.form
        user_bd = mongo.db.pessoa.find_one({'email':user.get('email')})
        if user_bd is None:
            data = f'{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}'
            hora = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'

            user = mongo.db.pessoa.insert({'nome' : user.get('nome'), 'sobrenome' : user.get('sobrenome'), 'email' : user.get('email'), 'senha' : user.get('senha')})

            mongo.db.conta.insert({'id_user': user, 'data':data, 'hora':hora, 'ContaInicial':0, 'ContaFinal':0, 'valor':0})
            return render_template('index.html',msg='Faça seu login agora')
        else:
            return render_template('cadastro.html',msg='Usuário já cadastrado')
    return render_template('cadastro.html')

@app.route('/depositar', methods = ['POST','GET'])
def depositar():
    if request.method == 'POST':
        user = request.form
        user_bd = mongo.db.pessoa.find_one({'email':user.get('email'),'senha':user.get('senha')})
        conta = mongo.db.conta.find_one({'id_user':user_bd['_id']})
        valor = int(request.form.get('valor'))
        if valor<=0:
            return render_template('user.html',user=user_bd,conta=conta,msg_deposito='Valor Inválido')

        data = f'{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}'
        hora = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'
        
        mongo.db.conta.update_one({'id_user':user_bd['_id']}, {'$set': {'data':data,'hora':hora,'ContaInicial':conta['ContaFinal'],'ContaFinal':(conta['ContaFinal']+valor),'valor':valor}})
        
        conta = mongo.db.conta.find_one({'id_user':user_bd['_id']})
        print(conta)
        mongo.db.transacoes.insert({'id_conta': conta['_id'], 'data':conta['data'], 'hora':conta['hora'], 'ContaInicial':conta['ContaInicial'], 'ContaFinal':conta['ContaFinal'], 'valor':conta['valor']})
        
        return render_template('user.html',user=user_bd,conta=conta,msg_deposito='Dinheiro Depositado')

@app.route('/sacar', methods = ['POST','GET'])
def sacar():
    if request.method == 'POST':
        user = request.form
        user_bd = mongo.db.pessoa.find_one({'email':user.get('email'),'senha':user.get('senha')})
        conta = mongo.db.conta.find_one({'id_user':user_bd['_id']})
        valor = int(request.form.get('valor'))
        if valor<=0:
            return render_template('user.html',user=user_bd,conta=conta,msg_sacar='Valor Inválido')

        data = f'{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}'
        hora = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'
        
        mongo.db.conta.update_one({'id_user':user_bd['_id']}, {'$set': {'data':data,'hora':hora,'ContaInicial':conta['ContaFinal'],'ContaFinal':(conta['ContaFinal']-valor),'valor':-valor}})
        
        conta = mongo.db.conta.find_one({'id_user':user_bd['_id']})
        print(conta)
        mongo.db.transacoes.insert({'id_conta': conta['_id'], 'data':conta['data'], 'hora':conta['hora'], 'ContaInicial':conta['ContaInicial'], 'ContaFinal':conta['ContaFinal'], 'valor':conta['valor']})
        
        return render_template('user.html',user=user_bd,conta=conta,msg_sacar='Dinheiro Sacado')



if __name__ == '__main__':
    app.run(debug=True)