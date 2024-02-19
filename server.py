from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, Reservation
from jinja2 import StrictUndefined

app = Flask(__name__, template_folder='templates')
app.secret_key = "dev"
#why do we need the undefined variables to be handled with ===?
app.jinja_env.undefined = StrictUndefined

#route for the login page
# @app.route("/")
# def login():
#     return render_template('login.html')

@app.route("/")
def homepage():
    """view homepage"""

    return render_template("homepage.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    """User Login"""
    #can't use .get for some reason?
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]

        #check if login valid by first querying db for user
        #no crud file, so using postgresql
        user = User.query.filter_by(email=email).first()

        if user:
            flash('You are logged in!')
            return redirect('/')
        else:
            flash("Please make an account first")
            return redirect("/signup")
        
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another username.')
            return redirect('/signup')
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.')
        return redirect('/login')
    return render_template('signup.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        date = request.form['date']
        date = datetime.strptime(date, '%Y-%m-%d').date()
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        reservations = Reservation.query.filter_by(date=date, start_time=start_time, end_time=end_time).all()
        if reservations:
            return render_template('results.html', reservations=reservations)
        else:
            flash('No reservations available for the selected date and time range.')
    return render_template('search.html')

@app.route('/book/<int:res_id>')
def book(res_id):
    reservation = Reservation.query.get(res_id)
    if reservation:
        flash('Reservation booked successfully!')
        return redirect('/')
    else:
        flash('Reservation not found.')
        return redirect('/search')

@app.route('/my_appointments/<int:user_id>')
def my_appointments(user_id):
    user = User.query.get(user_id)
    if user:
        reservations = user.reservations
        return render_template('my_appointments.html', reservations=reservations)
    else:
        flash('User not found.')
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)