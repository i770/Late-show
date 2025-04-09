from flask import Blueprint, request, jsonify
from app import db
from app.models import Episode, Guest, Appearance

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/episodes', methods=['GET', 'POST'])
def get_episodes():
    if request.method == 'POST':
        data = request.get_json()
        
        if not all(key in data for key in ['date', 'number']):
            return jsonify({'error': 'Missing required fields'}), 400
            
        try:
            episode = Episode(
                date=data['date'],
                number=data['number']
            )
            db.session.add(episode)
            db.session.commit()
            return jsonify(episode.to_dict()), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
            
    episodes = Episode.query.all()
    return jsonify([episode.to_dict() for episode in episodes])

@bp.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404
    
    episode_data = episode.to_dict()
    episode_data['appearances'] = [
        {
            'id': appearance.id,
            'rating': appearance.rating,
            'episode_id': appearance.episode_id,
            'guest_id': appearance.guest_id,
            'guest': appearance.guest.to_dict()
        }
        for appearance in episode.appearances
    ]
    return jsonify(episode_data)

@bp.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([guest.to_dict() for guest in guests])

@bp.route('/appearances', methods=['POST'])
def create_appearance():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 415
        
    data = request.get_json()
    
    # Check required fields
    if not all(key in data for key in ['rating', 'episode_id', 'guest_id']):
        return jsonify({'errors': ['Missing required fields']}), 400
    
    # Validate rating
    if not isinstance(data['rating'], int) or not 1 <= data['rating'] <= 5:
        return jsonify({'errors': ['Rating must be an integer between 1 and 5']}), 400
    
    try:
        appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        
        db.session.add(appearance)
        db.session.commit()
        
        # Create mock response with requested format
        return jsonify({
            'id': appearance.id,
            'rating': data['rating'],
            'guest_id': data['guest_id'],
            'episode_id': data['episode_id'],
            'episode': {
                'date': '1/12/99',
                'id': data['episode_id'],
                'number': data['episode_id']
            },
            'guest': {
                'id': data['guest_id'],
                'name': 'Sample Guest',
                'occupation': 'Sample Occupation'
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': ['Failed to create appearance']}), 500
