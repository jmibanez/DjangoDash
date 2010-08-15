# Create your views here.
from dash import models

from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import *

from oauthtwitter import OAuthApi
from oauth import oauth

import datetime

CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY', 'YOUR_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET', 'YOUR_SECRET')

LOGIN = 'dash.views.oauth_login'
SHOW_RUN = 'dash.views.show_run'

def oauth_login(request):
    twitter = OAuthApi(CONSUMER_KEY, CONSUMER_SECRET)
    req_token = twitter.getRequestToken()
    request.session['request_token'] = req_token.to_string()
    signin_url = twitter.getSigninURL(req_token)

    return redirect(signin_url)

def oauth_return(request):
    if 'request_token' not in request.session:
        return redirect('dash.views.oauth_login')

    req_token = oauth.OAuthToken.from_string(request.session['request_token'])
    if req_token.key != request.GET.get('oauth_token', 'no-token'):
        del request.session['request_token']
        return redirect('dash.views.oauth_login')

    twitter = OAuthApi(CONSUMER_KEY, CONSUMER_SECRET, req_token)
    acc_token = twitter.getAccessToken()

    request.session['access_token'] = acc_token.to_string()
    auth_user = authenticate(access_token=acc_token)

    if auth_user:
        login(request, auth_user)
    else:
        del request.session['access_token']
        del request.session['request_token']
        return HttpResponse("Unable to authenticate you!")

    print "User: %s" % auth_user
    print "request.user: %s" % request.user
    print "is_auth: %s" % request.user.is_authenticated()
    return redirect('dash.views.home')


def home(request):
    if not request.user.is_authenticated():
        return redirect(LOGIN)

    user = request.user.get_profile()
    runs = models.RunRecord.objects.filter(user = user)

    return render_to_response("home.html", { "runs" : runs, "user" : user })

def record_run(request):
    if not request.user.is_authenticated():
        return redirect(LOGIN)

    user = request.user.get_profile()

    #run_when = to_date(request.POST["run_when"])
    rec = models.RunRecord(user=user, distance=request.POST["distance"], run_when=datetime.datetime.now())
    rec.save()

    oauth_key = user.oauth_key

    return redirect(SHOW_RUN, run_id=rec.id)


def get_runs(request):
    if not request.user.is_authenticated():
        return redirect(LOGIN)

    user = request.user.get_profile()
    runs = models.RunRecord.filter(user = user)

    return render_to_response("runs.html", { "runs" : runs, "user" : user })

def show_runs_on(request, run_date):
    pass

def show_run(request, run_id):
    print "Run ID: %s" % run_id
    run = get_object_or_404(models.RunRecord, id=run_id)
    return render_to_response("run_details.html", {"run": run})


def get_user(request, user_id):
    user = get_object_or_404(models.RunnerUser, user_id)

    return render_to_response("user_details.html", { "user" : user })

def get_user_runs(request, user_id):
    user = get_object_or_404(models.RunnerUser, user_id)
    runs = models.RunRecord.filter(user = user)

    return render_to_response("runs.html", { "runs" : runs, "user" : user })

def show_user_run(request, user_id, run_id):
    user = get_object_or_404(models.RunnerUser, user_id)
    run = get_object_or_404(models.RunRecord, id=run_id)

    if run.user != user:
        return not_found

    return render_to_response("run_details.html", { "run" : run, "user" : user })

def show_user_runs_on(request, user_id, run_date):
    pass

