from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Post, Comment
from app.extensions import login_manager


main = Blueprint('main', __name__)
#admin = Blueprint('admin', __name__, url_prefix='/admin')

@main.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, password_hash=password)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('用户名或密码错误', 'danger')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录', 'info')
    return redirect(url_for('main.index'))

@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('post.html')

@main.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id).all()
    if request.method == 'POST' and current_user.is_authenticated:
        content = request.form['content']
        comment = Comment(content=content, post_id=post.id, author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.post_detail', post_id=post.id))
    return render_template('post_detail.html', post=post, comments=comments)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # 根据 ID 加载用户


#管理员
@main.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('你无权访问该页面', 'danger')
        return redirect(url_for('main.index'))

    users = User.query.all()
    return render_template('dashboard.html', users=users)


#管理员删除用户
@main.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('无权限执行此操作', 'danger')
        return redirect(url_for('main.dashboard'))

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'用户 {user.username} 已被删除', 'success')
    else:
        flash('用户不存在', 'danger')

    return redirect(url_for('main.dashboard'))
