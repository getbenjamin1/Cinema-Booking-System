from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct
from sqlalchemy.sql import text
from sqlalchemy.schema import CheckConstraint
from werkzeug.security import generate_password_hash, check_password_hash
import qrcode
from io import BytesIO
import base64

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
    
def getShows():
    shows = Show.query.all()
    return shows

def getMovies():
    movies = Movie.query.all()
    return movies

def getScreens():
    screens = Screen.query.all()
    return screens

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

@app.route('/admin/bookings')
def admin_bookings():
    ensureAuth()
    bookings = Booking.query.all()
    return render_template('admin_bookings.html', bookings=bookings)

@app.route('/book/<int:Movie_ID>')
def book(Movie_ID):
    shows = Show.query.filter_by(Movie_ID=Movie_ID).all()
    movie = Movie.query.get(Movie_ID)
    return render_template('book.html', shows=shows, movie=movie)

@app.route('/bookShow', methods=['POST'])
def book_show():
    Show_ID = request.form.get('Show_ID')
    latest_booking = db.session.query(db.func.max(Booking.Booking_ID)).scalar()
    latest_booking = int(latest_booking[1:]) if latest_booking else 0
    new_booking_id = 'B' + str(latest_booking + 1).zfill(3)
    Booking_ID = request.form.get('Booking_ID', new_booking_id)
    No_of_Tickets = request.form.get('No_of_Tickets', 1)
    Total_Cost = request.form.get('Total_Cost', 5)
    Card_Number = request.form.get('Card_Number', '4638123456789101')
    Name_on_card = request.form.get('Name_on_card', 'john doe')
    User_ID = request.form.get('User_ID', 'U001')
    Email_ID = request.form.get('Email_ID', 'bla@bla.bla')

    booking = Booking(
        Booking_ID=Booking_ID,
        No_of_Tickets=int(No_of_Tickets),
        Total_Cost=int(Total_Cost),
        Card_Number=Card_Number,
        Name_on_card=Name_on_card,
        User_ID=User_ID,
        Show_ID=Show_ID,
        Email_ID=Email_ID
    )
    db.session.add(booking)
    db.session.commit()

    return new_booking_id, 200

@app.route('/admin/management', methods=['GET', 'POST'])
def test():
    ensureAuth()
    shows = getShows()
    screens = getScreens()
    return render_template('admin_screens_shows.html', screens=screens, shows=shows)

@app.route('/admin/deleteShow/<id>', methods=['POST'])
def delete_show(id):
    ensureAuth()
    show = Show.query.get(id)
    db.session.delete(show)
    db.session.commit()
    flash('Screen deleted successfully', 'success')

@app.route('/admin/deleteScreen/<id>', methods=['POST'])
def delete_screen(id):
    ensureAuth()

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
    ensureAuth()

    screens = getScreens()
    return render_template('admin_screens.html', screens=screens)
@app.route('/admin/editScreen/<screen_id>', methods=['GET', 'POST'])
def edit_screen(screen_id):
    ensureAuth()

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
    ensureAuth()
    
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

    ensureAuth()
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
    ensureAuth()
    if request.method == 'POST':
        new_show = Show(Show_ID=new_id, Movie_ID=request.form.get('movie_id'), Show_Date=request.form.get('show_date'), Screen_ID=request.form.get('screen_id'), Show_Time=request.form.get('time'), Seats_Remaining=request.form.get('seats_remaining'))
        db.session.add(new_show)
        db.session.commit()
        return redirect(url_for('test'))
    return render_template('create_show.html', new_id=new_id)

   
@app.route('/admin/editMovie/<id>', methods=['GET', 'POST'])
def edit_movie(id):
    ensureAuth()
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
    ensureAuth()
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('admin_movies'))

@app.route('/admin/createMovie', methods=['GET', 'POST'])
def create_movie():
    ensureAuth()
    if request.method == 'POST':
        new_id = int(Movie.query.order_by(Movie.Movie_ID.desc()).first().Movie_ID) + 1
        new_movie = Movie(Movie_ID=new_id, Name=request.form.get('name'), Genre=request.form.get('genre'), Duration=request.form.get('duration'), Image=request.form.get('image'), Description=request.form.get('description'), Category=request.form.get('category'), Language=request.form.get('language'), Rating=request.form.get('rating'), Trailer=request.form.get('trailer'))
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('create_movie.html')

@app.route('/admin')
def admin():
    ensureAuth()
    return render_template('admin_splash.html')

@app.route('/admin/movies')
def admin_movies():
    ensureAuth()
    movies = getMovies()
    return render_template('admin_movies.html', movies=movies)

@app.route('/admin/shows')
def admin_shows():
    ensureAuth()
    shows = getShows()
    return render_template('admin_shows.html', shows=shows)

@app.route('/login', methods=['GET', 'POST'])
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

    # Fetch shows for each screen ID
    shows = {}
    for screen_id in screen_ids:
        shows[screen_id] = Show.query.filter_by(Screen_ID=screen_id).all()

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
