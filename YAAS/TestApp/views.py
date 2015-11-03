# Create your views here.
from models import Auction
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User, Permission
from django.contrib.auth import login, authenticate, logout, hashers
import re, string


def show_home(request):
    # / points to the "Home" article
    logged_in = False
    username=""
    if request.user.is_authenticated():
        logged_in = True
        username = request.user.username

    return render_to_response("index.html", {'logged_in': logged_in, 'username': username},
                              context_instance=RequestContext(request))
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

