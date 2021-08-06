#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from nlp.qa.question_classifier import *
from nlp.qa.question_parser import *
from nlp.qa.answer_search import *
from translate import Translator
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
                sent = translator_EN.translate(sent)
                print('before chatbot ', sent)
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


def eval_img(pred):
    if pred == '0':
        answer = "您好，恭喜您在乳腺癌诊断报告中被确认为阴性，请继续保持良好生活习惯，可以在对话框输入xx食物功效获得健康tips！"
    elif pred == '1':
        answer = "您好，非常遗憾您在本次乳腺癌诊断报告中被确认为阳性，请尽快联系您的负责医师进行进一步的诊断及治疗，可以通过以下问题了解乳腺癌的相关知识：" \
                 "乳腺癌是什么" \
                 "乳腺癌是什么原因造成的" \
                 "乳腺癌能吃什么食物" \
                 "乳腺癌能治愈吗" \
                 "乳腺癌的治疗方法"
    elif pred == '-1':
        answer = 'Size of image error.'
    elif pred == '-2':
        answer = 'File uploaded is not image.'
    else:
        answer = 'sys error.'
    return answer


def eval_sentence(handler, msg):
    if check_contain_chinese(msg) == False:  # 输入英文
        translator_CH = Translator(from_lang="english", to_lang="chinese")
        translator_EN = Translator(from_lang="chinese", to_lang="english")
        translation = translator_CH.translate(msg)
        answer = translator_EN.translate(handler.chat_main(translation, translator_EN))
    else:  # 输入中文
        answer = handler.chat_main(msg)

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
            translator_CH = Translator(from_lang="english", to_lang="chinese")
            translator_EN = Translator(from_lang="chinese", to_lang="english")
            translation = translator_CH.translate(question)
            answer = translator_EN.translate(handler.chat_main(translation, translator_EN))
        else:
            answer = handler.chat_main(question)
        print('系统:', answer)

