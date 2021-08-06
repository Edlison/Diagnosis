from flask import render_template, url_for, redirect, request, jsonify
from view import app
from cnn import api_cnn
from nlp import api_qa_img, api_qa_sentence
import base64
import io


@app.route('/')
def base():
    return redirect(url_for('index'))


@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('past.html')


@app.route('/i', methods=['POST'])
def i():
    pic = request.form['pic']
    img_info = pic.split(',')
    data = base64.b64decode(img_info[1])
    img = io.BytesIO(data)
    pred = api_cnn(img)
    print('[CNN]pred ', pred)
    res = api_qa_img(pred)

    return jsonify({'res': res})


@app.route('/nlp', methods=['POST'])
def nlp():
    que = request.form['que']
    print('[NLP]Q', que)
    res = api_qa_sentence(que)
    print('[NLP]A', res)

    return jsonify({'ans': res})
