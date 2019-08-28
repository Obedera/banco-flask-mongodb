#!/usr/bin/python

from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

@app.route("/",methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        result = request.form
        if result['email'] == 'obede' and result['senha'] == '1234':
            return render_template('user.html',email=result['email'],senha=result['senha'])
        else:
            return render_template('index.html',msg='Login invalido')

    return render_template('index.html')

    
@app.route('/cadastro',methods = ['POST','GET'])
def cadastrar():
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)