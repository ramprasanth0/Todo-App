from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

#------database integration-------
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
db=SQLAlchemy(app)

#-------database model for orm----------
class Todo(db.Model):
    __tablename__='todo'
    id=db.Column(db.Integer,primary_key=True)
    task_content=db.Column(db.String(100),nullable=False)
    time=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f'<Todo {self.id}>'

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        task_content=request.form['content']
        task=Todo(task_content=task_content)
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return "Unable to complete Task creation"
    else:
        todos=Todo.query.order_by(Todo.time).all()       
        return render_template('index.html',todos=todos)

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    curr_todo=Todo.query.get_or_404(id)
    if request.method=='POST':
        curr_todo.task_content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Task could not be updated"
    else:
        return render_template('update.html',todo=curr_todo)



@app.route('/delete/<int:id>')
def delete(id):
    todo_to_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(todo_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Unable to delete task"

# t=Todo()
# print(t)
