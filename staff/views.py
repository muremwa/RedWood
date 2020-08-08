from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.messages import add_message, constants as message_constants
from django.views import View, generic
from rest_framework.decorators import api_view


from .forms import StaffMovieForm, StaffVideoForm
from watch.models import Movie, Episode


class MovieIndex(PermissionRequiredMixin, generic.ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = 'staff/movie_index.html'
    permission_required = 'watch.can_view_movie'


class MovieDetail(PermissionRequiredMixin, View):
    permission_required = ('watch.can_edit_movie', 'watch.can_add_video', 'watch.can_edit_video')
    template_name = 'staff/movie_detail.html'

    def get(self, request, **kwargs):
        movie = get_object_or_404(Movie, pk=kwargs.get('pk'))
        movie_form = StaffMovieForm(instance=movie)
        video_form = StaffVideoForm(instance=movie.file, for_movie=True)

        return render(request, self.template_name, {
            'movie': movie,
            'movie_form': movie_form,
            'video_form': video_form
        })

    def post(self, request, **kwargs):
        movie = get_object_or_404(Movie, pk=kwargs.get('pk'))
        movie_form = StaffMovieForm(request.POST, instance=movie)

        if movie_form.is_valid():
            movie_form.save()

            add_message(request, message_constants.SUCCESS, 'Successfully changed %s' %movie.title)

            return render(request, self.template_name, {
                'movie': movie,
                'movie_form': movie_form,
                'video_form': StaffVideoForm(instance=movie.file, for_movie=True)
            })

        else:
            return render(request, self.template_name, {
                'not_valid': True,
                'movie': movie,
                'movie_form': movie_form,
                'video_form': StaffVideoForm(instance=movie.file, for_movie=True)
            })


@api_view(['OPTIONS', 'POST'])
@permission_required('watch.can_add_video')
def upload_video(request):
    if request.method == 'POST':
        owner_pk = request.POST.get('owner', None)
        owner = None
        if owner_pk:
            if request.POST.get('video_type') == 'M':
                owner = get_object_or_404(Movie, pk=owner_pk)
            elif request.POST.get('video_type') == 'S':
                owner = get_object_or_404(Episode, pk=owner_pk)

        form = StaffVideoForm(request.POST, request.FILES, instance=owner.file)

        if form.is_valid() and owner:
            video = form.save()

            response = {
                'success': True,
                'video_id': video.pk,
                'user': str(request.user),
                'owner': owner.title,
            }

        else:
            response = {
                'success': False,
                'error': form.errors
            }

        return JsonResponse(response)

    elif request.method == 'OPTIONS':
        form = StaffVideoForm()

        return JsonResponse({
            'fields': [f for f in form.fields] + ['owner']
        })

    else:
        return HttpResponseBadRequest('Not allowed for %s' % str(request.user))
