from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)                   #                 user:senha
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost/myDbName"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://joao:senha@127.0.0.1/flask"
db = SQLAlchemy(app)

class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
@app.route("/", methods=['POST', 'GET'])

def hello():
    if request.method == 'POST':
        #return "Olá Mercúrio"
        task_content = request.form['content']
        new_task = todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Erro'
        
    else:
        tasks = todo.query.order_by(todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    #return "Hello World!"
    #return "Hello Moon!"

@app.route('/delete/<int:id>')

def delete(id):
    task_to_delete = todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return('Erro')

@app.route('/update/<int:id>', methods=['GET', 'POST'])

def update(id):
    task = todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Erro'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)



#para desativar o flask, basta rodar deactivate
