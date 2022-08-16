from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail.backends import console
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max
from .forms import ListingForm, CategoryForm, BidForm, CommentForm
from .models import User, Listing, Category, Comment, Bid, Watchlist


def index(request):
    active_list = Listing.objects.all().filter(active=True)
    return render(request, 'auctions/index.html', {'active_list': active_list})


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
def add_category(request):
    creatCategForm = CategoryForm()
    if request.method == 'POST':
        creatCategForm = CategoryForm(request.POST)
        if creatCategForm.is_valid():
            creatCategForm.save()
            return redirect('category-list')
    return render(request, 'auctions/addCategory.html', {'creatCategForm': creatCategForm})


def create_listing(request):
    m = ""
    createForm = ListingForm()
    if request.method == 'POST':
        createForm = ListingForm(request.POST)
        if createForm.is_valid():
            obj = createForm.save(commit=False)
            obj.user = request.user
            obj.save()

            return redirect('index')
        else:
            m = "error in validity"

    return render(request, 'auctions/creatListing.html', {'creatForm': createForm, 'm': m})


@login_required
def category_list(request):
    category_list = Category.objects.all()
    return render(request, 'auctions/categoryList.html', {'category_list': category_list})


@login_required
def show_category(request, id):
    active_list = Listing.objects.all().filter(category_id=id, active=True)
    return render(request, 'auctions/index.html', {'active_list': active_list})


def show_listing(request, id):
    list = Listing.objects.get(id=id)
    bid_form = BidForm()
    comment_form = CommentForm()
    comments = Comment.objects.filter(listing=id).all()

    winner = Bid.objects.filter(listing=list).last()
    print(winner)
    if request.method == 'POST':
        bid = BidForm(request.POST)
        comment = CommentForm(request.POST)
        print(comment)
        try:
            bid = request.POST.get('bid')
            bid = float(bid)
            print(bid)
            if bid > list.price:
                list.price = bid
                list.save()
                obj = Bid.objects.create(user=request.user, listing=list, bid=bid)
                obj.save()

            else:
                return render(request, 'auctions/show_list.html', context={

                    'list': list,
                    "message": "previous bids is greatar than your bid",
                    'bid_form': bid_form,
                    'comment_form': comment_form,
                    'comments': comments,
                })

        except:
            comment = request.POST.get('comments')
            obj = Comment.objects.create(user=request.user, comments=comment, listing=list)
            obj.save()
            return redirect('show_list', id)

    obj = Watchlist.objects.all().filter(listing=list, user_id=request.user.id)
    if obj:
        check = True
    else:
        check = False

    return render(request, 'auctions/show_list.html', context={
        'list': list,
        'bid_form': bid_form,
        'comment_form': comment_form,
        'comments': comments,
        'winner': winner,
        'check': check
    })


def watchlist(requset, id):
    list = Listing.objects.get(id=id)
    obj = Watchlist.objects.all().filter(listing=list, user_id=requset.user.id)

    if obj:
        obj.delete()
        print(list.on_watch_list)
        # return redirect('show_list', list.id)
        context = {
            'list': list,
            "message": "previous bids is greatar than your bid",
            'bid_form': BidForm(),
            'comment_form': CommentForm(),
            'comments': Comment.objects.filter(listing=id).all(),
            'check': False
        }
        return render(requset, 'auctions/show_list.html', context)
    else:
        list.save()
        obj.create(listing=list, user_id=requset.user.id)
        print(list.on_watch_list)
        # return redirect('show_list', list.id)

        context = {
            'list': list,
            "message": "previous bids is greatar than your bid",
            'bid_form': BidForm(),
            'comment_form': CommentForm(),
            'comments': Comment.objects.filter(listing=id).all(),
            'check': True
        }
        return render(requset, 'auctions/show_list.html', context)

def show_watchlist(request):
    products = Watchlist.objects.filter(user=request.user)
    print(list)
    return render(request, 'auctions/watchlist.html', context={
        'items': products
    })


def show_closed_listing(request):
    listing = Listing.objects.filter(active=False)
    return render(request, 'auctions/closed_listings.html', context={
        'listing': listing
    })


def close_list(request, id):
    obj = Listing.objects.get(id=id)
    obj.active = False
    obj.save()
    return redirect('show_closed_listing')
