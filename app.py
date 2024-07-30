"""Importing Modules"""
from datetime import datetime
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
# My App
app = Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

# Data Class ~ Raw of Data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    compelte = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task : {self.id}"
    
with app.app_context():
        db.create_all()
# Main Route ~ Main page
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try :
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERORR : {e}")
            return f"Error : {e}"
        
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)

    return render_template('index.html')


@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error {e}"


@app.route("/update/<int:id>", methods=['GET','POST'])
def update(id:int):
    edit_task = MyTask.query.get_or_404(id)
    if request.method == 'POST':
        edit_task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error {e}"
    else:
        return render_template('edit.html', task=edit_task)    


if __name__ == '__main__':
    app.run(debug=True)