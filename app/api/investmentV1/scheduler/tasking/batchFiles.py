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

# 批量文件地址
batch_files_path = DevelopmentConfig.BATCH_FILES_PATH


# 读取文件到数据表中
def readFile():
    for path in batch_files_path:
        filePath = os.path.join(path, common.get_now_time_yyyymmdd())
        readingFiles = []
        try:
            okFiles = files.getFileNameList(filePath, '.ok')
            app.logger.info('--------start 当前文件读取地址：' + filePath)
            app.logger.info('开始读取批量文件：' + str(okFiles))
            if len(okFiles) > 0:
                readingFiles = files.renameFilesSuffix(filePath, okFiles, '.ok', '.reading')
                create_batch_files(filePath, okFiles)
                files.renameFilesSuffix(filePath, readingFiles, '.reading', '.success')
                app.logger.info('--------end 批量文件读取成功' + filePath)
            else:
                app.logger.info('--------end 路径[' + filePath + ']下没有需要读入的批量文件')
        except Exception as e:
            app.logger.error('读取批量文件失败，开始事务回滚:' + str(e))
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
        insertDict['type'] = filename[:filename.index('_')] + '%'
        insertList.append(insertDict)
    # 插入数据
    if len(insertList) != 0:
        sql = "insert into mba_batch_files " \
              "(is_deleted, file_name, file_path, file_periods, " \
              "status, cal_date, create_time, update_time) " \
              "select '0', :file_name, :file_path, IFNULL(MAX(file_periods),0)+1, " \
              "'0', DATE_FORMAT(now(),'%Y-%m-%d'), now(), now() " \
              "from mba_batch_files where file_name like :type "
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
