from flask import render_template, url_for, redirect, request, jsonify
from view import app
from cnn import api_cnn
from nlp import api_qa_img, api_qa_sentence


@app.route('/')
def base():
    return redirect(url_for('index'))


@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('past.html')


@app.route('/i', methods=['POST'])
def i():
    pic = request.form['pic']
    print('pic ', pic)
    pred = api_cnn(pic)
    print('pred ', pred)
    res = api_qa_img(pred)
    print('res ', res)

    return jsonify({'res': res})


@app.route('/nlp', methods=['POST'])
def nlp():
    que = request.form['que']
    print('question', que)
    res = api_qa_sentence(que)
    print('res ', res)

    return jsonify({'ans': res})
