from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import reverse, redirect
from django.views import View, generic


from .forms import StaffMovieForm, StaffVideoForm
from watch.models import Movie


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
        movie_form = StaffMovieForm(request.POST)

        if movie_form.is_valid():
            movie_form.save()

        else:
            return render(request, self.template_name, {
                'movie': movie,
                'movie_form': movie_form,
                'video_form': StaffVideoForm(instance=movie.file, for_movie=True)
            })

        return redirect(reverse('staff:movie-detail'))


@csrf_exempt
@permission_required('watch.can_add_video')
def upload_video(request):
    if request.method == 'POST' and request.is_ajax():
        form = StaffVideoForm(request.POST, request.FILES)

        if form.is_valid():
            # video_pk = form.save()
            video_pk = 230239
            response = {
                'success': True,
                'video_id': video_pk,
                's': str(request.user)
            }
        else:
            response = {
                'success': False,
                'error': form.errors
            }

        return JsonResponse(response)

    else:
        return HttpResponseBadRequest('Not allowed')
