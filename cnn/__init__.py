# @Author  : Edlison
# @Date    : 8/6/21 02:28
from cnn.diagnose_new import diagnose_with_model


def api_cnn(img):
    res = diagnose_with_model(img)
    return res
