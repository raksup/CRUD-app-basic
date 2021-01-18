from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

@app.route('/', methods =['GET', 'POST'])
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return "There was an error!"

    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('home.html', tasks=tasks)
    

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('home'))
    except:
        return "There was a problem deleting that task."
    return render_template('delete.html')

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = ToDo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']      #adds the current form content to the db
        try:
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return "There was an error while updating your task."
    else:
        return render_template('update.html', task=task)



if __name__ == "__main__":
    app.run(debug=True)
