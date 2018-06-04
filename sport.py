import os
from flask import Flask 
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy 

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "sportdatabase.db"))

app = Flask(__name__)
SQLALCHEMY_TRACK_MODIFICATIONS = True
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Sport(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    qty= db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        newqty = request.form.get("newqty")
        oldqty = request.form.get("oldqty")
        sport = Sport.query.filter_by(title=oldtitle).first()
        sport = Sport.query.filter_by(qty=oldqty).first()
        sport.title = newtitle
        sport.qty = newqty
        db.session.commit()
    except Exception as e:
        print("Couldn't update sport title")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    sport = Sport.query.filter_by(title=title).first()
    db.session.delete(sport)
    db.session.commit()
    return redirect("/")

@app.route("/", methods=["GET", "POST"])
def home():
	sports = None
	if request.form:
		try:
			sport = Sport(title=request.form.get("title"),qty=request.form.get("qty"))
			db.session.add(sport)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			print("Failed to add sport item")
			print(e)
	sports = Sport.query.all()
	return render_template("home.html", sports=sports)

if __name__ == "__main__":
	app.run(debug=True)