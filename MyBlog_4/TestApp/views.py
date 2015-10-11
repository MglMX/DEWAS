# Create your views here.
from models import Blog
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from datetime import datetime
import re, string


def addblog(request):
    blog = Blog()
    blog.timestamp = datetime.now()
    blog.save()
    if request.method == "POST" and request.POST.has_key("content"):
        # a valid POST request: save the new contents of the article
        # Always clean the input from the user
        blog.title = request.POST["title"]
        blog.content_body = request.POST["content"]
        blog.timestamp = datetime.now()
        blog.save()

        # Always redirect after a successful POST request
        return HttpResponseRedirect('/myblog/')
    else:
        # a GET request or a POST request using the worng form: show the form
        print "id:" + str(blog.id) + "titulo:(vacio segurmente juejue):" + str(blog.title)
        request.session['blogs_created']+=1
        return render_to_response("edit.html",
                                  {'id': blog.id, 'title': blog.title, 'content': blog.content_body,'version':blog.version},
                                  context_instance=RequestContext(request)
                                  )


def show_blog(request, id):
    if Blog.exists(id):
        blog = Blog.get_by_id(id)
        request.session['blogs_visited']+=1
    else:
        t = get_template("index.html")
        html = t.render(Context({'content': "The blog does not exist"}))
        return HttpResponse(html)

    t = get_template("show.html")
    # merge the template with the data from the article
    html = t.render(Context({'id': blog.id, 'name': blog.title, 'content': blog.content_body}))
    # create a response object and return it
    return HttpResponse(html)

def erase_stats(request):

    request.session['blogs_visited']=0

    request.session['blogs_edited']=0

    request.session['blogs_created']=0

    request.session['blogs_deleted']=0

    request.session["date"]=str(datetime.now())

    return HttpResponseRedirect('/myblog/')

def show_blogs(request):

    blogs=Blog.objects.all()

    for blog in blogs:
        print str("blog : "+blog.title+ "content: "+blog.content_body+ "id: "+str(blog.id))

    if "blogs_visited" not in request.session:
        request.session['blogs_visited']=0
    if "blogs_edited" not in request.session:
        request.session['blogs_edited']=0
    if "blogs_created" not in request.session:
        request.session['blogs_created']=0
    if "blogs_deleted" not in request.session:
        request.session['blogs_deleted']=0
    if "date" not in request.session:
        request.session["date"]=str(datetime.now())

    blogs_visited=request.session['blogs_visited']
    blogs_edited=request.session['blogs_edited']
    blogs_created=request.session['blogs_created']
    blogs_deleted=request.session['blogs_deleted']
    date=request.session['date']

    t = get_template("index.html")
    html = t.render(Context({"blogs": blogs,"blogs_visited":blogs_visited,"blogs_edited":blogs_edited,"blogs_created":blogs_created,"blogs_deleted":blogs_deleted,"session_date":str(date)}))

    return HttpResponse(html)


def delete_blog(request, id):

    if Blog.exists(id):

        blog = Blog.get_by_id(id)
        blog.delete()

        request.session['blogs_deleted']+=1

    return HttpResponseRedirect('/myblog/')



def editblog(request, id):
    if Blog.exists(id):
        # find an existing article
        print "The article exists wihiii"
        blog = Blog.get_by_id(id)
    else:
        # create a new article
        blog = Blog()
        blog.timestamp = datetime.now()
        blog.save()

    if request.method == "POST" and request.POST.has_key("content") and request.POST.has_key("version"):
        edited_version=int(request.POST["version"])
        print "Version of the blog: "+ str(edited_version)
        content=request.POST["content"]
        if edited_version==blog.version:
            # a valid POST request: save the new contents of the article
            # Always clean the input from the user
            blog.content_body = content
            blog.title = request.POST["title"]
            blog.timestamp = datetime.now()
            blog.version+=1
            blog.save()

            request.session['blogs_edited']+=1

            # Always redirect after a successful POST request
            return HttpResponseRedirect('/myblog/')
        else:
            print "Version of the blog in conflict: "+ str(edited_version)
            return render_to_response("conflict.html",{'title': blog.title,'content': blog.content_body, 'user_content': content, 'id': blog.id, 'version': blog.version},context_instance=RequestContext(request))


    else:
        print "No se ha hecho ekl post"
        # a GET request or a POST request using the worng form: show the form
        return render_to_response("edit.html",
                                  {'id': blog.id, 'title': blog.title, 'content': blog.content_body,'version':blog.version},
                                  context_instance=RequestContext(request)
                                  )
