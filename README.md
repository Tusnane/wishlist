# ✨ Вишлист по неделям (Django)

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
| 1. Архитектор ядра | [`task_1_architect/architecture_core.md`](task_1_architect/architecture_core.md), [UML](task_1_architect/uml_class_diagram.md) |
| 2. Разработчик интерфейса | [`task_2_frontend/ui_integration.md`](task_2_frontend/ui_integration.md) |
| 3. Безопасность и валидация | [`task_3_security/security_validation.md`](task_3_security/security_validation.md) |
| 4. QA и тестирование | [`task_4_qa/qa_test_plan.md`](task_4_qa/qa_test_plan.md) |
| 5. Технический писатель и DevOps | [`task_5_devops/devops_documentation.md`](task_5_devops/devops_documentation.md) |

В каждой папке `task_*` файл `README.md` совпадает с основным документом роли (GitHub показывает его при открытии папки).

## Структура
```
wishlist_django/   код (config, wishes, templates)
docs/              руководство по запуску и деплою
task_*/            документы по ролям
.github/workflows/ автотесты (CI)
```
