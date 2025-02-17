from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct
from sqlalchemy.sql import text
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash
import qrcode
from io import BytesIO
import base64
import datetime

admin_pw = "homersimpson99"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bartlikesdarts'
db_username, db_password, db_name = "bartsimpson", "duffdrinker", "debianem" 
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_username}:{db_password}@localhost/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__ = 'movie'
    Movie_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Genre = db.Column(db.String(50))
    Duration = db.Column(db.Integer)
    Image = db.Column(db.String(100))
    Description = db.Column(db.Text)
    Category = db.Column(db.String(20))
    Language = db.Column(db.String(20))
    Trailer = db.Column(db.String(200))
    Rating = db.Column(db.Float)


class Screen(db.Model):
    __tablename__ = 'screen'
    Screen_ID = db.Column(db.Integer, primary_key=True)
    No_of_Seats = db.Column(db.Integer, nullable=False)

class Show(db.Model):
    __tablename__ = 'show'
    Show_ID = db.Column(db.Integer, primary_key=True)
    Movie_ID = db.Column(db.String(5), db.ForeignKey('movie.Movie_ID'))
    Show_Date = db.Column(db.Date, nullable=False)
    Screen_ID = db.Column(db.String(5), nullable=False)
    Show_Time = db.Column(db.Time, nullable=False)
    Seats_Remaining = db.Column(db.Integer, CheckConstraint('Seats_Remaining >= 0'))
    movie = db.relationship('Movie', backref='shows')

class Booking(db.Model):
    __tablename__ = 'booking'
    Booking_ID = db.Column(db.String(10), primary_key=True)
    No_of_Tickets = db.Column(db.Integer, nullable=False)
    Total_Cost = db.Column(db.Integer, nullable=False)
    Card_Number = db.Column(db.String(19))
    Name_on_card = db.Column(db.String(21))
    User_ID = db.Column(db.String(5))
    Show_ID = db.Column(db.Integer)
    Email_ID = db.Column(db.String(30))

def ensureAuth():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    return None
    
def getShows():
    shows = Show.query.all()
    return shows

def getMovies():
    movies = Movie.query.all()
    return movies

def getScreens():
    screens = Screen.query.all()
    return screens

def subtractSeat(show_id, no_of_tickets):
    show = Show.query.get(show_id)
    if show:
        if show.Seats_Remaining >= no_of_tickets:
            show.Seats_Remaining -= no_of_tickets
            db.session.commit()
            return True
        else:
            return False
    else:
        return False


@app.route('/viewTicket', methods=['POST'])
def view_ticket():
    ticket_id_b64 = request.data.decode('utf-8')

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(ticket_id_b64)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    image_buffer = BytesIO()
    img.save(image_buffer, format="PNG")
    image_data = base64.b64encode(image_buffer.getvalue()).decode('utf-8')

    return render_template('viewTicket.html', image_data=image_data)

def addToWeeklyReport(Show_ID, No_of_Tickets):
    # Get current date
    current_date = datetime.datetime.now()
    # Calculate the start of the current week (assuming Monday is the start of the week)
    start_of_week = current_date - datetime.timedelta(days=current_date.weekday())
    # Calculate the end of the current week
    end_of_week = start_of_week + datetime.timedelta(days=6)
    # Format the start and end dates
    start_of_week_str = start_of_week.strftime("%Y-%m-%d")
    end_of_week_str = end_of_week.strftime("%Y-%m-%d")

    # Create or open the file in append mode
    with open("weekly_report.txt", "a") as file:
        # Write the data to the file
        file.write(f"Show_ID: {Show_ID}, No_of_Tickets: {No_of_Tickets}, Week: {start_of_week_str} to {end_of_week_str}\n")

@app.route('/admin/bookings')
def admin_bookings():
    r = ensureAuth()
    if r is not None:
        return r
    bookings = Booking.query.all()
    return render_template('admin_bookings.html', bookings=bookings)

@app.route('/book/<int:Movie_ID>')
def book(Movie_ID):
    shows = Show.query.filter_by(Movie_ID=Movie_ID).all()
    movie = Movie.query.get(Movie_ID)
    return render_template('book.html', shows=shows, movie=movie)

@app.route('/bookShow', methods=['POST'])
def book_show():
    print(request.form)
    show_id = request.form.get('Show_ID')
    no_of_tickets = int(request.form.get('No_of_Tickets', 1))

    if subtractSeat(show_id, no_of_tickets):
        # Proceed with booking
        latest_booking = db.session.query(db.func.max(Booking.Booking_ID)).scalar()
        latest_booking = int(latest_booking[1:]) if latest_booking else 0
        new_booking_id = 'B' + str(latest_booking + 1).zfill(3)
        booking_id = request.form.get('Booking_ID', new_booking_id)
        total_cost = request.form.get('Total_Cost', 5)
        card_number = request.form.get('Card_Number', '4638123456789101')
        name_on_card = request.form.get('Name_on_card', 'john doe')
        user_id = request.form.get('User_ID', 'U001')
        email_id = request.form.get('Email_ID', 'bla@bla.bla')

        booking = Booking(
            Booking_ID=booking_id,
            No_of_Tickets=int(no_of_tickets),
            Total_Cost=int(total_cost),
            Card_Number=card_number,
            Name_on_card=name_on_card,
            User_ID=user_id,
            Show_ID=show_id,
            Email_ID=email_id
        )
        db.session.add(booking)
        db.session.commit()
        addToWeeklyReport(show_id, no_of_tickets)

        return new_booking_id, 200
    else:
        return "Not enough available seats", 400


