# Xarala Academy - Online Learning Platform

## Vision

The aim of this project is to help anyone to learn new skills and create value easily.

We’re solving the quality of education by building a simple and easy to use solution.

## Language

The development language is English. All comments and documentation should be written in English so that we don't end up with “franglais” methods, and so we can share our learnings with developers around the world.

However, the domain language is French. We consider each tax, collecting organism, and French regulation as a domain-specific term. In the same fashion, well-known abbreviations of these domain-specific terms are accepted.

## Installation

We’re using these technologies:

- Python/Django
- GraphQL/Graphene
- Html/CSS/Javascript/
- Bootstrap 4.x
- JQuery

In order to run the application, you should have *Python-3.8 or higher* installed in your system.

In order to run the application you should have *Python-3.8 or higher* installed in your system.

We use **Pipenv** as a dependency manager, you can install it [here](https://pipenv.pypa.io/en/latest/install/).

*Note: All members of the team should use it.
Once installed, you have to run these commands to setup the project:

```shell
pipenv install
cp src/xarala/local_settings.example src/xarala/local_settings.py
```

## Run the application

Make sur to change the database information on ```local_settings.py```

```bash
python src/manage.py migrate
python src/manage.py runserver
```

Enjoy!

### Discussing strategies

We’re trying to develop this project in the open as much as possible.

## Versioning

Version numbering follows the [Semantic versioning](http://semver.org/) approach.

## License

All rights reserved © [xarala](https://www.xarala.co)