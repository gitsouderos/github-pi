# Github PI (Personal Investigator)
As our final project in _LLMs and societel consequences_ we Implemented a chat application aimed at making github repositories easier to find and understand.

## System Requirements
* [Docker and Docker Compose](https://www.docker.com/)
* GNU Make
* The database backup file can be downloaded [here](https://drive.google.com/file/d/1PQ9hRLftau4lqZJVjVWHx9Sto03Ccmr5/view)
* To develop the application it is recomended to use Poetry v1.8.3 or above.

## Starting the application from scratch
The system runs within Docker so as long as you have docker installed on your environment, you should be good to go. If you want to run outside of docker, install the technologies listed in the compose.yaml file and go from there.

1. [Download the database backup file](https://drive.google.com/file/d/1PQ9hRLftau4lqZJVjVWHx9Sto03Ccmr5/view)
2. Rename the database backup file to `data_db_FULL.sql` and move it to ./backups
3. Create your .env file based on the .env.example in the repo (for convenience `cp .env.example .env`)
    - Fill out the correct API keys with your info.
    - Note that the env variables already filled out work for docker but field marked with "<VALUE>" are sensitive to your credentials.
4. cd into the project root directory and run `make up`
5. Once all the services are up run `make restore-db`
6. Install the right embedding model in Ollama. This step is hacky, I'm sorry. 
    - exec into the ollama service with `docker exec -u root -it github-pi-ollama-1 /bin/bash`
    - install bge-m3 model to the container with `ollama pull bge-m3`
7. Navigate to [localhost:8501](http://localhost:8501/) and start interacting with the app ✅


## Troubleshooting:
* The app requires a lot of memory and disk space to run. If you get an error in docker saying "out of memory" or something like that you can clean your docker system using `docker system prune`. __WARNING this will clean out all the dangling images, containers and volumes not in use__.

* If you get file permission errors when running the .sh files (also called by `make restore-db` and `make backup-db`), try changing the permissions on the file with `chmod +x <file name>.sh`

* The Makefile contains convenience commands for the app. If you dont have make, just reference the file for the relevant commands
