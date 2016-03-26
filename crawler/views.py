from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
                
                access_token = (auth.access_token, auth.access_token_secret)
		request.session['access_token'] = access_token
		return redirect('/dashboard/')

# just remove token and redirect to home
def logout(request):
	request.session.pop('access_token')
	return redirect('/')

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
