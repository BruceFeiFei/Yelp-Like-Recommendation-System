from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=200)


class Event(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(to=User, blank=True, through='Rating')


class Rating(models.Model):
    RATING_STARS = [
        (1, 'One Star'),
        (2, 'Two Star'),
        (3, 'Three Star'),
        (4, 'Four Star'),
        (5, 'Five Star'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    star = models.IntegerField(choices=RATING_STARS)

