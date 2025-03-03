Docker Image for Personal Assistant Project
-------------------------------------------

I. Description
==============
This guide will walk you through setting up the Docker environment for the Personal Assistant web application. 
It will use Docker to run PostgreSQL as the database for the application.


II. Setup Steps
===============
1) Install Docker Desktop: Download and install Docker Desktop from here: https://www.docker.com/ 

2) Open an Empty Directory: Create or open a directory where you want to store your project files. Make sure the directory name is in English.

3) Open Command Line: Open your preferred command line tool in this empty directory.

4) Download .env and docker-compose.yml:

    Depending on your operating system, use the following commands to download the necessary files:

    4a. For Windows PowerShell:
   
        ```
        # Download .env file
        Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Yuliia-Vogel/Python-WEB_team-project2/refs/heads/main/docker_make_container/.env.example" -OutFile ".env"
        ```
   
        ```
        # Download docker-compose.yml file
        Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Yuliia-Vogel/Python-WEB_team-project2/refs/heads/main/docker_make_container/docker-compose.yml" -OutFile "docker-compose.yml"
        ```
   
    4b. For Git Bash, WSL, or Linux/macOS:
   
        ```
        # Download .env file
        curl -o .env https://raw.githubusercontent.com/Yuliia-Vogel/Python-WEB_team-project2/refs/heads/main/docker_make_container/.env.example
        ```
   
        ```
        # Download docker-compose.yml file
        curl -o docker-compose.yml https://raw.githubusercontent.com/Yuliia-Vogel/Python-WEB_team-project2/refs/heads/main/docker_make_container/docker-compose.yml
        ```
   
    4c. Alternatively, using wget:
   
        ```
        # Download .env file
        wget -O .env https://raw.githubusercontent.com/Yuliia-Vogel/Python-WEB_team-project2/refs/heads/main/docker_make_container/.env.example
        ```
   
        ```
        # Download docker-compose.yml file
        wget -O docker-compose.yml https://raw.githubusercontent.com/Yuliia-Vogel/Python-WEB_team-project2/refs/heads/main/docker_make_container/docker-compose.yml
        ```
   
6) Edit the .env file: Open the .env file and adjust the values based on your desired configuration (e.g., database settings, Cloudinary credentials, - follow the instructions inside the generated .env file).

7) Pull the Docker Image and Start the Container: Run the following commands to pull the image and start the container:
    ```
    docker pull kyrylodolia/personal_assistant:latest
    docker-compose up
    ```
8) Access the Application: Once the container is running, you can access the Personal Assistant application by navigating to http://localhost:8000/ in your web browser.


III. System Requirements
========================
    * Docker Desktop (download and install here).
    * Command line tool (PowerShell, Git Bash, WSL, or terminal for Linux/macOS).
    * An internet connection to download necessary configuration files.
