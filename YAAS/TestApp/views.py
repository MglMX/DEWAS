# Create your views here.
from models import Auction
from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User, Permission
from django.contrib.auth import login, authenticate, logout, hashers
from datetime import datetime
from django.core.mail import EmailMessage
import json
from django.core import serializers

import re, string

def api_auction(request,id):
    auction = Auction.get_by_id(id)
    auction_ser = serializers.serialize('json',[auction,])
    struct = json.loads(auction_ser)
    auction_ser = json.dumps(struct[0])

    return HttpResponse(auction_ser, content_type='application/json')

def api_auctions(request):
    auctions = Auction.objects.all()
    auctions_ser = serializers.serialize('json',auctions)
    struct = json.loads(auctions_ser)
    auctions_ser = json.dumps(struct)

    return HttpResponse(auctions_ser, content_type='application/json')

def change_lang(request):
    if request.method=="POST":
        lang=request.POST["language"]
        print "lang: "+lang
        request.session["lang"]=lang
        return HttpResponseRedirect("/")

def show_home(request):
    # / points to the "Home" article
    logged_in = False
    username = ""
    if request.user.is_authenticated():
        logged_in = True
        username = request.user.username

    auctions = Auction.objects.exclude(status="BAN")

    if "lang" not in request.session:
        request.session["lang"]="ENG"

    if request.session["lang"]=="ENG":
        template="index.html"
    elif request.session["lang"]=="ESP":
        template="index-es.html"


    return render_to_response(template, {'logged_in': logged_in, 'username': username, 'auctions': auctions},
                              context_instance=RequestContext(request))


def ban(request,id):
    if request.user.is_superuser and Auction.exists(id):
        auction = Auction.get_by_id(id)
        auction.status="BAN"
        auction.save()

        return HttpResponseRedirect("/auction/"+str(auction.id)+"?m=banned")

    return HttpResponseRedirect("/")



def show_auction(request, id):
    if Auction.exists(id):
        auction = Auction.get_by_id(id)
        title = auction.title
        description = auction.description
        seller = auction.seller
        deadline = auction.deadline
        last_bid = auction.last_bid
        last_bider = auction.last_bider
        status = auction.status
        desc_version = auction.desc_version

        is_seller = False
        if seller == request.user.username:
            is_seller = True

        is_super = False

        if request.user.is_superuser:
            is_super = True


        #Status to show in the template

        print "Status: "+status
        if status=="ACT":
            status_m="ACTIVE"
        elif status=="BAN":
            status_m="BANNED"
        elif status=="DUE":
            status_m="DUE"
        else:
            status_m="ADJUDICATED"

        m=request.GET.get('m','')

        show_msg=True
        message=""
        if m=="success":
            message="Bid placed succesfully! "
        elif m=="banned":
            message="The auction has been banned"
        elif m == "changed":
            message="The description of the auction has changed or your bid is not big enough. Please place your bet again."
        elif m == "own_act":
            message="You cannot bid you own auction"
        else:
            show_msg=False

        if request.session["lang"]=="ENG":
            template="auciton.html"
        elif request.session["lang"]=="ESP":
            template="auction-es.html"

        return render_to_response(template,
                                  dict(title=title, description=description, desc_version=desc_version, seller=seller,
                                       last_bid=last_bid, last_bider=last_bider, deadline=deadline, id=id,
                                       is_seller=is_seller, show_msg=show_msg,message=message,status=status_m,is_super=is_super),
                                  context_instance=RequestContext(request))


def search(request):
    query = request.GET.get('title', '')
    print "Query: " + query
    auctions = Auction.objects.filter(Q(title__icontains=query))

    return render_to_response("searchresult.html", {'auctions': auctions}, context_instance=RequestContext(request))


