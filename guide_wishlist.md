# 📘 Как запустить свой вишлист и выложить его в интернет

Руководство «для чайника»: каждый шаг расписан отдельно, после каждого написано, **что ты должен увидеть**. Если увидел не то — смотри раздел «Если что-то сломалось» в конце.

**Что у нас есть:** файл `wishlist_django.zip`. Внутри — готовый сайт на Django.

**План:**
1. Сначала запускаем сайт **на своём компьютере**, чтобы убедиться, что он работает.
2. Потом арендуем **сервер**, привязываем **домен** и выкладываем сайт в интернет.

> 💡 **Слово «терминал»** — это чёрное окно, куда ты вставляешь команды текстом. В Windows это программа **PowerShell** (нажми кнопку «Пуск», набери `PowerShell`, открой). На Mac — программа **Терминал**. Команду копируешь целиком, вставляешь в окно и нажимаешь **Enter**.

---

# ЧАСТЬ 1. Запускаем на своём компьютере

## Шаг 1. Установи Python
1. Открой сайт **python.org** → Downloads → скачай последнюю версию Python 3.
2. Запусти установщик. **ОЧЕНЬ ВАЖНО:** внизу первого окна поставь галочку **«Add python.exe to PATH»**, и только потом жми «Install Now».
3. Проверь. Открой терминал и введи:
```bash
python --version
```
✅ Должно написать что-то вроде `Python 3.12.4`. (На Mac, если не сработало, пиши `python3` вместо `python` во всех командах.)

## Шаг 2. Распакуй проект
1. Найди скачанный `wishlist_django.zip`.
2. Правой кнопкой → «Извлечь всё…» (на Mac — двойной клик).
3. Получится папка `wishlist_django`. Переложи её куда-нибудь удобно, например на Рабочий стол.

## Шаг 3. Открой терминал внутри папки
- **Windows:** открой папку `wishlist_django`, кликни в адресную строку сверху, набери `powershell` и нажми Enter.
- **Mac:** в Терминале набери `cd ` (с пробелом), перетащи папку `wishlist_django` в окно терминала и нажми Enter.

Проверь, что ты в нужном месте:
```bash
dir        # Windows
ls         # Mac
```
✅ Среди файлов должны быть `manage.py`, `requirements.txt`, `README.md`.

## Шаг 4. Создай «виртуальную комнату» для Python
Это отдельная коробочка, куда установятся нужные программы, не мешая остальным.

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```
Если появилась красная ошибка про «выполнение сценариев отключено», введи один раз:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
ответь `Y`, потом снова `venv\Scripts\Activate.ps1`.

**Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```
✅ В начале строки появится `(venv)`. Так и должно быть. Все дальнейшие команды делай при этом `(venv)`.

## Шаг 5. Установи нужное
```bash
pip install -r requirements.txt
```
✅ Побегут строчки про скачивание, в конце `Successfully installed Django...`.

## Шаг 6. Включи «режим разработки»
Это говорит сайту: «я дома, можно без строгой защиты».

**Windows PowerShell:**
```powershell
$env:DEBUG="1"
```
**Mac:**
```bash
export DEBUG=1
```
⚠️ Эту команду нужно повторять каждый раз, когда открываешь новое окно терминала.

## Шаг 7. Создай базу данных
```bash
python manage.py makemigrations wishes
python manage.py migrate
```
✅ Много строчек с `OK`. Появится файл `db.sqlite3` — это твоя «тетрадка» с желаниями.

## Шаг 8. Создай себе аккаунт
```bash
python manage.py createsuperuser
```
Он спросит:
- **Username** — придумай логин (например, `masha`), Enter.
- **Email** — можно пропустить, просто Enter.
- **Password** — введи пароль. **Пока ты печатаешь, символы НЕ показываются. Это нормально!** Введи, Enter, повтори ещё раз.
- Если пишет, что пароль слишком простой, и спрашивает `Bypass password validation? [y/N]`, лучше нажми `N` и придумай пароль посложнее.

## Шаг 9. Запусти сайт
```bash
python manage.py runserver
```
✅ Появится строчка `Starting development server at http://127.0.0.1:8000/`.

Открой браузер и перейди на адрес **http://127.0.0.1:8000**. Введи логин и пароль из шага 8.

🎉 **Ты увидел свой вишлист!** Попробуй: впиши желание в любой день и нажми «+», кликни по желанию (оно станет зачёркнутым), нажми ✕ (удалится), попробуй кнопки «Вперёд» и «Назад».

Остановить сайт: в терминале нажми **Ctrl + C**.

---

# ЧАСТЬ 2. Выкладываем в интернет на свой домен

