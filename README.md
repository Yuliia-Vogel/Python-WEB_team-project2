# Python-WEB_team-project2
The final team project for Python WEB at GO.IT school

1) Open your VSCode or PyCharm and clone this repository.

2) Create database Postgres in Docker. 
- open Docker desktop
- open Command line 
- and print command:
```
docker run --name your_db_name -p 5432:5432 -e POSTGRES_PASSWORD=your password_to_db -d postgres
```
Please save your DB name and your password, it will be necessary for the .env file.

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

5) Install poetry (if still not):
```
pip install poetry
```

6) Install all dependencies for the application:
```
poetry install
```

7) Create .env file in the root folder. As an example there is a .env.example file in root folder.
To have a secret_key, please run command:
```
poetry run python src/utils/gen_secret_key.py
```
You'll receive your unique key, please add it as SECRET_KEY in the .env file.

** You can use specially prepared Cloudinary account, please use credentials for Cloudinery which are in .env.example file (you need only clear the part "should_be_left_" and clear quotation marks).
** In order to use your own Cloudinary account, you can register on https://cloudinary.com/ 
Save your credentials (CLOUD_NAME, API_KEY and API_SECRET) and use it in the .env file.

8) Apply migration of data to database:
```
poetry run python src/manage.py migrate
```
9) Run the server:
```
python src/manage.py runserver
```
10) Follow the link http://127.0.0.1:8000/ and start the work with Personal Assistant in web-browser.

11) To use the Personal Assistant, the registration is needed.

12) If you forget your parrword, you can press the bottom "Forget password", and the link will appear in your terminal. Please follow this link to create your new password. Please follow the instruction via the link.

13) All the data will be saved in the PostgreSQL database inside the docker-container.

14) Uploaded files will be sorten into 6 categories (images, documents, videos, audio, archives and other) and saved in Cloudinery storage in one of the appropriate folder ("images", "documents", "videos", "audio", "archives", "other"). You can upload your file into Personal Assistant, view it (if possible depending on its format), download it or delete it from application.

15) Please keep in mind usage limits regarding files uploading:
Maximum image file size - 10 MB
Maximum video file size - 100 MB
Maximum online image manipulation size - 100 MB
Maximum raw file size - 10 MB
Maximum image megapixels - 25 MP
Maximum total number of megapixels in all frames - 50 MP
--------------------------------------
.exe file extension is forbidden.
--------------------------------------

16) If you need some info for demo, you can create 50 fake contacts and 50 fake notes using Faker package.
First, register at least one user, and then run the command:
```
poetry run python src/utils/gen_fake_data.py
```

17) Finally, to stop the Personal Assistant, go to the terminal where server is running, and press Ctrl+C.
The server will be stopped. However all your data (user account, your contacts, notes, tags and files will be saved.)






