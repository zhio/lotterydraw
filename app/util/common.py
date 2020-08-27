
from fastapi.responses import JSONResponse


def trueReturn(data = None, msg=None):
    """ 操作成功结果 """
    result = {
        "status": True,
        "data": data,
        "msg": msg
    }
    return JSONResponse(content=result)


def falseReturn(data = None, msg = None):
    """ 操作成功结果 """
    result = {
        "status": False,
        "data": data,
        "msg": msg
    }
    return JSONResponse(content=result)


def trueContent(data, msg):
    """ 操作成功结果 """
    result = {
        "status": True,
        "data": data,
        "msg": msg
    }
    return result


def falseContent(data = "", msg = ""):
    """ 操作成功结果 """
    result = {
        "status": 400,
        "data": data,
        "msg": msg
    }
    return result