from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Movie, Series, Episode
from .serializers import MovieSerializer, SeriesSerializer, SeasonSerializer, EpisodeSerializer


# index
class Index(APIView):
    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response({'detail': 'You must login first'})

        series = Series.objects.all()[:5]
        movies = Movie.objects.all()[:5]
        data = {
            'movies': MovieSerializer(movies, many=True).data,
            'series': SeriesSerializer(series, many=True).data
        }
        return Response(data)


# all movies
class AllMovies(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'You must login first'})
        else:
            return super().get(request, args, kwargs)


# all tv series
class AllTvSeries(ListAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'You must login first'})
        else:
            return super().get(request, args, kwargs)


# each movies
class EachMovie(APIView):
    @staticmethod
    def get(request, movie_id):
        if not request.user.is_authenticated:
            return Response({'detail': 'You must login first'})

        movie = get_object_or_404(Movie, pk=movie_id)
        data = MovieSerializer(movie).data
        return Response(data)


# each tv series
class EachSeries(APIView):
    def get(self, request, series_id):
        if not request.user.is_authenticated:
            return Response({'detail': 'You must login first'})

        series = get_object_or_404(Series, pk=series_id)
        data = self.get_data(series)
        return Response(data)

    def get_data(self, series):
        data = SeriesSerializer(series).data
        data['seasons'] = self.all_seasons(series)
        return data

    @staticmethod
    def all_seasons(series):
        seasons = series.season_set.all()
        all_seasons = SeasonSerializer(seasons, many=True).data

        for season in all_seasons:
            episodes = EpisodeSerializer(
                Episode.objects.filter(season=season['series']),
                many=True
            ).data
            season['episodes'] = episodes

        return all_seasons
