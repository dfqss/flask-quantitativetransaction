from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    """
    装饰器配置
    """
    SCHEDULER_API_ENABLED = True

    """
    数据库配置 当此处不配置时，自动会读取[.env]中的数据库配置信息
    """
    # 开发环境
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/lin_cmsflask1'

    # 生产环境
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mba:!IDy_7)ZA-U3@localhost:3311/mba'
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_COMMIT_TEARDOWN = True

    """
    批量指标文件上传路径
    """
    # 开发环境
    BATCH_FILES_PATH = [
        r'C:\Users\thinkpad\Desktop\servers\coreIndex',
        r'C:\Users\thinkpad\Desktop\servers\finAnalysisIndex'
    ]

    # 生产环境
    # BATCH_FILES_PATH = ['/home/mba/share/coreIndex', '/home/mba/share/otherIndex']

    """
    文件类型:
        财务分析指标：CWFXZB
        成长指标：CZZB
        杜邦分析指标：DBFXZB
        股票估值：GPGZ
        技术分析指标：JSFXZB
        行业分类：HYFL
        证券基础指标：ZQJCZB
    """
    FILE_TYPES = ['CWFXZB', 'CZZB', 'DBFXZB', 'GPGZ', 'JSFXZB', 'HYFL', 'ZQJCZB']
    pass
