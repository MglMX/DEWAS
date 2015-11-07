from django.conf.urls import patterns, include, url
from TestApp.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'Test.views.home', name='home'),
                       # url(r'^Test/', include('Test.foo.urls')),


                       (r'^register/$', register),
                       (r'^login/$', log_in),
                       (r'^logout/$', log_out),
                       (r'^editaccount/$', edit_account),
                       (r'^createauction/$', create_auction),
                       (r'^confirmauction/$', confirm_auction),
                       (r'^auction/(?P<id>\d+)$', show_auction),
                       (r'^editauction/(?P<id>\d+)$', edit_auction),
                       (r'^search/$', search),
                       (r'^bid/(?P<id>\d+)$', bid),
                       (r'^banauction/(?P<id>\d+)$', ban),
                       (r'^language/$', change_lang),
                       (r'^api/auction/(?P<id>\d+)$', api_auction),
                       (r'^api/auction/$', api_auctions),

                       url(r'^admin/', include(admin.site.urls)),


                       (r'$', show_home),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:

                       )
