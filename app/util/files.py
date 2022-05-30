import os


# 获取某一个指定目录下的所有指定文件名
def getFileNameList(path, suffix):
    path = os.path.abspath(os.path.realpath(path))
    fileNameList = []
    # 判断文件路径是否存在
    if not os.path.exists(path):
        # 如果不存在则创建目录
        os.makedirs(path)
    # 获取path目录下后缀为suffix的文件名称
    for filename in os.listdir(path):
        if suffix in filename:
            fileNameList.append(filename)
    return fileNameList


# 批量修改文件名后缀：修改源文件
def renameFilesSuffix(path, fileNameList, renameFromSuffix, renameToSuffix):
    for filename in fileNameList:
        oldFileName = os.path.join(path, filename)
        # oldFileName = path + '\\' + filename
        newFileName = os.path.join(path, filename.replace(renameFromSuffix, renameToSuffix))
        # newFileName = path + '\\' + filename.replace(renameFromSuffix, renameToSuffix)
        os.rename(oldFileName, newFileName)


# 批量修改文件名后缀：不修改源文件,返回一个文件名称的集合
def modifyFilesSuffix(fileNameList, modifyFromSuffix, modifyToSuffix):
    returnList = []
    for filename in fileNameList:
        returnList.append(filename.replace(modifyFromSuffix, modifyToSuffix))
    return returnList
