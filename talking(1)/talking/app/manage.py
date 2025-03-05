from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

def create_admin():
    with app.app_context():
        username = "qwe"
        password = "admin123"

        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"用户 '{username}' 已存在，跳过创建！")
            return

        # 创建新管理员
        admin = User(
            username=username,
            password=generate_password_hash(password),  # 确保密码是哈希的
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("管理员账号创建成功！")

if __name__ == "__main__":
    create_admin()
