from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    # account/create-user/
    path('create-user/', views.UserCreate.as_view(), name='create-user'),

    # login
    path('login/', views.LoginAPI.as_view(), name='login'),

    # create-profile/
    path('create-profile/', views.ProfileCreate.as_view(), name='create-profile'),

    # profile/
    path('profile/<int:profile_id>/', views.ProfileFetch.as_view(), name='profile'),
]
