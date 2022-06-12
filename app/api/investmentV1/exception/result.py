from lin import Success, Failed


# 返回成功信息
def success(code: int = 0):
    returnDict = dict()
    returnObj = Success(code)
    returnDict['code'] = "0000"
    returnDict['ret'] = "S"
    returnDict['message_code'] = returnObj.message_code
    returnDict['message'] = returnObj.message
    return returnDict


# 返回失败信息
def failed(code: int = 10200):
    returnDict = dict()
    returnObj = Failed(code)
    returnDict['code'] = "9999"
    returnDict['ret'] = "F"
    returnDict['message_code'] = returnObj.message_code
    returnDict['message'] = returnObj.message
    return returnDict
