```markdown
# Backend: Умный подбор способа подписания документов

## Установка и запуск

### 1. Подготовка
1. Убедитесь, что установлен Python 3.8+:
   ```bash
   python --version
   ```
2. Убедитесь, что PostgreSQL установлен. Если нет, выполните следующие шаги.

### 2. Установка PostgreSQL (Linux)
1. Установите PostgreSQL и сопутствующие пакеты:
   ```bash
   sudo apt install postgresql postgresql-contrib
   ```

2. Убедитесь, что служба PostgreSQL запущена:
   ```bash
   sudo systemctl status postgresql
   ```

3. Переключитесь на пользователя `postgres`:
   ```bash
   sudo -i -u postgres
   ```

4. Запустите `psql`:
   ```bash
   psql
   ```

5. Установите пароль для пользователя `postgres`:
   ```sql
   ALTER USER postgres PASSWORD 'yourpassword';
   ```
   Замените `'yourpassword'` на желаемый пароль.

6. Создайте базу данных с русской кодировкой:
   ```sql
   CREATE DATABASE signing_db
       WITH OWNER = postgres
       ENCODING = 'UTF8';
   ```

7. Проверьте, что база данных создана:
   ```sql
   \l
   ```

8. Выйдите из `psql`:
   ```sql
   \q
   exit
   ```

### 3. Настройка
1. Перейдите в директорию с бэкендом:
   ```bash
   cd backend
   ```
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Настройте подключение к базе данных. В файле `backend/database.py` замените строку:
   ```python
   SQLALCHEMY_DATABASE_URL = "postgresql://postgres:yourpassword@localhost/signing_db"
   ```
   Укажите пароль, установленный на шаге 5.

### 4. Инициализация базы данных
1. Инициализируйте базу данных и создайте тестового пользователя:
   ```bash
   python init_db.py
   ```

### 5. Запуск сервера
1. Запустите сервер:
   ```bash
   uvicorn main:app --reload
   ```
2. Backend будет доступен по адресу: [http://localhost:8000](http://localhost:8000).

## Примечания

### Тестовые данные
После инициализации базы данных создается тестовый пользователь:
- `client_id`: `test_client`
- Текущий метод подписи: `SMS`
- Доступные методы: `["SMS", "PayControl", "КЭП на токене", "КЭП в приложении"]`.

### Swagger UI
Для тестирования API откройте [http://localhost:8000/docs](http://localhost:8000/docs).
```