from django.conf.urls import patterns, include, url
from TestApp.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Test.views.home', name='home'),
    # url(r'^Test/', include('Test.foo.urls')),


    (r'^addblog/$',addblog),
    (r'^editblog/(?P<id>\d+)/$',editblog),
    (r'^myblog/$',show_blogs),
    (r'^myblog/(?P<id>\d+)/$',show_blog),
    (r'^deleteblog/(?P<id>\d+)/$',delete_blog),


    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
