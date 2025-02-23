# Python-WEB_team-project2
The final team project for Python WEB at GO.IT school

1) Open your VSCode or PyCharm and clone this repository.

2) Create database Postgres in Docker. 
- open Docker desktop
- open Command line 
- and print command:
```
docker run --name web_progect_db -p 5432:5432 -e POSTGRES_PASSWORD=web_progect_db -d postgres
```

3)  Create and activate virtual environment (venv). 
- To create venv write the command in terminal of your VSCode:
```
python -m venv venv
```
- To activate venv write command in terminal (Windows):
```
venv\Scripts\Activate
```
- If you use cmd, write command:
```
venv\Scripts\activate.bat
```
- If you use poetry, write:
```
poetry shell
```

4) Install all dependencies for the application:
```
pip install poetry
poetry install
```

5) Create .env file in the root folder. As an example there is a .env.example file in root folder.
To have a secret_key, please run command:
```
poetry run python src/utils/gen_secret_key.py
```
You'll receive your unique key, please add it as SECRET_KEY in the .env file.

6) Apply migration of data to database:
```
poetry run python src/manage.py migrate
```
7) Run the server:
```
python src/manage.py runserver
```
8) Follow the link http://127.0.0.1:8000/ and start the work with Personal Assistant in web-browser.

All the data will be saved in the PostgreSQL database inside the docker-container.

9) If you need some info for demo, you can create 50 fake contacts and 50 fake notes using Faker package.
First, register at least one user, and then run the command:
```
poetry run python src/utils/gen_fake_data.py
```

Finally, to stop the server, go to terminal where server is running, and press Ctrl+C.
The server will be stopped.


Work with FILES.



