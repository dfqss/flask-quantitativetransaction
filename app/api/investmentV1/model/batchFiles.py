from lin import InfoCrud
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func


# 核心指标表
class MbaBatchFiles(InfoCrud):
    file_name = Column(String(60), primary_key=True, comment='文件名称')
    file_path = Column(String(60), comment='文件路径')
    status = Column(String(30), comment='文件读取状态 0-未读 1-读取成功 2-读取失败')
    description = Column(String(255), comment='描述')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        batch_files = {
            'file_name': self.file_name,
            'file_path': self.file_path,
            'status': self.status,
            'description': self.description,
            'create_time': self.create_time,
            'update_time': self.update_time
        }
        return batch_files
