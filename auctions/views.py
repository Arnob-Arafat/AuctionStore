from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Comments, Listing
from django.contrib import messages

def index(request):
    return render(request, "auctions/index.html",{
        "listing":Listing.objects.all()
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")
        category = request.POST.get("category")
        image = request.POST.get("image")

        l = Listing(image=image,title=title, description=description,bidding=price,original=price,bidcount=0,listed_by=request.user,category=category)
        l.save()
        return redirect("index")
    return render(request, "auctions/createlist.html")

def listing(request, id):
    errormessage=False
    SellerisHere = request.user is Listing.objects.get(id=id).listed_by
    item = Listing.objects.get(id=id)
    comments = Comments.objects.filter(listing=item)
    return render(request, "auctions/listing.html",{
        "item": Listing.objects.get(id=id),
        "errormessage":errormessage,
        "SellerisHere":SellerisHere,
        "comments":comments,
    })

@login_required
def add(request):
    if request.method == "POST":
        id = request.POST.get('additemid')
        item = Listing.objects.get(id=id)
        request.user.watchlist.add(item)

    return redirect("watchlist")

@login_required
def remove(request):
    if request.method == "POST":
            id = request.POST.get('id')
            item = Listing.objects.get(id=id)
            request.user.watchlist.remove(item)
    
    return redirect("watchlist")

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html",{
        "listing": request.user.watchlist.all()
    })

@login_required
def bid(request):
    error = True
    currentbid = int(request.POST.get("currentbid"))
    item = Listing.objects.get(id=request.POST.get('biditemid'))
    if currentbid >= item.original and (item.bidcount == 0 or currentbid > item.bidding): 
        item.bidding = currentbid
        item.bidcount += 1
        item.currentbidder = request.user
        item.save()
        error = False
        

    return render(request, "auctions/listing.html",{
            "item": item,
            "error":error,
       })

@login_required
def closelisting(request):
    item = Listing.objects.get(id=request.POST.get('closeitemid'))
    buyer = item.currentbidder
    buyer.owned.add(item)
    buyer.save()
    item.sold = True
    item.save()

    return redirect("index")


@login_required
def boughtitems(request):
    owned = request.user.owned.all()
    return render(request, "auctions/bought.html", {
        "owned":owned
    })

@login_required
def comment(request):
    item = Listing.objects.get(id=request.POST.get("commentorid"))
    commentor = request.user
    comment = Comments.objects.create(commentor=commentor, text=request.POST.get('text'), listing=item)
    comment.save()
    return redirect("listing", id = item.id)

def categories(request):
    categories = Listing.objects.exclude(sold=True).exclude(category="").exclude(category__isnull=True).values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html",{
        "categories":categories
    })

def categoricallist(request, category):
    items = Listing.objects.filter(category=category)
    return render(request, "auctions/listbycategory.html",{
        "items":items,
        "category":category,
    })