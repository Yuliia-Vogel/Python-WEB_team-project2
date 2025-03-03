# Python-WEB_team-project Instruction
The final team project for Python WEB at GO.IT school

## Docker Instructions
For detailed instructions on using Docker, refer to [README.docker.md](README.docker.md).

I. App description
==================
    This web-based Personal Assistant application is designed to help you stay organized by providing the following features:
        * Creating and managing notes on any topic
        * Storing and managing contacts
        * Limited file storage for organizing and accessing your documents
        * A news feed covering sports, Ukrainian politics, currency exchange rates, and weather updates
    Access to all features requires registration to ensure the security and privacy of your data. 
    Each user can access only their own personal data, which remains unavailable to other users and unauthorized individuals.

II. App installation
====================
1) Open your VSCode or PyCharm and clone this repository.

2) Create database Postgres in Docker. 
    1. Open Docker desktop
    2. Open the Command Line and run the following command:
        ```
        docker run --name web_project_db -p 5432:5432 -e POSTGRES_PASSWORD=web_project_db_pass -d postgres
        ```
    3. If you use the command above as is, you can use the default credentials provided in the .env.example file (marked as #Default) when setting up your .env file.

    Important:

    If you already have PostgreSQL installed locally on your computer, you should change the external port to 5433 (or another free port) to avoid conflicts with your local PostgreSQL instance:
        ```
        docker run --name web_project_db -p 5433:5432 -e POSTGRES_PASSWORD=web_project_db_pass -d postgres
        ```
    If you choose to use custom credentials, make sure to save your database name and password, as they will be required in your .env file.

3)  Create and activate virtual environment (venv). 
    1. To create venv write the command in terminal of your VSCode:
        ```
        python -m venv venv
        ```
4) To activate venv:
    4a. For Windows write command in terminal:
        ```
        venv\Scripts\Activate
        ```
    4b. If you use cmd, write command:
        ```
        venv\Scripts\activate.bat
        ```
    4c. If you use poetry, write:
        ```
        poetry shell
        ```

5) Install poetry (if it’s not installed yet):
        ```
        pip install poetry
        ```

6) Install all dependencies for the application:
    ```
    poetry install
    ```

7) Create .env file 
    1. In the root folder, create a .env file. You can use the .env.example file as a reference.
    2. To generate a SECRET_KEY, run the following command:
        ```
        poetry run python src/utils/gen_secret_key.py
        ```
        This will generate a unique key. Add it as SECRET_KEY in your .env file.
    
    3. Cloudinary Configuration:
        You can use a preconfigured Cloudinary account by copying the credentials from the .env.example file (marked as #Default).
        These credentials allow the app to interact with Cloudinary but do not grant access to the Cloudinary account itself. This means that uploaded files are not visible on the Cloudinary platform, even to those who have these credentials, ensuring the security of user files.
        If you prefer to use your own Cloudinary account, register at Cloudinary, retrieve your credentials (CLOUD_NAME, API_KEY, and API_SECRET), and add them to your .env file.

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

12) If you forget your parrword, you can press the bottom "Forget password", and the link will be sent to your email. Please enter your email-box and follow this link to create your new password. Please follow the instruction via the link.

13) All the data will be saved in the PostgreSQL database inside the docker-container.

14) Uploaded files will be sorten into 6 categories (images, documents, videos, audio, archives and other) and saved in Cloudinery storage in the appropriate folder ("images", "documents", "videos", "audio", "archives" or "other"). You can upload your file into Personal Assistant, view it (if possible depending on its format), download it or delete it from the cloud storage and from current web-application.

15) Please keep in mind usage limits regarding files uploading:
    Maximum image file size - 10 MB
    Maximum video file size - 100 MB
    Maximum online image manipulation size - 100 MB
    Maximum raw file size - 10 MB
    Maximum image megapixels - 25 MP
    Maximum total number of megapixels in all frames - 50 MP
    --------------------------------------
    .exe and .bat file extensions are forbidden.
    --------------------------------------

16) If you need some info for demo, you can create 50 fake contacts and 50 fake notes using Faker package.
First, register at least one user, and then run the command:
    ```
    poetry run python src/utils/gen_fake_data.py
    ```

17) Finally, to stop the Personal Assistant, go to the terminal where server is running, and press Ctrl+C.
The server will be stopped. All your data (user account, your contacts, notes, tags and files will be saved.)


III. System Requirements
========================
    Operating System: Windows, macOS, or Linux
    Python Version: 3.11 or higher, but lower than 3.13
    Package Manager: Poetry
    Database: PostgreSQL (for creation in Docker)
    Additional Requirements: Docker (for running PostgreSQL in a container)


IV. Running Tests ()
====================
    To run all tests:
        ```
        python src/manage.py test
        ``` 
    --------------------------------
    To run tests for a specific app:
        ```
        python src/manage.py test files 
        ```
        (Replace "files" with the name of the required app: contacts, files, news, notes, users)
    -----------------------------
    To run a specific test class:
        ```
        python src/manage.py test files.tests.FileUploadTest
        ```
        (Replace "files" with the name of the required app: contacts, files, news, notes, users; 
        and replace "FileUploadTest" with the name of the required test class)
    ------------------------
    To run a specific test::
        ```
        python src/manage.py test files.tests.FileUploadTest.test_upload_file_success
        ```
        (Replace "files" with the name of the required app: contacts, files, news, notes, users; 
        and replace "FileUploadTest" with the name of the required test class,
        and replace "test_upload_file_success" with the name of the test)

