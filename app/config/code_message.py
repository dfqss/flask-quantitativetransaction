"""
  消息码配置文件
  格式：消息码 -> 消息
"""

MESSAGE = {
    # 码值-成功
    0: "成功",
    1: "创建成功",
    2: "更新成功",
    3: "删除成功",
    4: "密码修改成功",
    5: "删除用户成功",
    6: "更新用户成功",
    7: "更新分组成功",
    8: "删除分组成功",
    9: "添加权限成功",
    10: "删除权限成功",
    11: "注册成功",
    12: "新建图书成功",
    13: "更新图书成功",
    14: "删除图书成功",
    15: "新建分组成功",
    16: "添加股票池成功",

    # 码值-失败
    9999: "服务器未知错误",
    10000: "未携带令牌",
    10001: "权限不足",
    10010: "授权失败",
    10011: "更新密码失败",
    10012: "请传入认证头字段",
    10013: "认证头字段解析失败",
    10020: "资源不存在",
    10021: "用户不存在",
    10022: "未找到相关书籍",
    10023: "分组不存在，无法新建用户",
    10024: "分组不存在",
    10025: "找不到相应的视图处理器",
    10026: "未找到文件",
    10030: "参数错误",
    10031: "用户名或密码错误",
    10032: "请输入正确的密码",
    10040: "令牌失效",
    10041: "access token 损坏",
    10042: "refresh token 损坏",
    10050: "令牌过期",
    10051: "access token 过期",
    10052: "refresh token 过期",
    10060: "字段重复",
    10070: "禁止操作",
    10071: "已经有用户使用了该名称，请重新输入新的用户名",
    10072: "分组名已被使用，请重新填入新的分组名",
    10073: "root分组不可添加用户",
    10074: "root分组不可删除",
    10075: "guest分组不可删除",
    10076: "邮箱已被使用，请重新填入新的邮箱",
    10077: "不可将用户分配给不存在的分组",
    10078: "不可修改root用户的分组",
    10080: "请求方法不允许",
    10100: "刷新令牌获取失败",
    10110: "文件体积过大",
    10120: "文件数量过多",
    10121: "文件太多",
    10130: "文件扩展名不符合规范",
    10140: "请求过于频繁，请稍后重试",
    10150: "丢失参数",
    10160: "类型错误",
    10170: "请求体不可为空",
    10180: "全部文件大小不能超过",
    10190: "读取文件数据失败",
    10200: "失败",
    10201: "添加股票池失败",
    10202: "查询核心指数列表失败",
    10203: "查询股票池列表失败",
    10204: "查询核心指数历史列表失败",
    10205: "查询杜邦指标列表失败",
    10206: "查询财务分析指标列表失败",
    10207: "查询成长指标列表失败",
    10301: "查询行业分类列表失败",
    10302: "查询证券基础指标列表失败",
    10303: "查询股票估值列表失败",
    10304: "查询技术分析指标列表失败"
}
