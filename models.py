from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)  # Added email field with unique constraint
    created_at = models.DateTimeField(auto_now_add=True)  # Added created_at timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Added updated_at timestamp
    # Other fields...

    def __str__(self):
        return self.email

# Other models...