from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):    
    """
    Performs Serialisation for data of Movie db
    """
    class Meta:
        model = Movie
        fields = "__all__"