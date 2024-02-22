from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy.schema import CheckConstraint
from werkzeug.security import generate_password_hash, check_password_hash

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

class Show(db.Model):
    __tablename__ = 'show'
    Show_ID = db.Column(db.Integer, primary_key=True)
    Movie_ID = db.Column(db.String(5), db.ForeignKey('movie.Movie_ID'))
    Show_Date = db.Column(db.Date, nullable=False)
    Screen_ID = db.Column(db.String(5), nullable=False)
    Show_Time = db.Column(db.Time, nullable=False)
    Seats_Remaining = db.Column(db.Integer, CheckConstraint('Seats_Remaining >= 0'))
    movie = db.relationship('Movie', backref='shows')

@app.route('/admin/editShow/<id>', methods=['GET', 'POST'])
def edit_show(id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    show = Show.query.get(id)
    movie = Movie.query.get(show.Movie_ID) 

    if request.method == 'POST':
        show.Movie_ID = request.form.get('movie_id')
        show.Show_Time = request.form.get('time')
        show.Seats_Remaining = request.form.get('seats_remaining')
        show.Show_Date = request.form.get('show_date')
        show.Screen_ID = request.form.get('screen_id')
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('edit_show.html', show=show, movie=movie)

@app.route('/admin/editMovie/<id>', methods=['GET', 'POST'])
def edit_movie(id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    movie = Movie.query.get(id)
    if request.method == 'POST':
        movie.Name = request.form.get('name')
        movie.Genre = request.form.get('genre')
        movie.Duration = request.form.get('duration')
        movie.Image = request.form.get('image')
        movie.Description = request.form.get('description')
        movie.Category = request.form.get('category')
        movie.Language = request.form.get('language')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_movie.html', movie=movie)

@app.route('/admin/api/delete/<id>', methods=['POST'])
def delete_movie(id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/createMovie', methods=['GET', 'POST'])
def create_movie():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    elif request.method == 'POST':
        new_id = int(Movie.query.order_by(Movie.Movie_ID.desc()).first().Movie_ID) + 1
        new_movie = Movie(Movie_ID=new_id, Name=request.form.get('name'), Genre=request.form.get('genre'), Duration=request.form.get('duration'), Image=request.form.get('image'), Description=request.form.get('description'), Category=request.form.get('category'), Language=request.form.get('language'))
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('create_movie.html')

@app.route('/admin')
def admin():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin_splash.html')

@app.route('/admin/movies')
def admin_movies():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    movies = Movie.query.all()
    return render_template('admin_movies.html', movies=movies)

@app.route('/admin/shows')
def admin_shows():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    shows = Show.query.all()
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
    movies = Movie.query.limit(6).all()
    return render_template('index.html', movies=movies)

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


if __name__ == '__main__':
    app.run(host='', port=5000, debug=True)
