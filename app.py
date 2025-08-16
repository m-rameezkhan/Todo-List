from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), "instance", "todo.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    desc = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['todoTitle']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('hello_world'))

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return "This is Product Page"

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == 'POST':
        todo.title = request.form['todoTitle']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect(url_for('hello_world'))

    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('hello_world'))

# Create DB if not exists
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