def bid(request, id):

    if request.user.is_authenticated() and Auction.exists(id):
        print "Bid: "+str(request.POST["bid"])
        placed_bid = round(float(request.POST["bid"]), 2)
        auction = Auction.get_by_id(id)
        print "placed_bid: "+str(placed_bid)+" last_bd: "+str(auction.last_bid)+" resta: "+str(placed_bid - float(auction.last_bid))
        if auction.desc_version != int(request.POST["desc_version"]) or (placed_bid - float(auction.last_bid)) < 0.01:
            return HttpResponseRedirect("/auction/"+str(auction.id)+"?m=changed")
        elif auction.seller==request.user.username:
            return HttpResponseRedirect("/auction/"+str(auction.id)+"?m=own_auct")
        elif auction.status == "ACT":

            #Email to the seller
            seller = User.objects.get(username=auction.seller)
            email = EmailMessage('YAAS: Someone bid on your auction '+auction.title,
                                 'Hello ' + seller.username + ",\n The user '" + request.user.username + "' has place a bid.", to=[seller.email])
            email.send()

            #Email to the last bidder
            email = EmailMessage('YAAS: You placed a bid on '+auction.title,
                                 'Hello ' + request.user.username + ",\n You have correctly place a bid", to=[request.user.email])
            email.send()

            print "Las_bider: "+str(auction.last_bider)
            #Email to the previous bidder
            if auction.last_bider != "":
                previous_bidder = User.objects.get(username=auction.last_bider)
                email = EmailMessage('YAAS: Someone increased your bid on '+auction.title,
                                 'Hello ' + request.user.username + ",\n Someone has placed a bid bigger than yours.", to=[previous_bidder.email])
                email.send()

            auction.last_bid = placed_bid
            auction.last_bider = request.user.username

            auction.save()
            return HttpResponseRedirect("/auction/"+str(auction.id)+"?m=success")
    else:
        return HttpResponseRedirect("/")


def edit_auction(request, id):
    if Auction.exists(id):
        auction = Auction.get_by_id(id)
        if auction.seller == request.user.username:
            if request.method == "POST":
                auction.description = request.POST["description"]
                auction.desc_version += 1
                auction.save()

                return HttpResponseRedirect("/auction/" + str(auction.id))
            else:
                return render_to_response("editauction.html",
                                          {'title': auction.title, 'description': auction.description,
                                           'id': auction.id}, context_instance=RequestContext(request))


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
            password = request.POST["password"]
            user = request.user
            print "The user is authenticated!! pass: "+str(request.POST["password"])
            if user.check_password(password):
                if 'newpassword' in request.POST and request.POST["newpassword"]!="":
                    print "New password: "+request.POST["newpassword"]
                    newpassword = request.POST["newpassword"]
                    user.set_password(newpassword)

                print "The passwotd is correct"
                newemail = request.POST["email"]
                print "New email: "+newemail
                user.email = newemail
                user.save()

        return HttpResponseRedirect('/')

    else:
        print "Has hecho get"
        logged_in = False
        email = ""
        if request.user.is_authenticated():
            logged_in = True
            email = request.user.email

        return render_to_response("editaccount.html", {'logged_in': logged_in, 'email': email},
                                  context_instance=RequestContext(request))


def confirm_auction(request):
    if request.method == "POST":
        if request.POST["save"] == "YES":
            auction = Auction()
            auction.title = request.POST["title"]
            auction.description = request.POST["description"]
            auction.minimun_price = round(float(request.POST["minimum_price"]), 2)
            deadline = datetime.strptime(request.POST["deadline"], "%d.%m.%Y_%H:%M")
            auction.deadline = deadline
            auction.last_bid = round(float(request.POST["minimum_price"]), 2)
            auction.status = "ACT"
            auction.seller = request.user.username
            auction.last_bider = ""
            auction.save()

            email = EmailMessage('YAAS: Auction created',
                                 'Hello ' + request.user.username + ",\n Your auction '" + request.POST[
                                     "title"] + "' has been succesfully created", to=[request.user.email])
            email.send()

        return HttpResponseRedirect('/')


def create_auction(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            valid = True
            title = request.POST["title"]
            description = request.POST["description"]
            minimum_price = request.POST["minimunprice"]
            message = ""

            if float(minimum_price) < 0:
                valid = False
                message += "Minimum price must be greater than 0."

            seller = request.user.username
            deadline = request.POST["deadline"]
            result = re.match("[0-9]{2}\.[0-9]{2}\.[0-9]{4}_[0-9]{2}:[0-9]{2}", deadline)

            if result is None:
                valid = False
                message += " The date does not match the format"
            else:
                date = datetime.strptime(deadline, "%d.%m.%Y_%H:%M")
                days = (date - datetime.now()).days
                if days < 3:
                    valid = False
                    message += "The auction has to live at least 72 hours"

            if valid:
                return render_to_response("auctionconfirm.html",
                                          {'title': title, 'description': description, 'minimum_price': minimum_price,
                                           'deadline': deadline}, context_instance=RequestContext(request))
            else:
                return HttpResponse("Error: " + message)

    else:
        logged_in = False
        if request.user.is_authenticated():
            logged_in = True

        return render_to_response("auctioncreation.html", {'logged_in': logged_in},
                                  context_instance=RequestContext(request))
