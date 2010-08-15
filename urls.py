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
    (r'^record-run$', 'dash.views.record_run'),

    (r'^my-runs/$', 'dash.views.get_runs'),
    (r'^my-runs/on/(?P<run_date>\d{2}-\d{2}-\d{4})$', 'dash.views.show_runs_on'),
    (r'^my-runs/(?P<run_id>[A-Za-z0-9]+)$', 'dash.views.show_run'),

    (r'^users/(?P<user_id>\w+)$', 'dash.views.get_user'),
    (r'^users/(?P<user_id>\w+)/runs$', 'dash.views.get_user_runs'),
    (r'^users/(?P<user_id>\w+)/run/(?P<run_id>[A-Za-z0-9]+)$', 'dash.views.show_user_run'),
    (r'^users/(?P<user_id>\w+)/runs-on/(?P<run_date>\d{2}-\d{2}-\d{4})$', 'dash.views.show_user_runs_on'),
)
