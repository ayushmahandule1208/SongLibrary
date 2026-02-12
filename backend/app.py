from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import func
from models import db, Song
from config import config
from data_processor import DataProcessor
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_name='default'):
    """Application factory pattern"""
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # Create tables and load raw data
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")

        # Path to raw_songs.json (same folder as app.py)
        file_path = os.path.join(os.path.dirname(__file__), "raw_songs.json")

        if os.path.exists(file_path):
            # Load only if DB is empty (prevents duplicate reload)
            if Song.query.count() == 0:
                inserted_count = DataProcessor.process_json_file(file_path)
                logger.info(f"Raw songs loaded successfully ({inserted_count} inserted)")
            else:
                logger.info("Database already contains data. Skipping JSON load.")
        else:
            logger.warning("raw_songs.json not found.")

    # Register routes
    register_routes(app)
    
    return app



def register_routes(app):
    """Register all API routes"""
    
    @app.route('/', methods=['GET'])
    def index():
        """Health check endpoint"""
        return jsonify({
            'status': 'success',
            'message': 'Song Playlist API is running',
            'version': '1.0.0',
            'endpoints': {
                'GET /api/songs': 'Get all songs with pagination',
                'GET /api/songs/<id>': 'Get song by ID',
                'GET /api/songs/search': 'Search songs by title',
                'PUT /api/songs/<id>/rating': 'Update song rating',
                'POST /api/songs/upload': 'Upload JSON data',
                'GET /api/stats': 'Get database statistics'
            }
        }), 200
    
    
    # ===========================================
    # 1.2.1 [MUST HAVE] Get all songs with pagination
    # ===========================================
    @app.route('/api/songs', methods=['GET'])
    def get_all_songs():
        """
        Get all songs with pagination support
        
        Query Parameters:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 10, max: 100)
            sort_by (str): Column to sort by (default: index)
            order (str): Sort order - 'asc' or 'desc' (default: asc)
        
        Returns:
            JSON response with paginated songs
        """
        try:
            # Get query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', app.config['DEFAULT_PAGE_SIZE'], type=int)
            sort_by = request.args.get('sort_by', 'index', type=str)
            order = request.args.get('order', 'asc', type=str).lower()
            
            # Validate parameters
            if page < 1:
                return jsonify({'error': 'Page number must be >= 1'}), 400
            
            if per_page < 1 or per_page > app.config['MAX_PAGE_SIZE']:
                return jsonify({'error': f'per_page must be between 1 and {app.config["MAX_PAGE_SIZE"]}'}), 400
            
            # Validate sort column
            valid_sort_columns = ['index', 'id', 'title', 'danceability', 'energy', 
                                  'tempo', 'duration_ms', 'star_rating', 'created_at']
            if sort_by not in valid_sort_columns:
                return jsonify({'error': f'Invalid sort_by column. Valid columns: {valid_sort_columns}'}), 400
            
            # Build query with sorting
            query = Song.query
            
            # Handle special case for 'class' field
            if sort_by == 'class':
                sort_column = Song.class_field
            else:
                sort_column = getattr(Song, sort_by)
            
            # Apply sorting
            if order == 'desc':
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
            
            # Execute pagination
            pagination = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            # Build response
            response = {
                'status': 'success',
                'data': [song.to_dict() for song in pagination.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total_pages': pagination.pages,
                    'total_items': pagination.total,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
            
            return jsonify(response), 200
            
        except Exception as e:
            logger.error(f"Error getting songs: {str(e)}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    
    # ===========================================
    # 1.2.2 [MUST HAVE] Get song by title
    # ===========================================
    @app.route('/api/songs/search', methods=['GET'])
    def search_song_by_title():
        """
        Search for songs by title (exact match or partial match)
        
        Query Parameters:
            title (str): Song title to search for
            exact (bool): If true, exact match; if false, partial match (default: false)
        
        Returns:
            JSON response with matching songs
        """
        try:
            title = request.args.get('title', '', type=str)
            exact = request.args.get('exact', 'false', type=str).lower() == 'true'
            
            if not title:
                return jsonify({'status': 'error', 'message': 'Title parameter is required'}), 400
            
            # Search for songs
            if exact:
                songs = Song.query.filter_by(title=title).all()
            else:
                songs = Song.query.filter(Song.title.ilike(f'%{title}%')).all()
            
            if not songs:
                return jsonify({
                    'status': 'success',
                    'message': 'No songs found',
                    'data': []
                }), 200
            
            return jsonify({
                'status': 'success',
                'data': [song.to_dict() for song in songs],
                'count': len(songs)
            }), 200
            
        except Exception as e:
            logger.error(f"Error searching songs: {str(e)}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    
    # ===========================================
    # Get song by ID
    # ===========================================
    @app.route('/api/songs/<song_id>', methods=['GET'])
    def get_song_by_id(song_id):
        """
        Get a specific song by its ID
        
        Args:
            song_id (str): Song ID
        
        Returns:
            JSON response with song data
        """
        try:
            song = Song.query.filter_by(id=song_id).first()
            
            if not song:
                return jsonify({
                    'status': 'error',
                    'message': f'Song with ID {song_id} not found'
                }), 404
            
            return jsonify({
                'status': 'success',
                'data': song.to_dict()
            }), 200
            
        except Exception as e:
            logger.error(f"Error getting song: {str(e)}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    
    # ===========================================
    # 1.2.3 [NICE TO HAVE] Update song rating
    # ===========================================
    @app.route('/api/songs/<song_id>/rating', methods=['PUT'])
    def update_song_rating(song_id):
        """
        Update the star rating for a song
        
        Args:
            song_id (str): Song ID
        
        Request Body:
            {
                "rating": 5  // Integer between 0 and 5
            }
        
        Returns:
            JSON response with updated song data
        """
        try:
            # Get request data
            data = request.get_json()
            
            if not data or 'rating' not in data:
                return jsonify({
                    'status': 'error',
                    'message': 'Rating is required in request body'
                }), 400
            
            rating = data['rating']
            
            # Validate rating
            try:
                Song.validate_rating(rating)
            except ValueError as e:
                return jsonify({'status': 'error', 'message': str(e)}), 400
            
            # Find song
            song = Song.query.filter_by(id=song_id).first()
            
            if not song:
                return jsonify({
                    'status': 'error',
                    'message': f'Song with ID {song_id} not found'
                }), 404
            
            # Update rating
            song.star_rating = rating
            db.session.commit()
            
            logger.info(f"Updated rating for song {song_id} to {rating}")
            
            return jsonify({
                'status': 'success',
                'message': 'Rating updated successfully',
                'data': song.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating rating: {str(e)}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    
    # ===========================================
    # Upload JSON data
    # ===========================================
    @app.route('/api/songs/upload', methods=['POST'])
    def upload_json_data():
        """
        Upload and process JSON song data
        
        Request Body:
            JSON data in the specified format
        
        Returns:
            JSON response with upload status
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'status': 'error',
                    'message': 'No JSON data provided'
                }), 400
            
            # Normalize data
            normalized_data = DataProcessor.normalize_json(data)
            
            # Load to database
            inserted_count = DataProcessor.load_data_to_db(normalized_data)
            
            return jsonify({
                'status': 'success',
                'message': f'Successfully uploaded {inserted_count} songs',
                'inserted_count': inserted_count
            }), 201
            
        except ValueError as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        except Exception as e:
            logger.error(f"Error uploading data: {str(e)}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    
    # ===========================================
    # Get statistics
    # ===========================================
    @app.route('/api/stats', methods=['GET'])
    def get_stats():
        """
        Get database statistics
        
        Returns:
            JSON response with statistics
        """
        try:
            total_songs = Song.query.count()
            
            # Average stats
            stats = db.session.query(
                func.avg(Song.danceability).label('avg_danceability'),
                func.avg(Song.energy).label('avg_energy'),
                func.avg(Song.tempo).label('avg_tempo'),
                func.avg(Song.duration_ms).label('avg_duration_ms'),
                func.min(Song.duration_ms).label('min_duration_ms'),
                func.max(Song.duration_ms).label('max_duration_ms')
            ).first()
            
            # Rating distribution
            rating_dist = db.session.query(
                Song.star_rating,
                func.count(Song.star_rating)
            ).group_by(Song.star_rating).all()
            
            return jsonify({
                'status': 'success',
                'data': {
                    'total_songs': total_songs,
                    'average_danceability': float(stats.avg_danceability) if stats.avg_danceability else 0,
                    'average_energy': float(stats.avg_energy) if stats.avg_energy else 0,
                    'average_tempo': float(stats.avg_tempo) if stats.avg_tempo else 0,
                    'average_duration_ms': float(stats.avg_duration_ms) if stats.avg_duration_ms else 0,
                    'min_duration_ms': stats.min_duration_ms,
                    'max_duration_ms': stats.max_duration_ms,
                    'rating_distribution': {
                        str(rating): count for rating, count in rating_dist
                    }
                }
            }), 200
            
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'status': 'error', 'message': 'Method not allowed'}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500


# Run application
if __name__ == '__main__':
    print("Starting Flask application...")
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    print(f"App created. Debug mode: {app.config['DEBUG']}")
    print("Starting server on http://0.0.0.0:5000")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True  # Force debug mode
    )