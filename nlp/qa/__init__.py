# @Author  : Edlison
# @Date    : 8/6/21 02:29
from nlp.qa.chatbot_graph import eval_img, eval_sentence, ChatBotGraph
handler = ChatBotGraph()


def api_qa_img(pred):
    res = eval_img(pred)
    return res


def api_qa_sentence(msg):
    res = eval_sentence(handler, msg)
    return res
