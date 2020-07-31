from django import forms
from django.contrib.admin.widgets import AdminDateWidget

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
            'video_type': forms.HiddenInput(),
            'file_quality': forms.Select(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'intro_start': forms.NumberInput(attrs={'class': 'form-control'}),
            'intro_end': forms.NumberInput(attrs={'class': 'form-control'}),
            'credits_start': forms.NumberInput(attrs={'class': 'form-control'}),
            'video_art': forms.FileInput(attrs={'class': 'form-control'}),
        }

    class Media:
        js = ['staff/js/videoUpload.js']


class StaffMovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        exclude = ('file',)
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'director': forms.TextInput(attrs={"class": "form-control"}),
            'writers': forms.TextInput(attrs={"class": "form-control"}),
            'genre': forms.TextInput(attrs={"class": "form-control"}),
            'cast': forms.Textarea(attrs={"class": "form-control"}),
            'rating': forms.NumberInput(attrs={"class": "form-control", 'max': 10, 'min': 0}),
            'date_of_release': AdminDateWidget(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={"class": "form-control"}),
            'art': forms.FileInput(attrs={"class": "form-control"}),
            'synopsis': forms.Textarea(attrs={"class": "form-control"}),
        }
