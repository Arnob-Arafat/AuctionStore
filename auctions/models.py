from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True,related_name="watcher")

class Comments(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    text = models.CharField(max_length=64)
    datetime = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey("Listing", blank=True, on_delete=models.SET_NULL, null=True,related_name="comments")

class Listing(models.Model):
    image = models.URLField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    bidding = models.DecimalField(max_digits=10,decimal_places=2)
    original = models.DecimalField(max_digits=10,decimal_places=2)
    bidcount = models.IntegerField()
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    category = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)
    currentbidder = models.ForeignKey(User, blank=True, on_delete=models.SET_NULL,null=True,related_name="biddingproducts")
    sold = models.BooleanField(default="False")
    owner = models.ForeignKey(User, blank=True,on_delete=models.SET_NULL,null=True, related_name="owned")

    def __str__(self):
           return f"Product Name: {self.title} Current Bidding = {self.bidding} Listed by = {self.listed_by} Category = {self.category}"

