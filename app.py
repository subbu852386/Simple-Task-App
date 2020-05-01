from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
#from flaskwebgui import FlaskUI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#ui = FlaskUI(app)

db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    note = db.Column(db.String(200))

    def __init__(self, name, note):
        self.name = name
        self.note = note

@app.route('/')
def index():
    return render_template('index.html', datas=Notes.query.all())

@app.route('/send', methods=['POST'])
def send():
    name = request.form['name']
    note = 'In-Progress'
    if name == "":
        flash("**Empty Text Detected**: Feel free Add your text under the Task field.")
    else:
        tasks = Notes(name, note)
        db.session.add(tasks)
        db.session.commit()
        flash('New Task Added :)')
    return redirect(url_for('index'))

@app.route('/receive')
def receive():
    return render_template('receive.html', datas=Notes.query.all())
    #return redirect(url_for('index'), datas=Notes.query.all())

@app.route('/delete/<id>')
def delete(id):
    task = Notes.query.filter_by(id=int(id)).delete()
    db.session.commit()
    flash('Task has been Deleted :-(')
    return redirect(url_for('index'))

@app.route('/update/<id>/<status>')
def update(id,status):
    task = Notes.query.filter_by(id=int(id)).first()
    task.note = status
    db.session.commit()
    flash('[' + task.name + '] Task Updated Successfully')
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run()
    #ui.run()