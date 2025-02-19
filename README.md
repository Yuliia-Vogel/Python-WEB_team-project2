# Python-WEB_team-project2
The final team project for Python WEB at GO.IT school

Щоб в вас працювало треба:
-  стянути до себе, бажано через SSH
-  в корені проекту, де знаходиться pyproject.toml, в терміналі ввести poetry install. Має встановити всі залежності.
Не забудьте увійти в створене оточення - poetry shell.
Також треба додати це оточення в VSCode, щоб він бачив встановлені бібліотеки. З цим можу окремо допомогти якщо виникнуть проблеми.
-  створити .env файл в корені проекту з ось такими речами

SECRET_KEY= 

DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
secret_key в кожного унікальний в джанго, тому його треба в себе створити і вставити в .env, для цього в папці utils є скрипт, 
який виводить ключ в терміналі, просто вводимо це:
poetry run python src/utils/gen_secret_key.py
Копіюємо ключ і вставляємо в .env

DATABASE_NAME, це ім'я бази даних, яку ми маємо створити в Postgres у себе локально, який в нас має запускатися з Docker. 
Якщо зашити ім'я яке було в минулих проектах, то все перемішається.

-  виконуємо міграції з увімкненим докер контейнером py manage.py makemigrations

