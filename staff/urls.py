from django.urls import path

from . import views as staff_views


app_name = 'staff'


urlpatterns = [
    # movies/
    path('movies/', staff_views.MovieIndex.as_view(), name='movie-index'),

    # movies/23/
    path('movies/<int:pk>/', staff_views.MovieDetail.as_view(), name='movie-detail'),

    # upload/
    path('upload/', staff_views.upload_video, name='upload'),
]
