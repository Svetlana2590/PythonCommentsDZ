from flask import Flask, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__) #создаём приложение
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/contacts' #ссылка для подключения
db = SQLAlchemy(app) #передаём приложение
migrate = Migrate(app, db)


class User(db.Model):  #передаём таблицу
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)


@app.route('/') #создаем главную страницу
def index():
    return render_template('index.html', message="Привет из index.html")


@app.route('/greet', methods=['POST']) #добавление пользователя в таблицу
def greet():
    name = request.form['name']
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    return render_template('index.html', message=f'Привет, {name}!')


@app.route('/users/') #добавление пользователей в базу
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/number/<int:num>') #ввод числа
def number(num):
    return render_template('index.html', message=f"Number: {num}", number=num, sps=['test', 'qwer'])


@app.route('/projects/check/user/<username>')
@app.route('/user/<username>') #ввод имени
def user(username):
    return render_template('index.html', message=f"Hello, {username}!", number=0)


@app.route('/test/<int:test_num>') #генерация ссылки
def test(test_num):
    return f"[ {test_num},\n {url_for('user', username=f'user{test_num}')} ]"


if __name__ == '__main__': #открытый хост и отладчик
    app.run(host='0.0.0.0', debug=True)
