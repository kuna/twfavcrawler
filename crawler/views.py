from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from models import *
import twitter

# -------------------------------

def main(request):
    return render(request, "main.htm")

# if not logined, then go to auth page first
def dashboard(request):
    token = request.session.get('access_token')
    if (token == None):
        return redirect('/auth/')
    try:
        user_obj = User.objects.get(token=token[0])
        return render(request, "dashboard.htm", {
            "userid": user_obj.id,
            "username": user_obj.screen_name,
            })
    except Exception as e:
        raise e
#        return HttpResponse('user cannot found', status=500)



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
# save user id, name, tokens to DB
        api = twitter.CreateApi(auth, access_token)
        user_obj = api.me()
        request.session['twitter_id'] = user_obj.id
        User.objects.update_or_create(
            id=user_obj.id,
            screen_name=user_obj.screen_name,
            name=user_obj.name,
            token=access_token[0],
            token_secret=access_token[1]
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
        task = Task.objects.filter(user=userobj, status=0)
        if (task):
            task = task.latest('date')
            return JsonResponse({'success': 1,
                'message': task.message,
                'value': task.current / task.total})
        else:
            return JsonResponse({'success': 0,
                'message': 'No task exists.'})
    except Exception as e:
        return JsonResponse({'success': 0,
            'message': 'invalid user'})

# make test tweet
def api_testtwit(request, userid):
    token = request.session.get('access_token')
    if (token == None):
        return JsonResponse({'success': 0,
            'message': 'login please'})
    api = twitter.CreateApi(token)
    api.update_status('test - http://tw.insane.pe.kr')
    return JsonResponse({'success': 1,
        'message': 'ok'})

# just make task stop
# TODO what task? - currently most recent one.
def api_taskstop(request, userid):
    token = request.session.get('access_token')
    if (token == None):
        return JsonResponse({'success': 0,
            'message': 'login please'})

    try:
        userobj = User.objects.get(id=userid)
        task = Task.objects.filter(user=userobj, status=0)
        if (task.count() > 0):
            task = task.latest('date')
            task.status = 2
            task.message = "Stopped"
            task.save()
            return JsonResponse({'success': 1,
                'message': 'Stopped task successfully'})
        else:
            return JsonResponse({'success': 0,
                'message': 'No task exists.'})
    except Exception as e:
        raise e
#        return JsonResponse({'success': 0,
#            'message': 'invalid user'})

# make job
def api_favcrawler(request, userid):
    token = request.session.get('access_token')
    if (token == None):
        return JsonResponse({'success': 0,
            'message': 'login please'})
    api = twitter.CreateApi(token)

    try:
        userobj = User.objects.get(id=userid)
        task = Task.objects.filter(user=userobj, status=0)
        if (task.count() == 0 and twitter.Task_CrawlFavTweet(api)):
            return JsonResponse({'success': 1,
                'message': 'Started task successfully'})
        else:
            return JsonResponse({'success': 0,
                'message': 'Currently running task exists!'})
    except Exception as e:
        raise e
#        return JsonResponse({'success': 0,
#            'message': 'under construction'})
