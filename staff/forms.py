from django import forms

from watch.models import Movie, Video


class StaffVideoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # if the video instance is none/does not exist, add initial data
        if kwargs.get('instance') is None:
            # if for_movie is present, type_video == 'M' else 'S'
            for_movie = kwargs.get('for_movie')
            if for_movie is not None:
                if for_movie:
                    v_type = 'M'
                else:
                    v_type = 'S'

                kwargs.update({
                    'initial': {
                        'video_type': v_type
                    }
                })

        if 'for_movie' in kwargs:
            kwargs.pop('for_movie')

        super().__init__(*args, **kwargs)

    class Meta:
        model = Video
        fields = '__all__'
        widgets = {
            'video_type': forms.HiddenInput()
        }

    class Media:
        js = ['videoUpload.js']

    def save(self, *args, **kwargs):
        res = None
        if hasattr(self, 'cleaned_data'):
            video = Video.objects.create(**self.cleaned_data)
            res = video.pk

        return res


class StaffMovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        exclude = ('file',)
