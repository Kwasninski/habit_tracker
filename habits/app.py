'''simple habit tracking app'''

# app features

# 1. add a habit
# 2. start tracking time from current time
# 3. add a counter +1 each 24h
# 4. ability to "reset" the counter by clicking a button


# imports

from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from datetime import datetime

#initialize the Flask application
app = Flask(__name__)
Scss(app)

#configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#Define the Habit model ~ row of data
class Habit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	counter = db.Column(db.Integer, default=0)
	date_created = db.Column(db.DateTime, default=datetime.now)

	def __repr__(self) -> str:
		return f"Habit {self.id} - {self.name}"

with app.app_context():
	db.create_all()

#home page
@app.route("/", methods=['GET', 'POST'])
def main():
	#add habit
	if request.method == 'POST':
		current_habit_name = request.form['name']
		new_habit = Habit(name=current_habit_name)
		try:
			db.session.add(new_habit)
			db.session.commit()
			return redirect('/')
		except Exception as e:
			return f"there was an issue adding your habit: {e}"
	#see all current habits
	else:
		habits = Habit.query.order_by(Habit.date_created).all()
		return render_template("index.html", habits=habits)


#delete an item
@app.route("/delete/<int:id>")
def delete(id):
    habit_to_delete = Habit.query.get_or_404(id)
    try:
        db.session.delete(habit_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"there was a problem deleting that task: {e}"
	


# update habit name
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
	habit = Habit.query.get_or_404(id)
	if request.method == 'POST':
		habit.name = request.form['name']
		try:
			db.session.commit()
			return redirect('/')
		except Exception as e:
			return f"there was an issue updating your habit: {e}"
	else:
		return render_template('update.html', habit=habit)
	

# increment habit counter
@app.route("/increment/<int:id>")
def increment(id):
	habit = Habit.query.get_or_404(id)
	habit.counter += 1
	try:
		db.session.commit()
		return redirect('/')
	except Exception as e:
		return f"there was a problem incrementing the counter: {e}"


# reset habit counter
@app.route("/reset-counter/<int:id>")
def reset_counter(id):
	habit_counter_reset = Habit.query.get_or_404(id)
	habit_counter_reset.counter *= 0
	try:
		db.session.commit()
		return redirect('/')
	except Exception as e:
		return f"There was a problem reseting the counter: {e}"




#run the app
if __name__ == "__main__":
	app.run(debug=True)