#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from nlp.qa.question_classifier import *
from nlp.qa.question_parser import *
from nlp.qa.answer_search import *
import json
import random
import requests
import urllib.parse
from hashlib import md5
from nlp.chatbot import api_chatbot


'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent, translator_EN=None):
        answer = '您好，我是医药智能助理，希望可以帮到您。祝您身体棒棒！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            if translator_EN:
                sent = translator_EN(sent)
                print('[NLP]Casualty ', sent)
                answer = api_chatbot(sent)
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)


def check_contain_chinese(check_str):
    for ch in check_str.encode('utf-8').decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def translate_api_CH(text):
    appid = '20210806000909193'
    secretKey = 'ejPq0aY5NhGpfMqOVZDJ'
    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    q = text
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    m1 = md5()
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    res = json.loads(requests.get(myurl).text)['trans_result'][0]['dst']

    return res


def translate_api_EN(text):
    appid = '20210806000909193'
    secretKey = 'ejPq0aY5NhGpfMqOVZDJ'
    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    q = text
    fromLang = 'zh'
    toLang = 'en'
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    m1 = md5()
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    res = json.loads(requests.get(myurl).text)['trans_result'][0]['dst']

    return res


def eval_img(pred):
    if pred == 0:
        answer = "Hello, congratulations! You were confirmed as negative in the breast cancer diagnosis report. " \
                 "Please continue to maintain good habits! You can enter the food effect in the dialog box to get health tips!"
    elif pred == 1:
        answer = "Hello, I am very sorry that you were confirmed as positive in this breast cancer diagnosis report. " \
                 "Please contact your responsible physician for further diagnosis and treatment as soon as possible. " \
                 "You can learn about breast cancer related knowledge through the following questions:\n" \
                 "What is breast cancer?\n" \
                 "What causes breast cancer?\n" \
                 "What foods can you eat for breast cancer?\n" \
                 "Can breast cancer be cured?\n" \
                 "Breast cancer treatment?"
    elif pred == -1:
        answer = 'error size.'
    elif pred == -2:
        answer = 'error file.'
    else:
        answer = 'sys error.'
    return answer


def eval_sentence(handler, msg):
    if check_contain_chinese(msg) == False:  # 输入英文
        answer = translate_api_CH(msg)
        answer = translate_api_EN(handler.chat_main(answer, translate_api_EN))
    else:  # 输入中文
        answer = handler.chat_main(msg, translate_api_EN)
        answer = translate_api_CH(answer)

    return answer


if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        if question == '0':
            answer = "您好，恭喜您在乳腺癌诊断报告中被确认为阴性，请继续保持良好生活习惯，可以在对话框输入xx食物功效获得健康tips！"
        elif question == '1':
            answer = "您好，非常遗憾您在本次乳腺癌诊断报告中被确认为阳性，请尽快联系您的负责医师进行进一步的诊断及治疗，可以通过以下问题了解乳腺癌的相关知识：" \
                     "乳腺癌是什么" \
                     "乳腺癌是什么原因造成的" \
                     "乳腺癌能吃什么食物" \
                     "乳腺癌能治愈吗" \
                     "乳腺癌的治疗方法"
        elif check_contain_chinese(question) == False:
            translation = json.loads(requests.get(translate_api_CH(question)).text)['trans_result'][0]['dst']
            answer = json.loads(requests.get(translate_api_EN(handler.chat_main(translation))).text)['trans_result'][0][
                'dst']
        else:
            answer = handler.chat_main(question)
        print('系统:', answer)

