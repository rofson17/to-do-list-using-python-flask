from flask import Flask, request,url_for, render_template,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///note.db'
db=SQLAlchemy(app)
app.secret_key = 'this is a to-do-list'



#create a  database
class Todo (db.Model):
    id=db.Column(db.Integer , primary_key=True)
    tittle=db.Column(db.String(70), default="Untittle")
    Note=db.Column(db.String(250),nullable=False)
    cur_date=db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id 


@app.route('/',  methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note_tittle= request.form.get("tittle")
        note_description= request.form.get("note")

        task=Todo(tittle=note_tittle,Note=note_description)
        
        try: 
            db.session.add(task)
            db.session.commit()
            # db.section.add(new)
            flash("you are successfuly logged in", 'success')  
            return redirect(url_for('index')) 
        except:
            flash("Database error", 'danger')  
            return redirect(url_for('index'))   
            
    else:
        note_card = Todo.query.filter_by().all()
        return render_template('index.html' ,card=note_card, card_edit=None)
 
@app.route("/delete/<int:id>")
def delete(id):
    del_task=Todo.query.get_or_404(id)
    try:
        db.session.delete(del_task)
        db.session.commit()
        flash("Delete task successfully", 'warning')  
        return redirect(url_for('index')) 
    except:
        flash("Database error", 'danger')  
        return redirect(url_for('index'))   
            

@app.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
        task=Todo.query.get_or_404(id)

        if request.method=="POST":
            task.tittle=request.form["tittle"]
            task.Note=request.form["note"]
        
            try:
                db.session.commit()
                flash("Note has been updated", 'success')  
                return redirect(url_for('index'))
        
            except:
                flash("Database error", 'danger')  
                return redirect(url_for('index'))   
            

            return render_template("edit.html",card_edit=task)
        return render_template("edit.html",card_edit=task)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
    
