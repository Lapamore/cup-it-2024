# Умный подбор способа подписания документов

## Установка и запуск (без Docker)

### 0. Подготовка системы

#### Установка Python
1. Скачайте и установите Python 3.8+ с [официального сайта](https://www.python.org/downloads/)
2. При установке обязательно поставьте галочку "Add Python to PATH"
3. Проверьте установку:
```bash
python --version
```

#### Установка Node.js
1. Скачайте и установите Node.js 18+ с [официального сайта](https://nodejs.org/)
2. Проверьте установку:
```bash
node --version
npm --version
```

#### Установка PostgreSQL
1. Скачайте и установите PostgreSQL 12+ с [официального сайта](https://www.postgresql.org/download/)
2. При установке:
   - Запомните или запишите пароль, который вы указываете для пользователя postgres
   - Оставьте стандартный порт 5432
   - Установите все предлагаемые компоненты

### 1. Настройка базы данных
1. Откройте pgAdmin (установился вместе с PostgreSQL)
2. Войдите, используя пароль, который вы задали при установке
3. Создайте базу данных:
   - Правый клик на "Databases" -> Create -> Database
   - Имя базы данных: `signature_db`
   - Нажмите Save

4. Откройте файл `backend/database.py` и измените строку подключения:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:ВАШ_ПАРОЛЬ@localhost/signature_db"
```
Замените "ВАШ_ПАРОЛЬ" на пароль, который вы указали при установке PostgreSQL.

### 2. Установка Frontend (Next.js)
```bash
# Переходим в директорию frontend
cd my-app

# Устанавливаем зависимости
npm install

# Запускаем в режиме разработки
npm run dev
```
Frontend будет доступен по адресу: http://localhost:3000

### 3. Установка Backend (FastAPI)
```bash
# Переходим в директорию backend
cd backend

# Создаем виртуальное окружение
python -m venv venv

# Активируем виртуальное окружение
# Для Windows:
venv\Scripts\activate
# Для Linux/Mac:
# source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Инициализируем базу данных и создаем тестового пользователя
python init_db.py

# Запускаем сервер
uvicorn main:app --reload
```
Backend будет доступен по адресу: http://localhost:8000
Swagger документация: http://localhost:8000/docs

### 4. Проверка работоспособности
1. Откройте в браузере http://localhost:3000
2. Проверьте, что фронтенд загрузился и отображается интерфейс
3. Откройте http://localhost:8000/docs
4. В Swagger UI попробуйте выполнить запрос GET `/users/test_client/current-method`
   - Если всё настроено правильно, вы получите текущий метод подписи для тестового пользователя

### Возможные проблемы и их решение

#### Ошибка подключения к базе данных
1. Проверьте, что PostgreSQL запущен
   - Windows: Службы (services.msc) -> PostgreSQL
   - Убедитесь, что служба запущена
2. Проверьте правильность пароля в database.py
3. Проверьте, что база данных signature_db создана

#### Ошибка "module not found"
1. Убедитесь, что вы активировали виртуальное окружение
2. Попробуйте переустановить зависимости:
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

#### Порты заняты
Если порты 3000 или 8000 заняты:
1. Для frontend - измените порт в package.json
2. Для backend - запустите на другом порту:
```bash
uvicorn main:app --reload --port 8001
```

### Тестовые данные
После инициализации базы данных создается тестовый пользователь:
- client_id: "test_client"
- Текущий метод подписи: "SMS"
- Доступные методы: ["SMS", "PayControl", "КЭП на токене", "КЭП в приложении"]
