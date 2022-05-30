from flask import Flask
from app.util import files, common
import os

app = Flask(__name__)


# 读取文件到数据表中
def readFile(conn, path):
    filePath = os.path.join(path, common.get_now_time_yyyymmdd())
    app.logger.info('核心指标文件地址：' + filePath)
    okFiles = files.getFileNameList(filePath, '.ok')
    if len(okFiles) > 0:
        files.renameFilesSuffix(filePath, okFiles, '.ok', '.reading')
        create_batch_files(conn, filePath, okFiles)
        readingFiles = files.modifyFilesSuffix(okFiles, '.ok', '.reading')
        files.renameFilesSuffix(filePath, readingFiles, 'reading', 'success')
    else:
        app.logger.info('路径[' + filePath + ']下没有需要读入的核心指标文件')


# 创建批量文件表数据
def create_batch_files(conn, filePath, okFiles):
    insertList = []
    for filename in okFiles:
        insertDict = dict()
        insertDict['file_name'] = filename.replace('.ok', '.xlsx')
        insertDict['file_path'] = filePath
        insertList.append(insertDict)
    # 插入数据
    if len(insertList) != 0:
        sql = "insert mba_batch_files " \
              "(is_deleted, file_name, file_path, status, create_time, update_time) " \
              "values ('0', :file_name, :file_path, '0', now(), now()) "
        conn.session.execute(sql, insertList)
        conn.session.commit()
