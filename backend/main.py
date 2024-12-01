from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import crud
import logging
from ml_model import predict_model
from database import SessionLocal, engine, Base
from pydantic import BaseModel
from schemas import MethodResponse, AvailableMethodsResponse, RecommendationResponse

class MethodRequest(BaseModel):
    method: str

class MethodResponse(BaseModel):
    method: str

class AvailableMethodsResponse(BaseModel):
    available_methods: List[str]

class RecommendationResponse(BaseModel):
    recommended_method: str
    confidence: float

app = FastAPI()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.put("/users/{client_id}/current-method")
def update_user_current_method(client_id: str, request: MethodRequest):
    try:
        db = SessionLocal()
        success = crud.update_user_current_method(db, client_id, request.method)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error updating method: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/users/{client_id}/current-method", response_model=MethodResponse)
def get_user_current_method(client_id: str):
    try:
        db = SessionLocal()
        current_method = crud.get_user_current_method(db, client_id)
        if current_method is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"method": current_method} 
    except Exception as e:
        logger.error(f"Error getting method: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/users/{client_id}/available-methods", response_model=AvailableMethodsResponse)
async def get_available_methods(client_id: str, db: Session = Depends(get_db)):
    logger.info(f"Received get available methods request for client {client_id}")
    methods = crud.get_user_available_methods(db, client_id)
    if not methods:
        raise HTTPException(status_code=404, detail="User not found")
    return {"available_methods": methods}

@app.post("/users/{client_id}/recommend-method", response_model=RecommendationResponse)
def recommend_method(client_id: str):
    try:
        db = SessionLocal()
        user_data = crud.get_user_data(db, client_id)
        if user_data is None:
            raise HTTPException(status_code=404, detail="User not found")
            
        recommended_method, confidence = predict_model(user_data)
        return {
            "recommended_method": recommended_method,
            "confidence": confidence
        }
    except Exception as e:
        logger.error(f"Error recommending method: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
