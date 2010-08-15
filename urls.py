from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Example:
    # (r'^django_dash/', include('django_dash.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

    (r'login', 'dash.views.oauth_login'),
    (r'return', 'dash.views.oauth_return'),

    (r'^$', 'dash.views.home'),
    (r'^home$', 'dash.views.home'),
)
