from django.db import models


def remove_colon(name):
    return '-'.join(' '.join(str(name).split(':')).split(' '))


def upload_item_to(instance: 'Video', filename: str):
    simple_path = 'videos'

    if hasattr(instance, 'movie'):
        simple_path = f'movies/{remove_colon(str(instance.movie))}'

    elif hasattr(instance, 'episode'):
        _season: 'Season' = instance.episode.season
        _series: 'Series' = _season.series
        simple_path = f'series/{_series}/{_season}'

    return f'watch/{simple_path}/{filename}'


# video
class Video(models.Model):
    video_qualities = (
        ('144', '144p'),
        ('240', '240p'),
        ('360', '360p'),
        ('720', '720p'),
        ('1080', '1080p'),
    )
    video_types = (
        ('M', 'Movie'),
        ('S', 'Series'),
    )

    video_type = models.CharField(max_length=1, choices=video_types)
    file_quality = models.CharField(max_length=4, choices=video_qualities)
    length = models.IntegerField(help_text='enter in seconds', blank=True, null=True)
    intro_start = models.IntegerField(help_text='enter in seconds', blank=True, null=True)
    intro_end = models.IntegerField(help_text='Enter in seconds', blank=True, null=True)
    credits_start = models.IntegerField(help_text='Enter in seconds', blank=True, null=True)
    video_art = models.ImageField(upload_to='watch/art', blank=True, null=True)
    file = models.FileField(upload_to=upload_item_to, blank=True, null=True)
    objects = models.Manager()

    @property
    def owner(self):
        _owner = None
        if hasattr(self, 'movie'):
            _owner = self.movie
        elif hasattr(self, 'episode'):
            _owner = self.episode

        return _owner

    def __str__(self):
        return 'video'


# movie
class Movie(models.Model):
    title = models.CharField(max_length=100, help_text='Enter the title of the movie')
    director = models.CharField(max_length=400, blank=True, null=True)
    writers = models.CharField(max_length=400, blank=True, null=True)
    cast = models.CharField(max_length=1000, blank=True, null=True)
    synopsis = models.TextField(help_text='Enter a short description of the plot*')
    rating = models.IntegerField(blank=True, null=True, help_text='enter a rating between 1 and 10')
    voters_of_rating = models.IntegerField(blank=True, null=True)
    date_of_release = models.DateField()
    genre = models.CharField(max_length=100)
    country = models.CharField(max_length=100, help_text='enter the country of origin')
    art = models.ImageField(upload_to='watch/art/', blank=True, null=True, help_text='enter the movie poster')
    file = models.OneToOneField(Video, on_delete=models.CASCADE, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return '{}(movie)'.format(self.title)


# series
class Series(models.Model):
    title = models.CharField(max_length=100)
    cast = models.CharField(max_length=1000, blank=True, null=True)
    synopsis = models.TextField()
    rating = models.IntegerField(blank=True, null=True)
    voters_of_rating = models.IntegerField(blank=True, null=True)
    date_of_release = models.DateField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    running_time = models.IntegerField()
    number_of_seasons = models.IntegerField()
    art = models.ImageField(upload_to='watch/art/', blank=True, null=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Series'

    def __str__(self):
        return '{}(series)'.format(self.title)


# season of a Tv series
class Season(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    number_of_episodes = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    season_number = models.IntegerField()
    date = models.DateField()
    objects = models.Manager()

    def __str__(self):
        return 'Season {} of {}'.format(self.season_number, self.series)


# episode of a season
class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    episode_number = models.IntegerField()
    name = models.CharField(max_length=100)
    file = models.OneToOneField(Video, on_delete=models.CASCADE, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return 'Episode {} of {}'.format(self.episode_number, self.season)
