# FastAPI template

## Description
This is a template for a FastAPI project. It includes:
- A basic FastAPI app
- A basic Dockerfile
- A basic docker-compose file

## Create a virtual environment & install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to run the app

### Run the app locally with a local database
```bash
if you want to run the app locally with a local database the .env file should look like this:
```bash
POSTGRES_PASSWORD=root
POSTGRES_USER=root
POSTGRES_DB=postgres
DATABASE_URI_LOCAL=postgresql://root:root@db:5432/postgres
```
Where db in DATABASE_URI_LOCAL is the name of the database service in the docker-compose file.
#### Access postgres from the terminal
```bash
psql -U root -d postgres
```
#### Access postgres from dbeaver

if you want to access from dbeaver follow the next steps:
- Get the ip of the container
```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' abc123
```
where abc123 is the id of the container

- Create a new connection in dbeaver
- Select PostgreSQL
- Host: the ip of the container
- Port: 5432
- Database: postgres
- Username: root
- Password: root
