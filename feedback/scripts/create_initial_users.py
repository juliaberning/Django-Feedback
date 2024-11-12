# Use this script to bulk upload users to the database.
# This script will create users and their profiles, and assign managers to each user.
# Make sure to fill the users_data list with your own data.
# The script assumes that the manager_username field is the username of the manager.
# If you have a different field, make sure to update the script accordingly.

from django.contrib.auth.models import User
from feedback.models import UserProfile

# Define the common password
common_password = "securepassword123"

# Define users and their information
users_data = [
    # {"username": "first_last", "first_name": "First", "last_name": "Last", "department": "DEPARTMENT", "manager_username": "MANAGER_USERNAME", "email": first.last@thenotcompany.com"},
]

# Step 1: Create all users without managers assigned
user_objects = {}
for user_data in users_data:
    # Create user and profile
    user = User.objects.create_user(
        username=user_data["username"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        email=user_data["email"],
        password=common_password,
    )
    user_profile = UserProfile.objects.create(
        user=user, department=user_data["department"]
    )
    user_objects[user_data["username"]] = user_profile

# Step 2: Assign managers
for user_data in users_data:
    manager_username = user_data.get("manager_username")
    if manager_username:
        user_objects[user_data["username"]].manager = user_objects[
            manager_username
        ].user
        user_objects[user_data["username"]].save()
