from flask import Flask

from app.api.investmentV1.model.batchFiles import MbaBatchFiles
from sqlalchemy import or_, and_, not_
from flask_sqlalchemy import SQLAlchemy
import time

from app.api.investmentV1.model.dupontAnalysisIndex import MbaDupontAnalysisIndex
from app.api.investmentV1.model.finAnalysisIndex import MbaFinAnalysisIndex
from app.api.investmentV1.model.growthIndex import MbaGrowthIndex
from app.api.investmentV1.model.industryClass import MbaIndustryClass
from app.api.investmentV1.model.secBasicIndex import MbaSecBasicIndex
from app.api.investmentV1.model.stockValue import MbaStockValue
from app.api.investmentV1.model.tecAnalysisIndex import MbaTecAnalysisIndex
from app.api.investmentV1.scheduler.tasking.batchFiles import update_batch_files_status
from app.config.development import DevelopmentConfig

from app.util.excel import readExcel

# 定义全局app变量
app = Flask(__name__)

# 加载配置:必须先加载配置参数，再创建conn才有效
app.config.from_object(DevelopmentConfig())

# 创建全局的数据库连接对象，一个数据库连接对象下执行同一个session
conn = SQLAlchemy(app)

# 批量文件地址
file_types = DevelopmentConfig.FILE_TYPES

# 初始化字段映射关系：如果后续添加，key值一定要现在file_types中添加，再关联表字段
entity_map = {
        # 财务分析指标：CWFXZB
        file_types[0]: MbaFinAnalysisIndex(),
        # 成长指标：CZZB
        file_types[1]: MbaGrowthIndex(),
        # 杜邦分析指标：DBFXZB
        file_types[2]: MbaDupontAnalysisIndex(),
        # 股票估值：GPGZ
        file_types[3]: MbaStockValue(),
        # 技术分析指标：JSFXZB
        file_types[4]: MbaTecAnalysisIndex(),
        # 行业分类：HYFL
        file_types[5]: MbaIndustryClass(),
        # 证券基础指标：ZQJCZB
        file_types[6]: MbaSecBasicIndex()
    }


def createOrUpdateOtherIndex():
    for fileType in file_types:
        # 获取要读取文件的信息
        app.logger.info('--------start 开始读取批量指标文件-类型为：' + fileType)
        file = get_file_names(fileType)
        # 没有查询到要读取的文件直接返回
        if len(file) <= 0:
            app.logger.info('--------end 该文件类型下没有需要读取的数据文件：' + fileType)
            continue
        # 获取文件路径、文件名称
        filePath = file[0][0]
        fileName = file[0][1]
        # 将数据更新为：毫秒值-[读取中]
        update_batch_files_status(conn, fileName, str(round(time.time() * 1000)), '')
        try:
            entity = entity_map[fileType]
            # 1.读取excel中的指标数据
            excelData = readExcel(filePath, fileName, 0, 2, entity.key_to_list())
            # 2.删除上一期数据
            truncate_table(entity.__tablename__)
            # 3.插入新一期的数据
            create_other_index(entity, excelData)
            # 提交数据
            conn.session.commit()
            # 更新数据读取状态为：2-成功
            update_batch_files_status(conn, fileName, '2', '')
        except Exception as e:
            app.logger.info('读取批量指标文件失败 [' + str(e) + ']')
            conn.session.rollback()
            # 更新数据读取状态为：1-失败
            update_batch_files_status(conn, fileName, '1', str(e))
        finally:
            conn.session.close()
        app.logger.info('--------end 读取批量指标文件结束-类型为：' + fileType)


# 查询mba_batch_files表中需要写入的核心指标文件的路径和文件名
def get_file_names(fileType):
    # 根据字段排序加 -MbaBatchFiles.file_name是降序
    slq = conn.session\
        .query(MbaBatchFiles.file_path, MbaBatchFiles.file_name)\
        .filter(and_(MbaBatchFiles.file_name.startswith(fileType),
                     MbaBatchFiles.status.__eq__('0')))\
        .order_by(MbaBatchFiles.file_periods).limit(1)
    return slq.all()


# 清空数据表数据
def truncate_table(entityName):
    app.logger.info('清空数据表数据：' + entityName)
    try:
        sql = "delete from " + entityName
        conn.session.execute(sql)
    except Exception as e:
        app.logger.error("清空数据表[" + entityName + "]失败:" + str(e))
        raise Exception("清空数据表[" + entityName + "]失败")


# 插入新一期的数据
def create_other_index(entity, excelData):
    entityName = entity.__tablename__
    keys = entity.key_to_list()
    app.logger.info('插入新一期数据：' + entityName)
    try:
        if len(excelData) > 0:
            sql = "insert into " + entityName + " (" + ','.join(
                keys) + ", is_deleted, create_time, update_time) values (:" + ',:'.join(
                keys) + ", '0', now(), now()) "
            conn.session.execute(sql, excelData)
    except Exception as e:
        app.logger.error("插入新一期数据表[" + entityName + "]失败:" + str(e))
        raise Exception("插入新一期数据表[" + entityName + "]失败")
