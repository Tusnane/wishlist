Веб-приложение: недели → дни → желания. Желания можно добавлять, отмечать выполненными и удалять. У каждого пользователя свои данные, вход по логину и паролю.

## Быстрый старт
```bash
cd wishlist_django
python -m venv venv && source venv/bin/activate     # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
export DEBUG=1                                      # Windows PowerShell: $env:DEBUG="1"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Откройте http://127.0.0.1:8000. Тесты: `python manage.py test -v 2`.
Подробная инструкция (локально и на сервере с доменом): [`docs/guide_wishlist.md`](docs/guide_wishlist.md).

## Документация по ролям
| Роль | Документ |
|---|---|
| 1. Архитектор ядра | Дрис Даниил
| 2. Разработчик интерфейса | Уклонский Анатолий
| 3. Безопасность и валидация | Гапонов Денис
| 4. QA и тестирование | Анпилогов Максим
| 5. Технический писатель и DevOps | Камков Никита

## Структура
```
wishlist_django/   код (config, wishes, templates)
docs/              руководство по запуску и деплою
task_*/            документы по ролям
.github/workflows/ автотесты (CI)
```
