from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=225)

    def __str__(self):
        return f'{self.category}'

    class Meta:
        verbose_name = 'Categoery'
        verbose_name_plural = 'Categories'


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=225)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    imgurl = models.URLField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    price = models.FloatField()
    on_watch_list = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.FloatField()

    def __str__(self):
        return f'{self.listing}: {self.bid} bids'

    class Meta:
        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField(max_length=255)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}:  comments'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Watchlist(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     listing = models.ForeignKey(Listing,on_delete=models.CASCADE,blank=True)
     

     def __str__(self):
        return f'{self.user}: whichList'

     class Meta:
        verbose_name = 'WatchList'
        verbose_name_plural = 'WatchLists'