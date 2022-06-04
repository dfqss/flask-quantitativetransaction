from flask import Flask
from app.util import files, common
import os
from flask_sqlalchemy import SQLAlchemy
from app.config.development import DevelopmentConfig

# 定义全局app变量
app = Flask(__name__)

# 加载配置:必须先加载配置参数，再创建conn才有效
app.config.from_object(DevelopmentConfig())

# 创建全局的数据库连接对象，一个数据库连接对象下执行同一个session
conn = SQLAlchemy(app)

# 核心指标文件地址
path_coreIndex = DevelopmentConfig.BATCH_FILES_PATH_CORE_INDEX


# 读取文件到数据表中
def readFile():
    filePath = os.path.join(path_coreIndex, common.get_now_time_yyyymmdd())
    readingFiles = []
    try:
        app.logger.info('核心指标文件地址：' + filePath)
        okFiles = files.getFileNameList(filePath, '.ok')
        if len(okFiles) > 0:
            readingFiles = files.renameFilesSuffix(filePath, okFiles, '.ok', '.reading')
            create_batch_files(filePath, okFiles)
            files.renameFilesSuffix(filePath, readingFiles, '.reading', '.success')
        else:
            app.logger.info('路径[' + filePath + ']下没有需要读入的核心指标文件')
    except Exception as e:
        app.logger.error('读取核心指标文件失败，开始事务回滚:' + str(e))
        conn.session.rollback()
        files.renameFilesSuffix(filePath, readingFiles, '.reading', '.fail')
    finally:
        conn.session.close()


# 创建批量文件表数据
def create_batch_files(filePath, okFiles):
    insertList = []
    for filename in okFiles:
        insertDict = dict()
        insertDict['file_name'] = filename.replace('.ok', '.xlsx')
        insertDict['file_path'] = filePath
        insertList.append(insertDict)
    # 插入数据
    if len(insertList) != 0:
        sql = "insert into mba_batch_files " \
              "(is_deleted, file_name, file_path, status, create_time, update_time) " \
              "values ('0', :file_name, :file_path, '0', now(), now()) "
        conn.session.execute(sql, insertList)
        conn.session.commit()


# 更新批量文件数据表状态 0-未读 1-失败 2-成功 随机数-读取中
def update_batch_files_status(db, fileName, status, description):
    try:
        value = [{"fileName": fileName, "status": status, "description": description}]
        sql = "update mba_batch_files set status = :status, description = :description " \
              "where file_name = :fileName"
        db.session.execute(sql, value)
        db.session.commit()
    except Exception as e:
        app.logger.error('更新批量文件数据表状态失败:' + str(e))
        db.session.rollback()
    finally:
        db.session.close()
