# Create your views here.
from dash import models
from dash.tweet import tweet_record

from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import *

from oauthtwitter import OAuthApi
from oauth import oauth

import datetime

CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY', 'YOUR_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET', 'YOUR_SECRET')

LOGIN = 'dash.views.oauth_login'

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