## Как это вообще устроено (простыми словами)
- **Сервер** — это компьютер, который стоит в дата-центре и никогда не выключается. Мы арендуем такой за деньги (обычно несколько евро в месяц).
- **IP-адрес** — это «номер дома» сервера, например `203.0.113.10`.
- **Домен** — это красивое «имя» вместо номера, например `wish.example.com`.
- **DNS-запись** — это «записка в телефонной книге»: «имя wish.example.com живёт по номеру 203.0.113.10».
- **Nginx** — «швейцар» сервера: принимает гостей из интернета и передаёт их нашему сайту.
- **Gunicorn** — «рабочий», который запускает сам сайт.
- **HTTPS** (замочек в браузере) — шифрование, чтобы никто не подсмотрел твой пароль.

В примерах ниже замени:
- `wish.example.com` → **твой настоящий домен** (или поддомен),
- `203.0.113.10` → **IP-адрес твоего сервера**.

## Шаг 1. Арендуй сервер
1. Выбери любого хостинг-провайдера с **VPS** (например, Hetzner, DigitalOcean, Timeweb Cloud, Selectel — подойдёт любой).
2. Создай сервер: система **Ubuntu 24.04** (или 22.04), самый дешёвый тариф хватит (1 ГБ памяти достаточно).
3. При создании выбери вход по **паролю** (проще) или ключу. Провайдер покажет тебе **IP-адрес** и пароль пользователя `root`. Запиши их.

## Шаг 2. Привяжи домен к серверу (DNS)
1. Зайди туда, где ты купил домен (личный кабинет регистратора), найди раздел **«DNS»** или **«DNS-записи»**.
2. Добавь запись:
   - **Тип:** `A`
   - **Имя (Host):** `wish` (получится `wish.example.com`) — или `@`, если хочешь сам домен без приставки
   - **Значение (Value):** IP твоего сервера
3. Сохрани. Подождать придётся от пары минут до нескольких часов.

Проверка (в терминале на твоём компьютере):
```bash
ping wish.example.com
```
✅ Он должен показать **IP твоего сервера**. Если пока показывает другой или пишет ошибку — подожди и повтори позже. Дальше можно идти, не дожидаясь, но HTTPS (шаг 13) заработает только когда DNS обновится.

## Шаг 3. Подключись к серверу
В терминале на **своём** компьютере:
```bash
ssh root@203.0.113.10
```
- На вопрос `Are you sure you want to continue connecting?` напиши `yes` и Enter.
- Введи пароль от сервера (**символы тоже не показываются**).

✅ Строка в терминале изменится на что-то вроде `root@server:~#`. Теперь все команды выполняются **на сервере**.

## Шаг 4. Обнови сервер и поставь программы
```bash
apt update && apt upgrade -y
apt install -y python3-venv python3-pip nginx certbot python3-certbot-nginx unzip ufw
```
✅ Долго бегут строчки, в конце снова появляется `root@server:~#`. Если спросит про перезапуск служб — жми Enter.

## Шаг 5. Загрузи проект на сервер
Открой **второе** окно терминала **на своём компьютере** (первое с ssh не закрывай) и выполни (путь замени на свой):

**Windows PowerShell:**
```powershell
scp $HOME\Downloads\wishlist_django.zip root@203.0.113.10:/opt/
```
**Mac:**
```bash
scp ~/Downloads/wishlist_django.zip root@203.0.113.10:/opt/
```
Введи пароль сервера. ✅ Покажет `100%`.

Вернись в окно, где ты подключён к серверу:
```bash
cd /opt
unzip wishlist_django.zip
cd wishlist_django
```
✅ Команда `ls` покажет `manage.py`, `wishes`, `config` и другие файлы.

## Шаг 6. Установи Python-программы на сервере
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
✅ В начале строки появится `(venv)`.

