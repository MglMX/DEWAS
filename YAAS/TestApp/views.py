# Create your views here.
from models import Auction
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User, Permission
from django.contrib.auth import login, authenticate, logout, hashers
from datetime import datetime
from django.core.mail import EmailMessage

import re, string


def show_home(request):
    # / points to the "Home" article
    logged_in = False
    username=""
    if request.user.is_authenticated():
        logged_in = True
        username = request.user.username

    auctions = Auction.objects.all()

    return render_to_response("index.html", {'logged_in': logged_in, 'username': username, 'auctions':auctions},
                              context_instance=RequestContext(request))

def show_auction(request,id):
    if Auction.exists(id):
        auction = Auction.get_by_id(id)
        title=auction.title
        description = auction.description
        seller = auction.seller
        deadline = auction.deadline
        last_bid = auction.last_bid
        last_bider = auction.last_bider
        status = auction.status

        is_seller=False
        if seller == request.user.username:
            is_seller=True



        return render_to_response("auction.html",{'title': title, 'description': description,'seller':seller, 'last_bid':last_bid, 'last_bider':last_bider,'deadline':deadline, 'id':id,'is_seller':is_seller},
                                  context_instance=RequestContext(request))

def edit_auction(request,id):
    if Auction.exists(id):
        auction = Auction.get_by_id(id)
        if auction.seller == request.user.username:
            if request.method=="POST":
                auction.description=request.POST["description"]
                auction.desc_version+=1
                auction.save()

                return HttpResponseRedirect("/auction/"+str(auction.id))
            else:
                return render_to_response("editauction.html",{'title':auction.title,'description':auction.description,'id':auction.id},context_instance=RequestContext(request))


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')

def log_in(request):
    print "login beofre post"
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        print "I do login"
        if user is not None:
            print "User logged in!"
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("Bad username or password")


def register(request):
    print "I do register"
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        user = User.objects.create_user(username, email, password)

        user.save()
        return HttpResponseRedirect('/')
    else:
        print "no post register"
        return render_to_response("register.html", context_instance=RequestContext(request))

def edit_account(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            password=request.POST["password"]
            user = request.user

            if user.check_password(password):
                if 'newpassword' in request.POST:
                    newpassword=request.POST["newpassword"]
                    user.set_password(newpassword)

                newemail = request.POST["email"]
                user.email = newemail
                user.save()

        return HttpResponseRedirect('/')

    else:
        logged_in = False
        email= ""
        if request.user.is_authenticated():
            logged_in=True
            email=request.user.email

        return render_to_response("editaccount.html",{'logged_in': logged_in,'email':email}, context_instance=RequestContext(request))

def confirm_auction(request):
    if request.method=="POST":
        if request.POST["save"] == "YES":

            auction = Auction()
            auction.title = request.POST["title"]
            auction.description = request.POST["description"]
            auction.minimun_price = (request.POST["minimum_price"])
            deadline = datetime.strptime(request.POST["deadline"], "%d.%m.%Y_%H:%M")
            auction.deadline = deadline
            auction.last_bid = float(request.POST["minimum_price"])
            auction.status = "ACT"
            auction.seller = request.user.username
            auction.last_bider = ""
            auction.save()

            email = EmailMessage('YAAS: Auction created', 'Hello '+request.user.username+ ",\n Your auction '"+request.POST["title"]+"' has been succesfully created", to=[request.user.email])
            #email.send()

        return HttpResponseRedirect('/')





def create_auction(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            valid=True
            title=request.POST["title"]
            description=request.POST["description"]
            minimum_price=request.POST["minimunprice"]
            message=""

            if float(minimum_price)<0:
                valid=False
                message+="Minimum price must be greater than 0."

            seller = request.user.username
            deadline=request.POST["deadline"]
            result=re.match("[0-9]{2}\.[0-9]{2}\.[0-9]{4}_[0-9]{2}:[0-9]{2}",deadline)

            if result is None:
                valid=False
                message+=" The date does not match the format"
            else:
                date=datetime.strptime(deadline,"%d.%m.%Y_%H:%M")
                days=(date-datetime.now()).days
                if days<3:
                    valid=False
                    message+="The auction has to live at least 72 hours"

            if valid:
                return render_to_response("auctionconfirm.html",{'title':title,'description':description,'minimum_price':minimum_price,'deadline':deadline},context_instance=RequestContext(request))
            else:
                return HttpResponse("Error: "+message)

    else:
        logged_in=False
        if request.user.is_authenticated():
            logged_in=True

        return render_to_response("auctioncreation.html",{'logged_in': logged_in}, context_instance=RequestContext(request))