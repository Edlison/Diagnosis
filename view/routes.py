from flask import render_template, url_for, redirect, request, jsonify
from view import app


@app.route('/')
def base():
    return redirect(url_for('index'))


@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('past.html')


@app.route('/i', methods=['POST'])
def i():
    pic = request.form['pic']
    print(pic)
    return jsonify({'res': pic})


@app.route('/nlp', methods=['POST'])
def nlp():
    que = request.form['que']
    print(que)

    return jsonify({'ans': 'hello'})
