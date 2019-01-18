from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer
from .models import Profile


# create user view
class UserCreate(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = ()
    authentication_classes = ()


# login view
class LoginAPI(APIView):
    permission_classes = ()

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(
            username=username,
            password=password
        )

        if user:
            # if a token does not exist yet!!
            try:
                token = user.auth_token.key
            except ObjectDoesNotExist:
                Token.objects.create(user=user)
                token = user.auth_token.key

            return Response({
                'success': True,
                'token': token,
                'username': user.username,
                'email': user.email
            })
        else:
            return Response({
                'success': False,
                'error': 'Wrong username or password'
            })


# getting a profile
class ProfileFetch(APIView):
    def get(self, request, profile_id):
        if request.user.is_authenticated:
            profile = get_object_or_404(Profile, pk=profile_id)
            data = {
                'user': profile.user.username,
                'profile': profile.profile_name,
                'minor': profile.minor
            }
            return Response(data)


# creating a profile
class ProfileCreate(APIView):
    def post(self, request):
        count = request.user.profile_set.all().count()

        if count >= 4:
            response = {'detail': 'Cannot make more profiles'}
        else:
            name = request.data.get('name')
            minor = request.data.get('minor')
            profile = Profile(
                profile_name=name,
                minor=minor,
                user=request.user
            )
            profile.save()
            response = {
                'detail': 'Create successfully',
                'name': name,
            }

        return Response(response)
