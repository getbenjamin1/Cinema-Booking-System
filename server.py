from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


app = Flask(__name__)

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
        'Description': movie.Description
    })

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
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
