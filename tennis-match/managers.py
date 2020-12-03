from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        user = self.model(email=email, **extra_fields)
        user.username = email
        user.set_password(password.value())
        # extra_fields.setdefault('level', level)
        # extra_fields.setdefault('gender', gender)
        # extra_fields.setdefault('singles', singles)
        # extra_fields.setdefault('doubles', doubles)
        # extra_fields.setdefault('mixed_doubles', mixed_doubles)
        # extra_fields.setdefault('picture', picture)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('level', 3.0)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('gender', 'F')
        extra_fields.setdefault('singles', True)
        extra_fields.setdefault('doubles', True)
        extra_fields.setdefault('mixed_doubles', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)