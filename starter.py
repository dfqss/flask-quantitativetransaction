"""
        :copyright: © 2020 by the Lin team.
        :license: MIT, see LICENSE for more details.
    """

from app import create_app
from app.api.cms.model.group import Group
from app.api.cms.model.group_permission import GroupPermission
from app.api.cms.model.permission import Permission
from app.api.cms.model.user import User
from app.api.cms.model.user_group import UserGroup
from app.api.cms.model.user_identity import UserIdentity
from app.config.code_message import MESSAGE

from app.api.investmentV1.scheduler.decorator import executeJob

app = create_app(
    group_model=Group,
    user_model=User,
    group_permission_model=GroupPermission,
    permission_model=Permission,
    identity_model=UserIdentity,
    user_group_model=UserGroup,
    config_MESSAGE=MESSAGE,
)


if app.config.get("ENV") != "production":

    @app.route("/")
    def slogan():
        return """
        <style type="text/css">
            * {
                padding: 0;
                margin: 0;
            }

            div {
                padding: 4px 48px;
            }

            a {
                color: black;
                cursor: pointer;
                text-decoration: none
            }

            a:hover {
                text-decoration: None;
            }

            body {
                background: #fff;
                font-family:
                    "Century Gothic", "Microsoft yahei";
                color: #333;
                font-size: 18px;
            }

            h1 {
                font-size: 100px;
                font-weight: normal;
                margin-bottom: 12px;
            }

            p {
                line-height: 1.6em;
                font-size: 42px
            }
        </style>
        <div style="padding: 24px 48px;">
            <p>
                <a href="https://www.talelin.com" target="_Blank">Lin</a>
                <br />
                <span style="font-size:30px">
                    <a href="/apidoc/redoc">心上无垢</a>，<a href="/apidoc/swagger">林间有风</a>。
                </span>
            </p>
        </div>
        """


"""
# coding:utf-8
@Time    : 2022/04/30
@Author  : sushuai
@desc    : 使用装饰器定时启动任务
@notes   : 使用flask run命令启动时，需要将调用函数写在最外层，才能正确调用
           使用py命令调用时，需要将调用函数写在主函数里才能正确调用
"""
executeJob()


if __name__ == "__main__":
    app.logger.warning(
        """
        ----------------------------
        |  app.run() => flask run  |
        ----------------------------
        """
    )
    app.run()
