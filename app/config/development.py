from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    """
    开发环境配置
    """
    # 装饰器配置
    SCHEDULER_API_ENABLED = True

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/lin_cmsflask'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True

    # 核心指标文件上传路径
    BATCH_FILES_PATH_CORE_INDEX = r'C:\Users\thinkpad\Desktop\servers'

    pass
