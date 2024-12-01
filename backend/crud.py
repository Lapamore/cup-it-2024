from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User, UserSignature
from typing import List, Dict, Any, Optional
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user(db: Session, client_id: str):
    return db.query(User).filter(User.client_id == client_id).first()

def get_user_current_method(db: Session, client_id: str) -> Optional[str]:
    """Получить текущий метод подписания пользователя"""
    user = get_user(db, client_id)
    return user.current_method if user else None

def get_user_available_methods(db: Session, client_id: str) -> List[str]:
    """Получить список доступных методов подписания пользователя"""
    user = get_user(db, client_id)
    return user.available_methods if user else []

def update_user_current_method(db: Session, client_id: str, new_method: str) -> bool:
    """Обновить текущий метод подписания пользователя"""
    logger.info(f"Attempting to update method for user {client_id} to {new_method}")
    
    user = get_user(db, client_id)
    if not user:
        logger.error(f"User not found: {client_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Available methods for user: {user.available_methods}")
    if new_method not in user.available_methods:
        logger.error(f"Method {new_method} not in available methods: {user.available_methods}")
        raise HTTPException(
            status_code=400,
            detail=f"Selected method {new_method} is not in available methods: {user.available_methods}"
        )
    
    user.current_method = new_method
    db.commit()
    logger.info(f"Successfully updated method to {new_method} for user {client_id}")
    return True

def get_user_data(db: Session, client_id: str) -> Dict[str, Any]:
    """Получает все необходимые данные пользователя для ML модели"""
    user = db.query(User).filter(User.client_id == client_id).first()
    if not user:
        return None

    # Получаем статистику подписей
    signatures = db.query(UserSignature).filter(UserSignature.client_id == client_id).first()
    
    # Если нет записи о подписях, создаем пустую статистику
    if not signatures:
        signatures = UserSignature(
            client_id=client_id,
            common_mobile=0,
            common_web=0,
            special_mobile=0,
            special_web=0
        )
    
    return {
        "organizations": user.organizations,
        "mobile_app": user.mobile_app,
        "claims": user.claims,
        "segment": user.segment,
        "role": user.role,
        "current_method": user.current_method,
        "available_methods": user.available_methods,
        "signatures_common_mobile": signatures.common_mobile,
        "signatures_common_web": signatures.common_web,
        "signatures_special_mobile": signatures.special_mobile,
        "signatures_special_web": signatures.special_web
    }
