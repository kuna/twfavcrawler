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
		request.session['request_token'] = (auth.request_token.key, auth.request_token.secret)
		return redirect(redirect_url)
	else:
		token = request.session.get('request_token')
		auth.set_request_token(token[0], token[1])
		try:
			token = auth.get_access_token(verifier)
		except tweepy.TweepError:
			return HttpResponse('auth error', status=500)

		request.session[response_data] = (auth.access_token.key, auth.access_token.secret)
		return redirect('/dashboard/')

# just remove token and redirect to home
def logout(request):
	request.session.delete('access_token')
	return redirect('/')

# make test tweet
def twit_test(request):
	token = request.session.get('access_token')
	if (token == None):
		return redirect('/auth/')
	api = twitter.CreateApi(token[0], token[1])
	success = 0
	if api.id:
		success = api.id
	return JsonResponse({'success': success})

