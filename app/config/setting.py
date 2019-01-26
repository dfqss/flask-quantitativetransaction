"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from datetime import timedelta

# 分页配置
COUNT_DEFAULT = 10
PAGE_DEFAULT = 0

# 令牌配置
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

# 插件模块暂时没有开启，以下配置可忽略
# plugin config写在字典里面
PLUGIN_PATH = {
    'oss': {'path': 'app.plugins.oss', 'enable': True, 'upload_folder': 'app/static'},
    'poem': {'path': 'app.plugins.poem', 'enable': True, 'limit': 5},
}
