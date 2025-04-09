# Late Show API

A Flask API for managing episodes, guests, and appearances on a late night talk show.

## Features

- CRUD operations for Episodes, Guests, and Appearances
- RESTful endpoints with JSON responses
- Input validation
- SQLite database with SQLAlchemy ORM

## API Endpoints

### Episodes
- `GET /api/episodes` - List all episodes
- `POST /api/episodes` - Create new episode
- `GET /api/episodes/<id>` - Get episode details

### Guests
- `GET /api/guests` - List all guests

### Appearances
- `POST /api/appearances` - Create new appearance

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Initialize database:
```bash
python seed.py
```
4. Run the development server:
```bash
flask run
```

## Usage Examples

### Create Appearance
```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "rating": 5,
  "episode_id": 100,
  "guest_id": 123
}' http://localhost:5000/api/appearances
```

Response:
```json
{
  "id": 1,
  "rating": 5,
  "guest_id": 123,
  "episode_id": 100,
  "episode": {
    "date": "1/12/99",
    "id": 100,
    "number": 100
  },
  "guest": {
    "id": 123,
    "name": "Sample Guest",
    "occupation": "Sample Occupation"
  }
}
```

## Requirements
- Python 3.x
- Flask
- Flask-SQLAlchemy
