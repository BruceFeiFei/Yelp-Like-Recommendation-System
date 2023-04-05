from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    id = models.CharField(max_length=200, primary_key=True)
    profile_url = models.URLField(max_length=2000)
    image_url = models.URLField(max_length=2000, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):   # str(user) call __str__
        return self.name

    def rated_businesses(self):
        rated_businesses = self.business_set.all()
        return rated_businesses

    def content_based_recommended_businesses(self):
        # Get all businesses the user has rated
        rated_businesses = self.review_set.all().values_list('business', flat=True)

        # Get the cities of the rated businesses
        rated_business_cities = Business.objects.filter(pk__in=rated_businesses).values_list('city', flat=True)

        # Get all businesses in the same cities as the rated businesses
        recommended_businesses = Business.objects.filter(city__in=rated_business_cities).exclude(
            pk__in=rated_businesses)
        # for testing
        # recommended_businesses = Business.objects.filter(city__in=rated_business_cities)
        return recommended_businesses

    def collaborative_based_recommended_businesses(self):
        # Get all businesses the user has rated
        rated_businesses = self.review_set.all().values_list('business', flat=True)

        # Get all users who have rated the same businesses as the current user
        similar_users = User.objects.exclude(pk=self.pk).filter(
            review__business__in=rated_businesses
        ).distinct()

        # Get all businesses that similar users have rated
        similar_businesses = Business.objects.filter(review__user__in=similar_users)

        # Get the businesses that the current user has not rated
        recommended_businesses = similar_businesses.exclude(review__user=self)

        return recommended_businesses


class Business(models.Model):
    PRICE_RATINGS = [
        ("$",    "cheap"),
        ("$$",   "mild cheap"),
        ("$$$",  "expensive"),
        ("$$$$", "extremely expensive"),
    ]
    id = models.CharField(max_length=200, primary_key=True)
    alias = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    image_url = models.URLField(max_length=2000, null=True)
    is_closed = models.BooleanField()
    url = models.URLField(max_length=2000, null=True)
    review_count = models.IntegerField()
    rating = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    price = models.CharField(max_length=10, choices=PRICE_RATINGS)
    address1 = models.CharField(max_length=200, null=True)
    address2 = models.CharField(max_length=200, null=True)
    address3 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, default=None)
    zip_code = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200)
    users = models.ManyToManyField(to=User, blank=True, through='Review')

    def __str__(self):
        return self.name


class Review(models.Model):
    RATING_STARS = [
        (1, 'One Star'),
        (2, 'Two Star'),
        (3, 'Three Star'),
        (4, 'Four Star'),
        (5, 'Five Star'),
    ]
    id = models.CharField(max_length=200, primary_key=True)
    url = models.URLField(max_length=2000)
    text = models.TextField()
    rating = models.IntegerField(choices=RATING_STARS)
    time_created = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)\
        + " rates "\
        + str(self.business)\
        + " at "\
        + str(self.rating)\
        + " Star."



