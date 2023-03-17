from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def rated_events(self):
        rated_events = self.event_set.all()
        return rated_events

    def content_based_recommended_events(self):
        # Get all events the user has rated
        rated_events = self.rating_set.all().values_list('event', flat=True)

        # Get the cities of the rated events
        rated_event_cities = Event.objects.filter(pk__in=rated_events).values_list('city', flat=True)

        # Get all events in the same cities as the rated events
        recommended_events = Event.objects.filter(city__in=rated_event_cities).exclude(pk__in=rated_events)

        return recommended_events

    def collaborative_based_recommended_events(self):
        # Get all events the user has rated
        rated_events = self.rating_set.all().values_list('event', flat=True)

        # Get all users who have rated the same events as the current user
        similar_users = User.objects.exclude(pk=self.pk).filter(
            rating__event__in=rated_events
        ).distinct()

        # Get all events that similar users have rated
        similar_events = Event.objects.filter(rating__user__in=similar_users)

        # Get the events that the current user has not rated
        recommended_events = similar_events.exclude(rating__user=self)

        return recommended_events


class Event(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(to=User, blank=True, through='Rating')
    city = models.CharField(max_length=200, default=None)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return str(self.user)\
        + " rates "\
        + str(self.event)\
        + " at "\
        + str(self.star)\
        + " Star."



