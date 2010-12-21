from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'pearson/$', 'contingency.views.index'),
	(r'pearson/compare/$', 'contingency.views.compare_with'),
	(r'^site_media/(?P<path>.*)/$', 'django.views.static.serve',
	        {'document_root': settings.STATIC_DOC_ROOT}),
    # Example:
    # (r'^PearsonBot/', include('PearsonBot.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
