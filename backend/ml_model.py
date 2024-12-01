import pandas as pd
from catboost import CatBoostClassifier
from typing import Dict, Any, Tuple

METHOD_MAP = {0: 'КЭП на токене', 1: 'КЭП в приложении', 2: 'SMS', 3: 'PayControl'}

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Подготовка признаков для модели"""
    
    df['is_available_cap_on_token'] = df['available_methods'].apply(lambda x: 1 if 'КЭП на токене' in x else 0)
    df['is_available_cap_in_phone'] = df['available_methods'].apply(lambda x: 1 if 'КЭП в приложении' in x else 0)
    df['is_available_sms'] = df['available_methods'].apply(lambda x: 1 if 'SMS' in x else 0)
    df['is_available_pay_control'] = df['available_methods'].apply(lambda x: 1 if 'PayControl' in x else 0)
    
    df = pd.get_dummies(df, columns=['segment', 'role', 'current_method'])
    
    required_columns = ['organizations',
        'mobileApp',
        'claims',
        'signatures_common_mobile',
        'signatures_common_web',
        'signatures_special_mobile',
        'signatures_special_web',
        'is_available_cap_on_token',
        'is_available_cap_in_phone',
        'is_available_sms',
        'is_available_pay_control',
        'segment_Крупный бизнес',
        'segment_Малый бизнес',
        'segment_Средний бизнес',
        'role_ЕИО',
        'role_Сотрудник',
        'currentMethod_PayControl',
        'currentMethod_SMS',
        'currentMethod_КЭП в приложении',
        'currentMethod_КЭП на токене'
    ]
    
    # Добавляем отсутствующие колонки
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0

    return df[required_columns]

def predict_model(user_data: Dict[str, Any]) -> Tuple[str, float]:
    """Предсказывает оптимальный метод подписания на основе данных пользователя"""
    try:
        df = pd.DataFrame([user_data])
        features = prepare_features(df)
        model = CatBoostClassifier()
        model.load_model('catboost_model.bin')
        
        prediction = model.predict(features)
        probabilities = model.predict_proba(features)
        
        recommended_method = METHOD_MAP[prediction[0].item()]
        confidence = max(probabilities[0])
        
        return recommended_method, float(confidence)

    except Exception as e:
        print(f"Ошибка предсказания: {str(e)}")
        return "SMS", 0.0