## Шаг 7. Придумай секретный ключ
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```
Он напечатает длинную белиберду. **Скопируй её** (выдели мышкой). Это секретный ключ сайта, никому его не показывай.

## Шаг 8. Создай файл с настройками
```bash
nano /etc/wishlist.env
```
Откроется простой текстовый редактор. Вставь (правой кнопкой мыши), заменив значения на свои:
```
SECRET_KEY=сюда_вставь_ключ_из_шага_7
ALLOWED_HOSTS=wish.example.com
CSRF_TRUSTED_ORIGINS=https://wish.example.com
DB_PATH=/var/lib/wishlist/db.sqlite3
```
⚠️ Без пробелов вокруг `=` и без кавычек.

Сохрани: **Ctrl + O**, Enter. Выйди: **Ctrl + X**.

Создай папку для базы данных:
```bash
mkdir -p /var/lib/wishlist
```

## Шаг 9. Подготовь сайт
Сначала «загрузи» настройки в текущее окно:
```bash
set -a; source /etc/wishlist.env; set +a
```
Затем по очереди:
```bash
python manage.py makemigrations wishes
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```
Логин и пароль придумай **новые и надёжные** (это будет вход на настоящий сайт). Пароль снова не отображается при вводе.

Теперь отдай файлы «рабочему», под которым будет жить сайт:
```bash
chown -R www-data:www-data /opt/wishlist_django /var/lib/wishlist
```

## Шаг 10. Сделай так, чтобы сайт работал всегда
Создай файл службы:
```bash
nano /etc/systemd/system/wishlist.service
```
Вставь:
```ini
[Unit]
Description=Wishlist site
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/wishlist_django
EnvironmentFile=/etc/wishlist.env
ExecStart=/opt/wishlist_django/venv/bin/gunicorn config.wsgi --bind 127.0.0.1:8000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```
Сохрани (**Ctrl+O**, Enter, **Ctrl+X**) и запусти:
```bash
systemctl daemon-reload
systemctl enable --now wishlist
systemctl status wishlist
```
✅ Должна быть зелёная надпись **`active (running)`**. Чтобы выйти из просмотра статуса, нажми **q**.

## Шаг 11. Настрой «швейцара» (nginx)
```bash
nano /etc/nginx/sites-available/wishlist
```
Вставь:
```nginx
server {
    listen 80;
    server_name wish.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Сохрани и включи:
```bash
ln -s /etc/nginx/sites-available/wishlist /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
```
✅ После `nginx -t` должно быть `syntax is ok` и `test is successful`.

## Шаг 12. Включи защиту от чужих (файрвол)
⚠️ **Порядок важен**, иначе можно закрыть себе доступ к серверу:
```bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
```
На вопрос `Proceed with operation (y|n)?` ответь `y`.

## Шаг 13. Включи HTTPS (замочек)
```bash
certbot --nginx -d wish.example.com
```
- Введи свою почту (для уведомлений о продлении).
- Согласись с условиями (`Y`), от рассылки можно отказаться (`N`).
- Если спросит про перенаправление HTTP на HTTPS — выбери **redirect** (пункт 2).

✅ Надпись `Congratulations!`. Если ошибка — почти всегда DNS ещё не обновился: подожди 10–30 минут и повтори.

## Шаг 14. Проверь! 🎉
Открой в браузере **https://wish.example.com**. Должна открыться страница входа с замочком. Войди логином из шага 9 и наполняй желания.

Можно закрыть терминал: сайт работает сам, даже когда ты выключил компьютер.

---

# ЧАСТЬ 3. Что делать потом

**Как посмотреть, что происходит, если сайт капризничает:**
```bash
journalctl -u wishlist -n 50 --no-pager
```

**Как перезапустить сайт:**
```bash
systemctl restart wishlist
```

**Как обновить сайт после изменений:** загрузи новый zip (как в шаге 5), распакуй поверх, затем на сервере:
```bash
cd /opt/wishlist_django && source venv/bin/activate
set -a; source /etc/wishlist.env; set +a
python manage.py migrate
python manage.py collectstatic --noinput
chown -R www-data:www-data /opt/wishlist_django /var/lib/wishlist
systemctl restart wishlist
```

**Резервная копия желаний** (файл базы), скачай себе на компьютер (в терминале на своём компьютере):
```bash
scp root@203.0.113.10:/var/lib/wishlist/db.sqlite3 ./backup.sqlite3
```
Делай так время от времени.

**Добавить ещё одного человека:** зайди на `https://wish.example.com/admin/` под своим логином → «Пользователи» → «Добавить». Публичной регистрации нет, чужие зайти не смогут.

---

# 🆘 Если что-то сломалось

| Что видишь | Почему | Что делать |
|---|---|---|
| `python` не найден | Не поставилась галочка PATH | Переустанови Python с галочкой «Add to PATH» |
| Нет `(venv)` в строке | Комната не включена | Повтори команду активации (шаг 4 / шаг 6) |
| `Bad Request (400)` на сайте | Домен не указан в настройках | Проверь `ALLOWED_HOSTS` в `/etc/wishlist.env`, потом `systemctl restart wishlist` |
| `403 CSRF verification failed` при входе | Не указан адрес с https | В `CSRF_TRUSTED_ORIGINS` должно быть `https://твой-домен`, затем перезапуск |
| `502 Bad Gateway` | Сайт не запущен | `systemctl status wishlist`, потом смотри `journalctl` (см. выше) |
| Сайт без оформления в `/admin/` | Не собрана статика | Повтори `collectstatic`, `chown` и перезапуск |
| Браузер «не находит сайт» | DNS не обновился или не тот IP | Проверь запись `A` и `ping` (часть 2, шаг 2) |
| Сайт не открывается вообще, а DNS верный | Закрыт порт | `ufw status` — должны быть `Nginx Full` и `OpenSSH` |
| Certbot ругается | DNS не обновился | Подожди 10–30 минут, повтори шаг 13 |
| Забыл пароль | — | На сервере (с загруженными настройками): `python manage.py changepassword ТВОЙ_ЛОГИН` |

---

## Если сервер — не для тебя
Есть путь попроще: сервисы вроде **PythonAnywhere**, **Render** или **Railway**. Там не нужно настраивать nginx и файрвол, но свой домен обычно подключается через платный тариф. Если захочешь такой вариант, скажи, на какой сервис, и я распишу такую же подробную инструкцию именно под него.
