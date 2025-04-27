# Learning Application

A web application for learning vocabulary and taking tests.

## Features

- User authentication (register, login)
- Topic management (create, read, update, delete)
- Vocabulary management (create, read, update, delete)
- Test management (create, read, update, delete)
- Test taking and result tracking
- Leaderboard system
- Statistics and analytics

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd learning-app
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```
Edit `.env` file with your configuration.

5. Initialize database:
```bash
flask db init
flask db migrate
flask db upgrade
```

6. Run the application:
```bash
flask run
```

## API Documentation

### Authentication

- `POST /api/register`: Register a new user
- `POST /api/login`: Login user

### Topics

- `GET /api/topics`: Get all topics
- `POST /api/topics`: Create a new topic
- `GET /api/topics/<topic_id>`: Get topic details
- `PUT /api/topics/<topic_id>`: Update topic
- `DELETE /api/topics/<topic_id>`: Delete topic

### Vocabulary

- `GET /api/topics/<topic_id>/vocabularies`: Get all vocabularies in a topic
- `POST /api/vocabularies`: Create a new vocabulary
- `GET /api/vocabularies/<vocabulary_id>`: Get vocabulary details
- `PUT /api/vocabularies/<vocabulary_id>`: Update vocabulary
- `DELETE /api/vocabularies/<vocabulary_id>`: Delete vocabulary

### Tests

- `GET /api/topics/<topic_id>/tests`: Get all tests in a topic
- `POST /api/tests`: Create a new test
- `GET /api/tests/<test_id>`: Get test details
- `PUT /api/tests/<test_id>`: Update test
- `DELETE /api/tests/<test_id>`: Delete test
- `POST /api/tests/submit`: Submit test results

### Test Results

- `GET /api/user/results`: Get user's test results
- `GET /api/topics/<topic_id>/results`: Get topic's test results
- `GET /api/user/topics/<topic_id>/results`: Get user's results in a topic

### Leaderboard

- `GET /api/topics/<topic_id>/leaderboard`: Get topic leaderboard
- `GET /api/user/rank/<topic_id>`: Get user's rank in topic
- `GET /api/topics/<topic_id>/top-users`: Get top users in topic

### Statistics

- `GET /api/user/statistics`: Get user statistics
- `GET /api/topics/<topic_id>/statistics`: Get topic statistics

## Development

### Running Tests

```bash
pytest
```

### Code Style

```bash
black .
flake8
mypy .
```

## License

MIT 