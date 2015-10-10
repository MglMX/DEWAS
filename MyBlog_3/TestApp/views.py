
# Create your views here.
from models import Article,Blog
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from datetime import datetime
import re,string

def addblog(request):
    blog = Blog()
    blog.timestamp=datetime.now()
    blog.save()
    if request.method == "POST" and request.POST.has_key("content"):
        # a valid POST request: save the new contents of the article
        # Always clean the input from the user
        blog.title = request.POST["title"]
        blog.content_body = request.POST["content"]
        blog.timestamp = datetime.now()
        blog.save()
        # Always redirect after a successful POST request
        return HttpResponseRedirect('/myblog/' )
    else:
        # a GET request or a POST request using the worng form: show the form
        print "id:"+str(blog.id)+"titulo:(vacio segurmente juejue):"+str(blog.title)
        return render_to_response("edit.html",
            {'id':blog.id,'title': blog.title, 'content': blog.content_body},
            context_instance=RequestContext(request)
        )


def show_blog(request,id):
    if Blog.exists(id):
        blog=Blog.get_by_id(id)
    else:
        t = get_template("index.html")
        html = t.render(Context({'content':"The blog does not exist"}))
        return HttpResponse(html)

    t = get_template("show.html")
    # merge the template with the data from the article
    html = t.render(Context({'id':blog.id, 'name': blog.title, 'content': blog.content_body}))
    # create a response object and return it
    return HttpResponse(html)


def show_blogs(request):
    the_content=""
    for blog in Blog.objects.all():
        the_content+="<p><a href='/myblog/"+str(blog.id) +"'>\r"+blog.title+"</a> </p>\n\r"

    print the_content
    t=get_template("index.html")
    html= t.render(Context({"content":the_content}))

    return HttpResponse(html)

def delete_blog(request,id):
    blog=Blog.get_by_id(id)
    blog.delete()

    return HttpResponseRedirect('/myblog/')


def editblog(request,id):
    if Blog.exists(id):
        # find an existing article
        print "The article exist wihiii"
        blog = Blog.get_by_id(id)
    else:
        # create a new article
        blog = Blog()
        blog.timestamp=datetime.now()
        blog.save()


    if request.method == "POST" and request.POST.has_key("content"):
        print "Ahora si se ha hecho el post"
        # a valid POST request: save the new contents of the article
        # Always clean the input from the user
        blog.content_body = request.POST["content"]
        blog.title = request.POST["title"]
        blog.timestamp=datetime.now()

        blog.save()
        # Always redirect after a successful POST request
        return HttpResponseRedirect('/myblog/')
    else:
        print "No se ha hecho ekl post"
        # a GET request or a POST request using the worng form: show the form
        return render_to_response("edit.html",
            {'id': blog.id, 'title': blog.title, 'content': blog.content_body},
            context_instance=RequestContext(request)
        )

