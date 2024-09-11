# Django Research Vocabs

[![Github Build](https://github.com/Geoluminate/django-research-vocabs/actions/workflows/build.yml/badge.svg)](https://github.com/Geoluminate/django-research-vocabs/actions/workflows/build.yml)
[![Github Docs](https://github.com/Geoluminate/django-research-vocabs/actions/workflows/docs.yml/badge.svg)](https://github.com/Geoluminate/django-research-vocabs/actions/workflows/docs.yml)
[![CodeCov](https://codecov.io/gh/Geoluminate/django-research-vocabs/branch/main/graph/badge.svg?token=0Q18CLIKZE)](https://codecov.io/gh/Geoluminate/django-research-vocabs)
![GitHub](https://img.shields.io/github/license/Geoluminate/django-research-vocabs)
![GitHub last commit](https://img.shields.io/github/last-commit/Geoluminate/django-research-vocabs)
![PyPI](https://img.shields.io/pypi/v/django-research-vocabs)

Streamline the handling of citable research vocabularies in your Django web applications.

Documentation
-------------

The full documentation is at https://Geoluminate.github.io/django-research-vocabs/

About
---------

Django Research Vocabs is designed to facilitate the management and organization of citable research_vocabs within your Django project by providing a set of tools and models that enable you to easily handle research_vocabs citations, references, and related metadata in your projects.

Features
-----------

- Link to remote or locally-stored RDF-based vocabularies and use them easily in your Django project

- Declaratively build your own standardized vocabulary and utilize it in your Django models

- Form fields that display vocabularies just like a standard ChoiceField

- Model fields that allow you to link to, and validate against, a set of vocabulary terms

- Abstract "Concept" model that allows you to store vocabulary terms directly in your database

- Abstract "ConceptTree" model that allows you to store hierarchical vocabularies in your database (requires django-treebeard)

- (Optional) GenericConcept model that allows you to store arbitrary terms in your database and establish standard Django relationships





- **Keywords Models**: The package offers pre-built Django models for research_vocabs references, authors, journals, and other relevant entities. These models allow developers to store and manage research_vocabs-related information in their applications' databases.

- **Integration**: Django Research Vocabs easily integrates with existing models in a Django project, enabling the association of research_vocabs references with other data objects, such as articles, blog posts, or research papers.

- **Efficient Querying**: Django Research Vocabs provides intuitive query methods that allow developers to retrieve research_vocabs references based on various criteria, such as author, title, journal, or publication year. This makes it easy to search and filter the research_vocabs database.

- **Citation Generation**: The package offers utilities to generate citations in various formats, such as APA, MLA, or Chicago style. This feature simplifies the process of programmatically generating citations for references within the Django application.

- **Admin Interface**: Django Research Vocabs includes an admin interface that allows authorized users to manage research_vocabs references conveniently. The interface provides CRUD (Create, Read, Update, Delete) operations for research_vocabs objects and ensures data integrity.

Quickstart
----------

Install Django Research Vocabs::

    pip install django-research-vocabs

Add it to your `INSTALLED_APPS`:


    INSTALLED_APPS = (
        ...
        'research_vocabs',
        ...
    )

Add Django Research Vocabs's URL patterns:

    urlpatterns = [
        ...
        path('', include("research_vocabs.urls")),
        ...
    ]


Running Tests
-------------

Does the code actually work?

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------
