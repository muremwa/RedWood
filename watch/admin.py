from django.contrib import admin

from .models import Movie, Series, Season, Episode


# admin site for movies
class MovieModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Film details', {
                'fields': [
                    'title', 'director', 'writers', 'cast', 'synopsis', 'date_of_release', 'genre', 'country',
                ]
            }
        ),
    ]
    list_display = ['title', 'genre']


# inline for season
class SeasonInline(admin.StackedInline):
    model = Season
    extra = 1


# admin site for series
class SeriesModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Series Details', {
                'fields': [
                    'title', 'cast', 'synopsis', 'running_time', 'date_of_release', 'genre', 'country',
                    'number_of_seasons', 'art'
                ]
            }
        ),
    ]

    list_display = ['title', 'genre', 'country']
    inlines = (SeasonInline,)


# episodes
class EpisodeModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Episode Details', {
                'fields': ['season', 'name', 'episode_number']
            }
        ),
    ]


admin.site.register(Movie, MovieModelAdmin)
admin.site.register(Series, SeriesModelAdmin)
admin.site.register(Episode, EpisodeModelAdmin)
