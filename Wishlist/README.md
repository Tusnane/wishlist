# Вишлист на Django

Недели → дни → желания. Клик по желанию отмечает его выполненным, ✕ удаляет.
Данные у каждого пользователя свои, вход по логину и паролю.

## Локальный запуск
```bash
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
export DEBUG=1                                       # Windows: set DEBUG=1
python manage.py makemigrations wishes
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Открой http://127.0.0.1:8000 и войди созданным пользователем.

## Деплой на свой домен (VPS, Ubuntu)
Замени `wish.example.com` на свой домен (DNS A-запись должна указывать на сервер).

```bash
export SECRET_KEY="длинная-случайная-строка"
export ALLOWED_HOSTS="wish.example.com"
export CSRF_TRUSTED_ORIGINS="https://wish.example.com"
export DB_PATH="/var/lib/wishlist/db.sqlite3"        # папка должна существовать

python manage.py makemigrations wishes
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
gunicorn config.wsgi --bind 127.0.0.1:8000
```
(Переменные лучше вынести в systemd-юнит через `Environment=`, а gunicorn запускать как сервис.)

Nginx (`/etc/nginx/sites-available/wishlist`):
```nginx
server {
    server_name wish.example.com;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
HTTPS: `sudo certbot --nginx -d wish.example.com`.

Админка: `/admin/`. Новых пользователей можно создавать там же.

## Тесты
```bash
pip install -r requirements-dev.txt
export DEBUG=1                      # Windows PowerShell: $env:DEBUG="1"
python manage.py test -v 2          # встроенный раннер Django (unittest)
pytest                              # то же самое через pytest
python -m unittest wishes.test_pure # только быстрые тесты без Django и БД
```
Миграция `0001_initial` уже лежит в репозитории, `makemigrations` перед запуском не нужен.
