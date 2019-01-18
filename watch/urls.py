from django.urls import path

from . import views

app_name = 'watch'

urlpatterns = [
    # watch/
    path('', views.Index.as_view(), name='home'),

    # watch/movies/
    path('movies/', views.AllMovies.as_view(), name='movies'),

    # watch/movies/34/
    path('movies/<int:movie_id>/', views.EachMovie.as_view(), name='movie'),

    # watch/series/
    path('series/', views.AllTvSeries.as_view(), name='series'),

    # watch/series/34/
    path('series/<int:series_id>/', views.EachSeries.as_view(), name='this_series'),
]
