# Django Feedback App

This Django feedback app allows users to evaluate each other.

## Setup Instructions

### 1. Create and Activate a Virtual Environment

First, create a virtual environment to keep dependencies isolated.

```bash
# Create a virtual environment
python -m venv venv
```
 Activate the virtual environment (use the appropriate command for your OS)

```bash
# On Windows
venv\Scripts\activate

# On macOS and Linux
source venv/bin/activate

```
### 2. Install dependencies
Install Django 


### 3. Run the server

```bash
python manage.py runserver
```

### 4. Create a superuser
To access the Django admin interface, you’ll need a superuser account. Create one by running:
```bash
python manage.py createsuperuser
```
Follow the prompts to set up a username, email, and password.

### 5. Make and apply migrations
Migrations are necessary to create and update database tables. Run the following commands to make and apply migrations when first running the app and after any change in the models: 
```bash
# Prepare migrations
python manage.py makemigrations

# Apply migrations to the database
python manage.py migrate
```
### 6. Optional: Running the Initial User Creation Script
To batch create initial users with their manager assignments, add user data to the create_initial_users.py script and establish an initial password for them. 
Then run:

```bash
python manage.py shell < feedback/scripts/create_initial_users.py
```
### 7. Optional: Generate a model diagram
To visualize the relationships between models, you can create a diagram using Django Extensions and Graphviz.

Install the necessary libraries:
```bash
pip install django-extensions
brew install graphviz
```
Generate the model diagram as a .dot file: 
```bash
python manage.py graph_models -a --dot -o feedback_models.dot
```

Convert the .dot file to a .png image:
```bash
dot -Tpng feedback_models.dot -o feedback_models.png
```

For further information on the graphs you can read the [the django-extensions documentation](https://django-extensions.readthedocs.io/en/latest/graph_models.html).