from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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


def add_listing_view(request):
    if request.method=="GET":
        return render(request,"auctions/add_listing.html")
    else:
        name = request.POST["name"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST["image"]
        category = request.POST["category"]
        Listing.objects.create(name=name, description=description, starting_bid=price, image=image, category=category, owner=request.user)
        return HttpResponseRedirect(reverse("index"))
    

def listing_view(request, id):
    listing = Listing.objects.get(pk=id)
    in_watchlist = False
    if request.user.is_authenticated:
        if request.user.watchlist.filter(pk=id).exists():
            in_watchlist = True

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": in_watchlist,
    })

def watchlist(request):
    if request.method=="POST":
        listing_id = request.POST["listing_id"]
        listing = Listing.objects.get(pk=listing_id)
        if request.user.watchlist.filter(pk=listing_id).exists():
            request.user.watchlist.remove(listing)
        else:
            request.user.watchlist.add(listing)
        return HttpResponseRedirect(reverse("listing",args=[listing_id]))
    else:
        return render(request,"auctions/watchlist.html",{
            "watchlist": request.user.watchlist.all()
        })
    
def add_bid(request, id):
    if request.method=="POST":
        bid = int(request.POST["bid"])
        listing = Listing.objects.get(pk=id)
        current_bit = listing.current_price()

        if bid > current_bit:
            Bid.objects.create(user=request.user, listing=listing, bid=bid)
            return HttpResponseRedirect(reverse("listing",args=[id]))
        else:
            return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": request.user.watchlist.filter(pk=id).exists(),
        "message": "Bid must be higher than the current price!"
        })

def close_bid(request,id):
    if request.method=="POST":
        listing=Listing.objects.get(pk=id)
        if request.user == listing.owner:
            
            listing.is_active = False
            listing.save()
        return HttpResponseRedirect(reverse("listing",args=[id]))

def comment(request,id):
    if request.method=="POST":
        user = request.user
        comment = request.POST["comment"]
        listing =Listing.objects.get(pk=id)
        new_comment = Comment(user=user, comment=comment, listing=listing)
        new_comment.save()
        return HttpResponseRedirect(reverse("listing",args=[id]))
    
def category(request):
    categories = Listing.objects.values_list("category",flat=True).distinct()
    return render(request,"auctions/categories.html",{
        "categories": categories,
    })

def specific_category(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request,"auctions/index.html",{
        "listings" : listings,
    })