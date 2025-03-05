from flask import Flask
from app.extensions import db, login_manager
from app.routes import main
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)

    # 设置登录视图
    login_manager.login_view = "login"
    login_manager.login_message = "请先登录"
    login_manager.login_message_category = "info"

    # 注册蓝图
    app.register_blueprint(main)
    #app.register_blueprint(admin)

    with app.app_context():
        db.create_all()

    return app
