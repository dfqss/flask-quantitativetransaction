import os

# from flask import current_app
from lin import Uploader
from werkzeug.utils import secure_filename

from .file import File
from ...util import common, files


class FileUploader(Uploader):

    # 上传文件
    def upload(self):
        ret = []
        # 获取文件路径和文件名称
        full_path = self._store_dir.split("|")
        filePath = full_path[0]
        fileName = full_path[1]
        self._store_dir = filePath
        # 创建当前文件的日期目录
        if not os.path.isabs(filePath):
            filePath = os.path.abspath(filePath)
        filePath += os.path.sep + common.get_now_time_yyyymmdd()
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        # 拼接上传服务的请求地址
        # site_domain = current_app.config.get(
        #     "SITE_DOMAIN",
        #     "http://{host}:{port}".format(
        #         host=current_app.config.get("FLASK_RUN_HOST", "127.0.0.1"),
        #         port=current_app.config.get("FLASK_RUN_PORT", "5000"),
        #     ),
        # )
        # 循环处理文件列表
        for single in self._file_storage:
            # md5防重处理
            file_md5 = self._generate_md5(single.read())
            single.seek(0)
            # 查看是否已经导入该文件
            exists = File.select_by_md5(file_md5)
            if exists:
                # 如果存在该文件则直接返回该文件信息
                ret.append(
                    {
                        "key": fileName,
                        "id": exists.id,
                        "path": exists.path,
                        "repetition": "true",
                        # "url": site_domain
                        #        + os.path.join(current_app.static_url_path, exists.path),
                    }
                )
            else:
                # 如果不存在则创建文件后返回文件信息
                absolute_path = os.path.join(filePath, fileName)
                secure_filename(fileName)
                # 创建数据文件到指定目录
                single.save(absolute_path)
                # 创建同名.ok文件
                file_ok = files.modifyFileSuffix(absolute_path, self._get_ext(fileName), '.ok')
                open(file_ok, 'w').close()
                # 创建文件表数据记录
                file = File.create_file(
                    name=fileName,
                    path=filePath,
                    extension=self._get_ext(fileName),
                    size=self._get_size(single),
                    md5=file_md5,
                    commit=True,
                )
                # 拼接返回参数
                ret.append(
                    {
                        "key": fileName,
                        "id": file.id,
                        "path": file.path,
                        "repetition": "false",
                        # "url": site_domain + os.path.join(current_app.static_url_path, file.path),
                    }
                )
        return ret
