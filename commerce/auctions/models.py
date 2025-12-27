from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watchers")

class Listing(models.Model):
    def current_price(self):
        if self.bids.exists():
            highest = self.bids.order_by('-bid').first()
            return highest.bid
        else:
            return self.starting_bid
    name = models.CharField(max_length=64)
    description = models.TextField(blank=False)
    starting_bid = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    is_active = models.BooleanField(default=True)

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=7, decimal_places=2)

class Comment(models.Model):
    comment = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    time =models.DateTimeField(auto_now_add=True)
