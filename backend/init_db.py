from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Создаем все таблицы
models.Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    try:
        # Проверяем, существует ли уже тестовый пользователь
        test_user = db.query(models.User).filter(models.User.client_id == "test_client").first()
        if test_user is None:
            # Создаем тестового пользователя
            test_user = models.User(
                client_id="test_client",
                organization_id="test_org",
                segment="Малый бизнес",
                role="ЕИО",
                organizations=3,
                current_method="SMS",
                mobile_app=True,
                signatures={
                    "common": {
                        "mobile": 3,
                        "web": 10
                    },
                    "special": {
                        "mobile": 5,
                        "web": 6
                    }
                },
                available_methods=["SMS", "PayControl", "КЭП на токене", "КЭП в приложении"],
                claims=0
            )
            db.add(test_user)
            db.commit()
            print("Test user created successfully!")
        else:
            print("Test user already exists!")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()