@app.route('/admin/report')

def weekly_report():
    r = ensureAuth()
    if r is not None:
        return r
    # Read the contents of the weekly report file
    with open("weekly_report.txt", "r") as file:
        report_data = file.readlines()

    # Initialize dictionary to store show counts
    show_counts = {}

    # Initialize variable to store total weekly tickets sold
    total_tickets_sold = 0

    # Parse the report data
    for line in report_data:
        parts = line.strip().split(", ")
        show_id = parts[0].split(": ")[1]
        tickets = int(parts[1].split(": ")[1])
        date_range = parts[2].split(": ")[1].split(" to ")
        start_date = datetime.datetime.strptime(date_range[0], "%Y-%m-%d")
        end_date = datetime.datetime.strptime(date_range[1], "%Y-%m-%d")

        # Fetch movie name from the Show table
        show = Show.query.get(show_id)
        movie_name = show.movie.Name

        # Aggregate ticket counts for each show
        show_counts.setdefault(movie_name, 0)
        show_counts[movie_name] += tickets

        # Increment the total tickets sold only once per ticket sold
        total_tickets_sold += tickets

    # Render a template with the parsed data
    return render_template('weekly_report.html', show_counts=show_counts, total_tickets_sold=total_tickets_sold)


@app.route('/admin/management', methods=['GET', 'POST'])
def test():
    r = ensureAuth()
    if r is not None:
        return r
    shows = getShows()
    screens = getScreens()
    return render_template('admin_screens_shows.html', screens=screens, shows=shows)

@app.route('/admin/deleteShow/<id>', methods=['POST'])
def delete_show(id):
    r = ensureAuth()
    if r is not None:
        return r
    show = Show.query.get(id)
    db.session.delete(show)
    db.session.commit()
    flash('Screen deleted successfully', 'success')

@app.route('/admin/deleteScreen/<id>', methods=['POST'])
def delete_screen(id):
    r = ensureAuth()
    if r is not None:
        return r

    screen = Screen.query.get(id)

    if screen is None:
        flash('Screen not found', 'error')
    else:
        db.session.delete(screen)
        db.session.commit()
        flash('Screen deleted successfully', 'success')

    return redirect(url_for('test'))

@app.route('/movies/<int:movie_id>')
def movie(movie_id):
        movie = Movie.query.get_or_404(movie_id)
        return render_template('movie.html', movie=movie)

@app.route('/admin/screens')
def admin_screens():
    r = ensureAuth()
    if r is not None:
        return r

    screens = getScreens()
    return render_template('admin_screens.html', screens=screens)
@app.route('/admin/editScreen/<screen_id>', methods=['GET', 'POST'])
def edit_screen(screen_id):
    r = ensureAuth()
    if r is not None:
        return r

    screen = Screen.query.get(screen_id)

    if screen is None:
        flash('Screen not found', 'error')
        return redirect(url_for('test'))

    if request.method == 'POST':
            screen.No_of_Seats = int(request.form.get('seats'))
            db.session.commit()

            flash('Screen updated successfully', 'success')
            return redirect(url_for('test'))

    return render_template('edit_screen.html', screen=screen)

@app.route('/admin/editShow/<id>', methods=['GET', 'POST'])
def edit_show(id):
    r = ensureAuth()
    if r is not None:
        return r
    
    show = Show.query.get(id)
    movie = Movie.query.get(show.Movie_ID) 

    if request.method == 'POST':
        show.Movie_ID = request.form.get('movie_id')
        show.Show_Time = request.form.get('time')
        show.Seats_Remaining = request.form.get('seats_remaining')
        show.Show_Date = request.form.get('show_date')
        show.Screen_ID = request.form.get('screen_id')
        db.session.commit()
        return redirect(url_for('test'))

    return render_template('edit_show.html', show=show, movie=movie)

@app.route('/admin/createScreen', methods=['GET', 'POST'])
def create_screen():
    global new_id
    highest_screen = Screen.query.order_by(Screen.Screen_ID.desc()).first()
    new_id = int(highest_screen.Screen_ID) + 1  #==

    r = ensureAuth()
    if r is not None:
        return r
    if request.method == 'POST':
        highest_screen = Screen.query.order_by(Screen.Screen_ID.desc()).first()
        no_of_seats = request.form.get('no_of_seats')
        new_screen = Screen(Screen_ID=new_id, No_of_Seats=no_of_seats)
        db.session.add(new_screen)
        db.session.commit()
        return redirect(url_for('test'))

    return render_template('create_screen.html', new_id=new_id)

