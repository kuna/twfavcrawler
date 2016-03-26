from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import models
import twitter

# -------------------------------

def main(request):
    return render(request, "main.htm")

# if not logined, then go to auth page first
def dashboard(request):
    token = request.session.get('access_token')
    if (token == None):
        return redirect('/auth/')
    return render(request, "dashboard.htm")



# -------------------------------

# if not logined, send to twitter auth page
# otherwise, send to dashboard page
def auth(request):
    auth = twitter.CreateBasicAuth()
    verifier = request.GET.get('oauth_verifier')
    if (verifier == None):
        redirect_url = auth.get_authorization_url()
        request.session['request_token'] = auth.request_token
        return redirect(redirect_url)
    else:
        token = request.session.get('request_token')
        auth.request_token = token
        try:
            token = auth.get_access_token(verifier)
        except tweepy.TweepError:
            return HttpResponse('auth error', status=500)
# save access token   
        access_token = (auth.access_token, auth.access_token_secret)
        request.session['access_token'] = access_token
# save user id to DB
        api = twitter.CreateApi(auth, access_token)
        user_obj = api.me()
        User.objects.update_or_create(
            id=user_obj.id,
            screen_name=user_obj.screen_name,
            name=user_obj.name
        )
        return redirect('/dashboard/')

# just remove token and redirect to home
def logout(request):
    request.session.pop('access_token')
    return redirect('/')

# ------------------------------------------------

# get current status of archive processing
def api_getstatus(request, userid):
    try:
        userobj = User.objects.get(id=userid)
        task = Task.objects.filter(user=userobj).latest('date')
        if (task):
            return JsonResponse({'success': 1,
                'message': str(task.current) + ' / ' + str(task.total)})
        else:
            return JsonResponse({'success': 1,
                'message': 'No task exists.'})
    except:
        return JsonResponse({'success': 0,
            'message': 'Invalid User'})

# make test tweet
def api_testtwit(request):
    token = request.session.get('access_token')
    if (token == None):
        return redirect('/auth/')
    api = twitter.CreateApi(token)

    success = 0
    if api.id:
        success = api.id
    return JsonResponse({'success': success})

# make job
def api_favcrawler(request):
    return JsonResponse({'success': 'under construction'})
