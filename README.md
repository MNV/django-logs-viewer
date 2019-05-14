# Logs Viewer API

Simple Django REST Framework application for retrieving and watching logs.

The API has three endpoints:

1. `count-by-types` - the aggregated data grouped by log level
2. `search-by-body` - searching by message body using full-text index
3. `search-by-field` - searching by JSON field

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

A step by step series of examples that tell you how to get a development environment running.

Build docker containers:
```
docker-compose build
```

Run them:

```
docker-compose up
```

## Running the tests

To run the tests use the following command:

```
docker-compose run app sh -c "python manage.py test"
```

### Code style

To run the code style tests use the following command:

```
docker-compose run app sh -c "python manage.py flake8"
```

## Built With

* [Django REST Framework](https://github.com/encode/django-rest-framework) - The web framework used
* [Docker](https://github.com/docker) - Container platform
* [Travis-CI](https://github.com/travis-ci/travis-ci) - Continuous integration platform

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
