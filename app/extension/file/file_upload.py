import os

from flask import current_app
from lin import Uploader
from werkzeug.utils import secure_filename

from .file import File
from ...config.development import DevelopmentConfig
from ...util import common

# 文件类型与目录映射
upload_files_map = DevelopmentConfig.UPLOAD_FILES_MAP


class FileUploader(Uploader):

    # 上传文件
    def upload(self):
        ret = []
        if self._store_dir in upload_files_map.values():
            # fileType = upload_files_map.get(fileType)
            pass



        # 创建当前文件的日期目录
        if not os.path.isabs(self._store_dir):
            self._store_dir = os.path.abspath(self._store_dir)
        self._store_dir += os.path.sep + common.get_now_time_yyyymmdd()
        if not os.path.exists(self._store_dir):
            os.makedirs(self._store_dir)
        # 拼接上传服务的请求地址
        site_domain = current_app.config.get(
            "SITE_DOMAIN",
            "http://{host}:{port}".format(
                host=current_app.config.get("FLASK_RUN_HOST", "127.0.0.1"),
                port=current_app.config.get("FLASK_RUN_PORT", "5000"),
            ),
        )
        # md5防重处理
        for single in self._file_storage:
            file_md5 = self._generate_md5(single.read())
            single.seek(0)
            exists = File.select_by_md5(file_md5)
            if exists:
                ret.append(
                    {
                        "key": single.name,
                        "id": exists.id,
                        "path": exists.path,
                        "url": site_domain
                        + os.path.join(current_app.static_url_path, exists.path),
                    }
                )
            else:
                absolute_path, relative_path, real_name = self._get_store_path(
                    single.filename
                )
                secure_filename(single.filename)
                single.save(absolute_path)
                file = File.create_file(
                    name=real_name,
                    path=relative_path,
                    extension=self._get_ext(single.filename),
                    size=self._get_size(single),
                    md5=file_md5,
                    commit=True,
                )
                ret.append(
                    {
                        "key": single.name,
                        "id": file.id,
                        "path": file.path,
                        "url": site_domain
                        + os.path.join(current_app.static_url_path, file.path),
                    }
                )
        return ret
