from django.db import models

from django.contrib.auth.models import User


# profile
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=200, blank=True, null=True)
    minor = models.BooleanField(default=False)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        count = Profile.objects.filter(user=self.user).count()
        if count <= 3:
            return super().save(args, kwargs)
        else:
            return

    def __str__(self):
        return self.profile_name
