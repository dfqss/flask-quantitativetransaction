from flask import Blueprint, request, Flask
from lin import login_required

from app.api import AuthorizationBearerSecurity, api
from app.api.investmentV1.exception.result import failed, success
from app.config.development import DevelopmentConfig
from app.extension.file.file_upload import FileUploader
from app.util import common
import datetime

app = Flask(__name__)
upload_api = Blueprint("upload", __name__)

# 文件类型与目录映射
upload_files_map = DevelopmentConfig.UPLOAD_FILES_MAP


@upload_api.route("/uploadFile", methods=["POST"])
@login_required
@api.validate(
    tags=["文件"],
    security=[AuthorizationBearerSecurity],
)
def uploadFile():
    # 获取上传文件列表
    files = request.files
    # 获取表单数据
    formData = request.form
    app.logger.info('start service uploadFile------服务入参：' + str(formData) + '\n' + str(files))
    # 获取文件类型
    fileType = formData.get('fileType')
    periods = formData.get('periods')
    # 判断文件类型是否为空
    if fileType is None or len(fileType.strip()) <= 0:
        app.logger.error('上传的文件类型为空' + str(files))
        return failed(10208)
    if fileType in upload_files_map:
        filePath = upload_files_map.get(fileType)
        fileName = get_file_name(fileType, periods, '.xlsx')
    else:
        app.logger.error('该文件不在可上传的文件类型中' + str(files))
        return failed(10210)
    # 上传文件
    try:
        uploader = FileUploader(files, config={'STORE_DIR': filePath + '|' + fileName})
        upload_ret = uploader.upload()
    except Exception as e:
        app.logger.error('上传文件失败:' + str(files))
        app.logger.error('文件类型:' + str(fileType))
        app.logger.error('失败原因:' + str(e))
        return failed(10209)
    # 返回参数信息
    successMap = success(17)
    successMap['upload_ret'] = upload_ret
    app.logger.info('end service uploadFile------服务出参：' + str(successMap))
    return successMap


# 获取文件名称
def get_file_name(fileType, periods, suffix):
    if fileType == 'REC8':
        fileName = 'HXZB_REC8_' + periods + '_END8_' + common.get_now_time_yyyymmdd()
    else:
        fileName = fileType + '_' + common.get_now_time_yyyymmdd()
    return fileName + '_' + str(datetime.datetime.now().microsecond) + suffix
