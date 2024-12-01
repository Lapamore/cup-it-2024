# Backend for Signing Service

This is a FastAPI backend service for managing user signing methods.

## Project Structure

```
backend/
├── database.py      # Database connection and session management
├── models.py        # SQLAlchemy models
├── schemas.py       # Pydantic schemas for request/response validation
├── crud.py         # Database operations
├── main.py         # FastAPI application and routes
└── requirements.txt # Project dependencies
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure database connection in `database.py`:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost:5432/signing_db"
```

3. Run the server:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Get Current Signing Method
```
GET /users/{client_id}/current-method
```

Response:
```json
{
    "current_method": "SMS"
}
```

### Update Current Signing Method
```
PUT /users/{client_id}/current-method
```

Request body:
```json
{
    "current_method": "SMS"
}
```

Response:
```json
{
    "message": "Current method updated successfully"
}
```

## Error Handling

The API includes validation for:
- User existence
- Available methods validation
- Request data validation
