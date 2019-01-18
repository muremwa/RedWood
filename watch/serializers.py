from rest_framework.serializers import ModelSerializer

from .models import Movie, Series, Season, Episode
from django.contrib.auth.models import User


# serializer for movies
class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        exclude = ('voters_of_rating',)


# serializer for Series
class SeriesSerializer(ModelSerializer):
    class Meta:
        model = Series
        fields = (
            'id', 'title', 'cast', 'synopsis', 'rating', 'date_of_release', 'genre', 'country', 'running_time',
            'number_of_seasons', 'art'
        )


# serializer for season
class SeasonSerializer(ModelSerializer):

    class Meta:
        model = Season
        fields = '__all__'


# episode serializer
class EpisodeSerializer(ModelSerializer):

    class Meta:
        model = Episode
        fields = '__all__'


# user serializer
class UserSerializer(ModelSerializer):
    pass
