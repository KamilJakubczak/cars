# Cars
A simple car api

# Link
https://wwww.itbs.dev

# Technology stack
- Django
- Docker
- Travis
- Nginx
- PostgreSQL
- Swagger


# Packages
- **flake8** - for PEP8 verification
- **drf-spectacular** - for automated api swagger documentation
- **coverage** - for checking test coverage
- **mock** - for mocking tests
- **psycopg2** - for working with PostgreSQL
- **requests** - for external http requests


# API Documentation
API documentation can be found on **/swagger**

https://www.itbs.dev/swagger

# How to handle application

## How to run for the application for the first time and reflect changes related with container
Go to directory with **docker-compose.yml** file then type
in terminal
```shell
docker-compouse up --build
docker-compose run app sh -c "migrate"
```

## How to run application 
Go to directory with **docker-compose.yml** file then type
in terminal
```sh
docker-compose up
```

## How to run commands in container
Type in terminal
```sh
docker-compose run app sh -c "python manage.py test -v2 && flake8"
```


