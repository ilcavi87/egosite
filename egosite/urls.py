from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.static import static


import egonet.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'egosite.views.home', name='home'),
    # url(r'^egosite/', include('egosite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', admin.site.urls),

    # urls for egonet
    url(r'^start/$',
        egonet.views.start,
        name='start'),
    url(r'^add_ego/$',
        egonet.views.add_ego, 
        name='add-ego'),
    url(r'^add_alters/$',
        egonet.views.add_alters, 
        name='add-alters'),
    url(r'^explain/$',
        egonet.views.explain,
        name='explain'),
    url(r'^alters_info/$',
        egonet.views.alters_info,
        name='alters-info'),
    url(r'^add_alter_info/([\d]+)/$',
        egonet.views.add_alter_info,
        name='add-alter-info'),
    url(r'^alters_neighbors/$',
        egonet.views.alters_neighbors,
        name='alters-neighbors'),
    url(r'^add_alter_neighbors/([\d]+)/$',
        egonet.views.add_alter_neighbors,
        name='add-alter-neighbors'),
    url(r'^relationships_attrs/$',
        egonet.views.relationships_attrs,
        name='relationship_attrs'),
    url(r'^add_relationship_attrs/([\d]+)/$',
        egonet.views.add_relationship_attrs,
        name='add-relationship-attrs'),
    url(r'^finished/$',
        egonet.views.finished,
        name='finished'),
    url(r'^report/(.*)/$',
        egonet.views.report,
        name='report'),
    url(r'^sample_report/$',
        egonet.views.sample_report,
        name='sample-report'),
    url(r'^terms/$',
        egonet.views.terms,
        name='terms'),
#    url(r'home/$',
#        egonet.views.home,
#        name='home'),
    url(r'^$',
        egonet.views.start,
        name='start'),
    url(r'^compare_alters/$',
        egonet.views.compare_alters,
        name='compare'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
