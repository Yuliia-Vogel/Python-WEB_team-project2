Docker-образ для проєкту Personal Assistant
-------------------------------------------

I. Опис проєкту
===============
Цей посібник допоможе вам налаштувати Docker-середовище для веб-застосунку Personal Assistant.
Docker буде використовуватися для запуску PostgreSQL як бази даних для застосунку.


II. Кроки для налаштувань
=========================
1) Завантажте та встановіть Docker Desktop за посиланням: https://www.docker.com/ 

2) Відкрийте порожню директорію: 
Створіть або відкрийте директорію, у якій ви хочете зберігати файли проєкту.
Переконайтеся, що назва директорії написана англійською мовою.

3) Відкрийте командний рядок:
Запустіть командний рядок у цій порожній директорії.

4) Завантажте файли .env та docker-compose.yml:

    Залежно від вашої операційної системи, використовуйте наведені нижче команди:

    4a. Для Windows PowerShell:
   
        ```
        # Завантажити файл .env
        Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Yuliia-Vogel/Python-WEB_team-project2/refs/heads/main/docker_make_container/.env.example" -OutFile ".env"
        ```
   
        ```
        # Завантажити файл docker-compose.yml
        Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Yuliia-Vogel/Python-WEB_team-project2/refs/heads/main/docker_make_container/docker-compose.yml" -OutFile "docker-compose.yml"
        ```
   
    4b. Для Git Bash, WSL або Linux/macOS:
   
        ```
        # Завантажити файл .env
        curl -o .env https://raw.githubusercontent.com/Yuliia-Vogel/Python-WEB_team-project2/refs/heads/main/docker_make_container/.env.example
        ```
   
        ```
        # Завантажити файл docker-compose.yml
        curl -o docker-compose.yml https://raw.githubusercontent.com/Yuliia-Vogel/Python-WEB_team-project2/refs/heads/main/docker_make_container/docker-compose.yml
        ```
   
    4c. Альтернативний варіант (wget):
   
        ```
        # Завантажити файл .env
        wget -O .env https://raw.githubusercontent.com/Yuliia-Vogel/Python-WEB_team-project2/refs/heads/main/docker_make_container/.env.example
        ```
   
        ```
        # Завантажити файл docker-compose.yml
        wget -O docker-compose.yml https://raw.githubusercontent.com/Yuliia-Vogel/Python-WEB_team-project2/refs/heads/main/docker_make_container/docker-compose.yml
        ```
   
6) Редагування файлу .env 
Відкрийте .env файл та налаштуйте значення відповідно до ваших потреб (наприклад, параметри бази даних, облікові дані Cloudinary).
Дотримуйтесь інструкцій, зазначених у файлі .env.example

7) Завантаження Docker-образу та запуск контейнера
Виконайте такі команди для завантаження образу та запуску контейнера:

    ```
    docker pull kyrylodolia/personal_assistant:latest
    docker-compose up
    ```
8) Доступ до застосунку
Після запуску контейнера відкрийте веб-браузер і перейдіть за посиланням: [/localhost:8000/](http://localhost:8000/)


III. Системні вимоги
====================
    * Docker Desktop (завантажити та встановити [тут](https://www.docker.com/))
    * Командний рядок (PowerShell, Git Bash, WSL або термінал для Linux/macOS)
    * Інтернет-з’єднання (для завантаження необхідних файлів конфігурації)