@app.route('/admin/createShow', methods=['GET', 'POST'])
def create_show():
    global new_id
    new_id = int(Show.query.order_by(Show.Show_ID.desc()).first().Show_ID) + 1
    r = ensureAuth()
    if r is not None:
        return r
    if request.method == 'POST':
        new_show = Show(Show_ID=new_id, Movie_ID=request.form.get('movie_id'), Show_Date=request.form.get('show_date'), Screen_ID=request.form.get('screen_id'), Show_Time=request.form.get('time'), Seats_Remaining=request.form.get('seats_remaining'))
        db.session.add(new_show)
        db.session.commit()
        return redirect(url_for('test'))
    return render_template('create_show.html', new_id=new_id)

   
@app.route('/admin/editMovie/<id>', methods=['GET', 'POST'])
def edit_movie(id):
    r = ensureAuth()
    if r is not None:
        return r
    movie = Movie.query.get(id)
    if request.method == 'POST':
        movie.Name = request.form.get('name')
        movie.Genre = request.form.get('genre')
        movie.Duration = request.form.get('duration')
        movie.Image = request.form.get('image')
        movie.Description = request.form.get('description')
        movie.Category = request.form.get('category')
        movie.Language = request.form.get('language')
        movie.Rating = request.form.get('rating')
        movie.Trailer = request.form.get('trailer')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_movie.html', movie=movie)

@app.route('/admin/api/delete/<id>', methods=['POST'])
def delete_movie(id):
    r = ensureAuth()
    if r is not None:
        return r
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('admin_movies'))

@app.route('/admin/createMovie', methods=['GET', 'POST'])
def create_movie():
    r = ensureAuth()
    if r is not None:
        return r
    if request.method == 'POST':
        new_id = int(Movie.query.order_by(Movie.Movie_ID.desc()).first().Movie_ID) + 1
        new_movie = Movie(Movie_ID=new_id, Name=request.form.get('name'), Genre=request.form.get('genre'), Duration=request.form.get('duration'), Image=request.form.get('image'), Description=request.form.get('description'), Category=request.form.get('category'), Language=request.form.get('language'), Rating=request.form.get('rating'), Trailer=request.form.get('trailer'))
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('create_movie.html')

@app.route('/admin')
def admin():
    r = ensureAuth()
    if r is not None:
        return r
    return render_template('admin_splash.html')

@app.route('/admin/movies')
def admin_movies():
    r = ensureAuth()
    if r is not None:
        return r
    movies = getMovies()
    return render_template('admin_movies.html', movies=movies)

@app.route('/admin/shows')
def admin_shows():
    r = ensureAuth()
    if r is not None:
        return r
    shows = getShows()
    return render_template('admin_shows.html', shows=shows)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = generate_password_hash(admin_pw)
        if admin is not None and check_password_hash(admin, password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password')
    if 'admin_logged_in' in session and session['admin_logged_in']:
        return redirect(url_for('admin'))
    else:
        session['visited_some_page'] = True
        return render_template('login.html')
    
@app.route('/')
def index():
    screen_ids = db.session.query(distinct(Show.Screen_ID)).all()
    screen_ids = [str(screen_id[0]) for screen_id in screen_ids]

    # Fetch the first show for each screen ID
    shows = {}
    for screen_id in screen_ids:
        show = Show.query.filter_by(Screen_ID=screen_id).first()
        if show:  # Check if a show exists for the screen ID
            shows[screen_id] = show

    return render_template('index.html', screen_ids=screen_ids, shows=shows)



@app.route('/api/movie/<int:movie_id>')
def get_movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return jsonify({
        'Movie_ID': movie.Movie_ID,
        'Name': movie.Name,
        'Genre': movie.Genre,
        'Duration': movie.Duration,
        'Image': movie.Image,
        'Description': movie.Description,
        'Category': movie.Category,
        'Language': movie.Language
    })
    
@app.route('/api/all-movies')
def get_all_movies():
    movies = getMovies()
    movie_data = [{
        'Movie_ID': movie.Movie_ID,
        'Name': movie.Name,
        'Genre': movie.Genre,
        'Duration': movie.Duration,
        'Image': movie.Image,
        'Description': movie.Description,
        'Category': movie.Category,
        'Language': movie.Language
    } for movie in movies]
    return jsonify(movie_data)


@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    db.session.commit()
    results = Movie.query.filter(Movie.Name.ilike(f'%{query}%')).all()
    return jsonify([{
        'Movie_ID': movie.Movie_ID,
        'Name': movie.Name,
        'Genre': movie.Genre,
        'Duration': movie.Duration,
        'Image': movie.Image,
    } for movie in results])
    return render_template('index.html', screen_ids=screen_ids, shows=shows)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/watchanddine')
def watchdine():
    return render_template('watch+dine.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='', port=5000, debug=True)
