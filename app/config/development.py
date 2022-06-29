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
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/lin_cmsflask'

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
        r'C:\Users\thinkpad\Desktop\servers\finAnalysisIndex',
        r'C:\Users\thinkpad\Desktop\servers\growthIndex',
        r'C:\Users\thinkpad\Desktop\servers\dupontAnalysisIndex',
        r'C:\Users\thinkpad\Desktop\servers\stockValue',
        r'C:\Users\thinkpad\Desktop\servers\tecAnalysisIndex',
        r'C:\Users\thinkpad\Desktop\servers\industryClass',
        r'C:\Users\thinkpad\Desktop\servers\secBasicIndex',
        r'C:\Users\thinkpad\Desktop\servers\listingDate',
    ]

    # 生产环境
    # BATCH_FILES_PATH = [
    #     '/home/mba/share/coreIndex',
    #     '/home/mba/share/finAnalysisIndex',
    #     '/home/mba/share/growthIndex',
    #     '/home/mba/share/dupontAnalysisIndex',
    #     '/home/mba/share/stockValue',
    #     '/home/mba/share/tecAnalysisIndex',
    #     '/home/mba/share/industryClass',
    #     '/home/mba/share/secBasicIndex',
    #     '/home/mba/share/listingDate',
    # ]

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

    """
    文件类型与目录映射关系:
    """
    # 开发环境
    UPLOAD_FILES_MAP = {
        'HXZB': r'C:\Users\thinkpad\Desktop\servers\coreIndex',
        'CWFXZB': r'C:\Users\thinkpad\Desktop\servers\finAnalysisIndex',
        'CZZB': r'C:\Users\thinkpad\Desktop\servers\growthIndex',
        'DBFXZB': r'C:\Users\thinkpad\Desktop\servers\dupontAnalysisIndex',
        'GPGZ': r'C:\Users\thinkpad\Desktop\servers\stockValue',
        'JSFXZB': r'C:\Users\thinkpad\Desktop\servers\tecAnalysisIndex',
        'HYFL': r'C:\Users\thinkpad\Desktop\servers\industryClass',
        'ZQJCZB': r'C:\Users\thinkpad\Desktop\servers\secBasicIndex',
        'REC8': r'C:\Users\thinkpad\Desktop\servers\coreIndex',
        'SSRQ': r'C:\Users\thinkpad\Desktop\servers\listingDate',
    }

    # 生产环境
    # UPLOAD_FILES_MAP = {
    #     'HXZB': '/home/mba/share/coreIndex',
    #     'CWFXZB': '/home/mba/share/finAnalysisIndex',
    #     'CZZB': '/home/mba/share/growthIndex',
    #     'DBFXZB': '/home/mba/share/dupontAnalysisIndex',
    #     'GPGZ': '/home/mba/share/stockValue',
    #     'JSFXZB': '/home/mba/share/tecAnalysisIndex',
    #     'HYFL': '/home/mba/share/industryClass',
    #     'ZQJCZB': '/home/mba/share/secBasicIndex',
    #     'REC8': '/home/mba/share/coreIndex',
    #     'SSRQ': '/home/mba/share/listingDate',
    # }
    pass
