from django.db import models

from rest_framework.authentication import TokenAuthentication

class BearerTokenAuthentication(TokenAuthentication):
    """
    Overriding keyword to Bearer
    """
    keyword = 'Bearer'

