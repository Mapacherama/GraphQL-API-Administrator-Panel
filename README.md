# Django GraphQL API Administrator Panel

This is a Django implementation of the GraphQL API Administrator Panel. The purpose of this project is to provide an easy-to-use, intuitive interface for managing data through a GraphQL API.
## Features

* Easy to use interface for managing data through a GraphQL API
* Intuitive navigation and user experience
* Dynamic schema generation
* GraphQL Playground integration for testing queries and mutations

## Requirements

* Django
* Graphene-File-Upload
* Graphene

## Installation

1. Clone the repository: git clone https://github.com/Mapacherama/GraphQL-API-Administrator-Panel.git
2. Install the required packages: `pip install -r requirements.txt`
3. Configure your Django project to use the app:
* Add "graphql_api_admin" to your INSTALLED_APPS list in settings.py
* Include the app's URLs in your project's urls.py file:

        from django.urls import path, include

        urlpatterns = [
            ...
            path('admin/', include('graphql_api_admin.urls')),
            ...
        ]

4. Migrate the database: python manage.py migrate
5. Start the Django development server: `python manage.py runserver`

## Usage

6. Navigate to http://localhost:8000/admin/ in your browser
7. Login with the credentials for your Django admin user
8. Use the interface to manage your data through the GraphQL API

For more information, please refer to the [Django Admin website](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/)
