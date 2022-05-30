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
    核心指标文件上传路径
    """
    # 开发环境
    BATCH_FILES_PATH_CORE_INDEX = r'C:\Users\thinkpad\Desktop\servers'
    # 生产环境
    # BATCH_FILES_PATH_CORE_INDEX = '/home/mba/share/coreIndex'

    pass
